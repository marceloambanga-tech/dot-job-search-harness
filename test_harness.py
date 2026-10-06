import copy
import os
import sqlite3
import json
import subprocess
import sys
import tempfile
import unittest
from harness import Harness, canonical_url, job_key, merge_patch

class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, 'state.sqlite3')
        self.h = Harness(self.path)
        self.package = {'vacancy_id':'V-test','destination':'https://example.com/apply/42',
                        'documents':[{'name':'cv.pdf','sha256':'a'*64}],
                        'answers':{'availability':'confirmada pelo usuário'},'version':'1'}
    def tearDown(self):
        self.h.close()
        self.tmp.cleanup()
    def test_tracking_and_identity_parameters(self):
        self.assertEqual(canonical_url('https://example.com/job?id=42&utm_source=x#top'), 'https://example.com/job?id=42')
        self.assertNotEqual(canonical_url('https://example.com/job?id=42'),canonical_url('https://example.com/job?id=43'))
    def test_distinct_jobs_same_company(self):
        j={'portal':'gupy','organization':'empresa','portal_id':'42'}
        self.assertNotEqual(job_key(j),job_key({**j,'portal_id':'43'}))
    def test_one_writer_survives_restart(self):
        self.h.start('r1')
        other=Harness(self.path)
        try:
            with self.assertRaises(sqlite3.IntegrityError):other.start('r2')
        finally:other.close()
    def test_budget_is_global(self):
        self.h.start('r1');self.h.reserve('r1',3,6);self.h.reserve('r1',3,4)
        with self.assertRaises(ValueError):self.h.reserve('r1',1,0)
        with self.assertRaises(ValueError):self.h.reserve('r1',0,1)
        self.assertEqual(self.h.status()['runs'][0][2:4],(6,10))
    def test_negative_reservation_rejected(self):
        self.h.start('r1')
        with self.assertRaises(ValueError):self.h.reserve('r1',-1,0)
    def test_manual_fields_and_concurrent_change(self):
        old={'sua_leitura':'Salva','status':'Aberta','suas_notas':'minha nota'}
        current={**old,'status':'Corrigido pelo usuário'}
        result=merge_patch(old,current,{'sua_leitura':'Vista','status':'Encerrada','suas_notas':'apagar','last_checked':'hoje'})
        self.assertEqual(result,{'patch':{'last_checked':'hoje'},'conflicts':['status']})
    def test_status_alone_does_not_authorize(self):
        with self.assertRaises(ValueError):self.h.claim_submission('C1',self.package,'Autorizada')
    def test_material_change_invalidates_approval(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada')
        changed=copy.deepcopy(self.package);changed['documents'][0]['sha256']='b'*64
        with self.assertRaises(ValueError):self.h.claim_submission('C1',changed,'Autorizada')
    def test_document_digest_must_be_real_hex_format(self):
        invalid=copy.deepcopy(self.package);invalid['documents'][0]['sha256']='z'*64
        with self.assertRaises(ValueError):self.h.approve('C1',invalid,'Mensagem humana identificada')
    def test_cli_missing_state_does_not_silently_reset(self):
        missing=os.path.join(self.tmp.name,'missing.sqlite3')
        result=subprocess.run([sys.executable,'harness.py','--db',missing,'status'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(os.path.exists(missing))
    def test_cli_init_never_overwrites_existing_state(self):
        self.h.start('existing')
        result=subprocess.run([sys.executable,'harness.py','--db',self.path,'init'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(self.h.status()['runs'][0][0],'existing')
    def test_interrupted_submission_never_repeats(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada')
        self.h.claim_submission('C1',self.package,'Autorizada')
        other=Harness(self.path)
        try:
            self.assertEqual(other.status()['attempts'][0][1],'Envio em verificação')
            with self.assertRaises(sqlite3.IntegrityError):other.claim_submission('C1',self.package,'Autorizada')
            with self.assertRaises(ValueError):other.approve('C1',self.package,'Outro clique')
        finally:other.close()
    def test_sheet_pending_blocks_even_if_local_db_empty(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada')
        with self.assertRaises(ValueError):self.h.claim_submission('C1',self.package,'Envio em verificação')
    def test_new_process_observes_pending_and_refuses_repeat(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada');self.h.claim_submission('C1',self.package,'Autorizada')
        result=subprocess.run([sys.executable,'harness.py','--db',self.path,'status'],capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(result.stdout)['attempts'][0][1],'Envio em verificação')
        repeated=subprocess.run([sys.executable,'harness.py','--db',self.path,'claim_submission'],
            input=json.dumps({'application_id':'C1','package':self.package,'sheet_state':'Autorizada'}),capture_output=True,text=True)
        self.assertNotEqual(repeated.returncode,0)
    def test_new_application_id_cannot_repeat_same_vacancy(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada');self.h.claim_submission('C1',self.package,'Autorizada')
        self.h.approve('C2',self.package,'Mensagem humana identificada')
        with self.assertRaises(sqlite3.IntegrityError):self.h.claim_submission('C2',self.package,'Autorizada')
    def test_receipt_required_and_sent_remains_blocked(self):
        self.h.approve('C1',self.package,'Mensagem humana identificada');self.h.claim_submission('C1',self.package,'Autorizada')
        with self.assertRaises(ValueError):self.h.confirm('C1','')
        self.h.confirm('C1','https://example.com/receipt/42')
        with self.assertRaises(sqlite3.IntegrityError):self.h.claim_submission('C1',self.package,'Autorizada')
    def test_recovery_requires_evidence_and_does_not_reset_budget(self):
        self.h.start('r1');self.h.reserve('r1',6,10)
        with self.assertRaises(ValueError):self.h.finish('r1','',True)
        self.h.finish('r1','Rodada reconciliada com histórico',True);self.h.start('r2')
        self.assertEqual(self.h.status()['runs'][0][2:4],(6,10))

if __name__=='__main__':unittest.main()
