"""Estado e decisões do Dot Vagas. Sem rede, credenciais ou envio externo."""
import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

USER_FIELDS = {'sua_leitura', 'sua_decisao', 'suas_notas', 'suas_correcoes'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()

def canonical_url(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('URL pública HTTP/HTTPS inválida')
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in {'gclid', 'fbclid'}]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/') or '/', urlencode(sorted(query)), ''))

def job_key(job):
    if all(job.get(k) for k in ('portal', 'organization', 'portal_id')):
        return ':'.join(str(job[k]).strip().casefold() if k != 'portal_id' else str(job[k]).strip()
                        for k in ('portal', 'organization', 'portal_id'))
    return 'url:' + canonical_url(job['original_url'])

def merge_patch(snapshot, current, proposed):
    """Não sobrescreve alteração desde a leitura nem campos pertencentes ao usuário."""
    patch, conflicts = {}, []
    for key, value in proposed.items():
        if key in USER_FIELDS:
            continue
        if current.get(key) != snapshot.get(key):
            conflicts.append(key)
        elif current.get(key) != value:
            patch[key] = value
    return {'patch': patch, 'conflicts': conflicts}

class Harness:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=5)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY, state TEXT NOT NULL, searches INTEGER DEFAULT 0,
            descriptions INTEGER DEFAULT 0, started TEXT NOT NULL, result TEXT);
          CREATE UNIQUE INDEX IF NOT EXISTS one_active_run ON runs(state) WHERE state='active';
          CREATE TABLE IF NOT EXISTS approvals (
            application_id TEXT PRIMARY KEY, package_hash TEXT NOT NULL,
            evidence TEXT NOT NULL, approved_at TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS attempts (
            application_id TEXT PRIMARY KEY, package_hash TEXT NOT NULL,
            state TEXT NOT NULL, claimed_at TEXT NOT NULL, receipt TEXT,
            vacancy_id TEXT NOT NULL UNIQUE);
        ''')
        self.db.commit()

    def close(self):
        self.db.close()

    def transaction(self, fn):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            value = fn()
            self.db.commit()
            return value
        except Exception:
            self.db.rollback()
            raise

    def start(self, run_id):
        def op():
            self.db.execute('INSERT INTO runs(id,state,started) VALUES (?,?,?)',
                            (run_id, 'active', datetime.now(timezone.utc).isoformat()))
            return {'run_id': run_id, 'state': 'active'}
        return self.transaction(op)

    def reserve(self, run_id, searches=0, descriptions=0):
        if any(type(v) is not int or v < 0 for v in (searches, descriptions)):
            raise ValueError('Reservas devem ser inteiros não negativos')
        def op():
            row = self.db.execute('SELECT searches,descriptions FROM runs WHERE id=? AND state=?',
                                  (run_id, 'active')).fetchone()
            if row is None:
                raise ValueError('Rodada ativa não encontrada')
            total = (row[0] + searches, row[1] + descriptions)
            if total[0] > 6 or total[1] > 10:
                raise ValueError('Orçamento global excedido')
            self.db.execute('UPDATE runs SET searches=?, descriptions=? WHERE id=?', (*total, run_id))
            return {'reserved_searches': total[0], 'reserved_descriptions': total[1]}
        return self.transaction(op)

    def finish(self, run_id, result, recovered=False):
        if not str(result).strip():
            raise ValueError('Resultado/evidência da reconciliação obrigatório')
        def op():
            c = self.db.execute('UPDATE runs SET state=?, result=? WHERE id=? AND state=?',
                                ('reconciled' if recovered else 'complete', str(result), run_id, 'active'))
            if c.rowcount != 1:
                raise ValueError('Rodada ativa não encontrada')
            return {'run_id': run_id, 'finished': True}
        return self.transaction(op)

    def approve(self, application_id, package, evidence):
        if not evidence.strip() or any(not package.get(k) for k in ('vacancy_id', 'destination', 'documents', 'answers', 'version')):
            raise ValueError('Pacote completo e evidência humana obrigatórios')
        if (not isinstance(package['documents'], list) or
                any(not isinstance(d, dict) or not isinstance(d.get('sha256'), str) or
                    not re.fullmatch(r'[0-9a-f]{64}', d['sha256']) for d in package['documents'])):
            raise ValueError('Cada documento exige SHA-256 dos bytes aprovados')
        canonical_url(package['destination'])
        def op():
            if self.db.execute('SELECT 1 FROM attempts WHERE application_id=?', (application_id,)).fetchone():
                raise ValueError('Existe tentativa prévia; reconciliar, não reautorizar automaticamente')
            h = digest(package)
            self.db.execute('INSERT OR REPLACE INTO approvals VALUES (?,?,?,?)',
                            (application_id, h, evidence, datetime.now(timezone.utc).isoformat()))
            return {'application_id': application_id, 'package_hash': h}
        return self.transaction(op)

    def claim_submission(self, application_id, package, sheet_state):
        if sheet_state != 'Autorizada':
            raise ValueError('Planilha não está Autorizada; não enviar')
        def op():
            h = digest(package)
            approval = self.db.execute('SELECT package_hash,evidence FROM approvals WHERE application_id=?',
                                       (application_id,)).fetchone()
            if not approval or approval[0] != h or not approval[1]:
                raise ValueError('Não há aprovação verificável para este pacote exato')
            self.db.execute('INSERT INTO attempts VALUES (?,?,?,?,NULL,?)',
                            (application_id, h, 'Envio em verificação', datetime.now(timezone.utc).isoformat(), package['vacancy_id']))
            return {'application_id': application_id, 'package_hash': h, 'state': 'Envio em verificação',
                    'next': 'Gravar e conferir o mesmo estado no Sheets antes de qualquer envio externo'}
        return self.transaction(op)

    def confirm(self, application_id, receipt):
        if not receipt.strip():
            raise ValueError('Confirmação identificável obrigatória')
        def op():
            c = self.db.execute('UPDATE attempts SET state=?, receipt=? WHERE application_id=? AND state=?',
                                ('Enviada', receipt, application_id, 'Envio em verificação'))
            if c.rowcount != 1:
                raise ValueError('Tentativa pendente não encontrada')
            return {'application_id': application_id, 'state': 'Enviada', 'receipt': receipt}
        return self.transaction(op)

    def status(self):
        return {'runs': self.db.execute('SELECT id,state,searches,descriptions,result FROM runs').fetchall(),
                'attempts': self.db.execute('SELECT application_id,state,package_hash,receipt FROM attempts').fetchall()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True, help='SQLite persistente do coordenador')
    parser.add_argument('action', choices=['init', 'start', 'reserve', 'finish', 'approve', 'claim_submission', 'confirm', 'status', 'job_key', 'merge_patch'])
    args = parser.parse_args()
    if args.action == 'init':
        # Criação exclusiva: init nunca reinicializa estado existente.
        with Path(args.db).open('xb'):
            pass
    elif not Path(args.db).is_file():
        parser.error('Estado ausente. Reconciliar planilha e histórico antes de inicializar; não recriar automaticamente.')
    payload = {} if args.action in ('init', 'status') else json.load(sys.stdin)
    h = Harness(args.db)
    try:
        if args.action == 'init':
            print(json.dumps({'initialized': True}))
            return
        fn = {'job_key': job_key, 'merge_patch': merge_patch}.get(args.action) or getattr(h, args.action)
        print(json.dumps(fn(**payload), ensure_ascii=False))
    finally:
        h.close()

if __name__ == '__main__':
    main()
