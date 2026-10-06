---
name: coordenar-vagas
description: Coordenar a busca recorrente de vagas do candidato com especialistas, Google Sheets e autorização específica para candidaturas.
---

Leia `../../ARQUITETURA.md` e `../../manifest.json` na implantação ou quando a versão mudar. Leia também ../../docs/implantacao.md. Na primeira implantação, use init após reconciliar histórico. Nas rodadas seguintes, estado ausente interrompe envios; nunca execute init para esconder a perda de dados. Use somente o Dot e agendamento existentes. A planilha é a interface e contém perfil revisável, decisões, regras e evidências.

## Rodada

1. Leia os cabeçalhos e linhas atuais de Perfil e configuração, Vagas, Candidaturas e Histórico. Reconcilie correções e tentativas pendentes. Campo vazio não revoga evidência de tentativa anterior.
2. Abra o estado persistente com `../../harness.py`. Use caminho absoluto confirmado na nuvem, fora de pasta temporária. `start` exige `run_id` único. Falha por rodada anterior ativa exige investigação e `finish` com evidência; não resetar o arquivo.
3. Reserve orçamento global com `reserve` antes de delegar. Distribua no máximo seis consultas e dez descrições novas no total. Registre consumo real separadamente do reservado. Não reinicie rodada para contornar limites.
4. Leia a skill do especialista e use delegação nativa comprovada, com contexto delimitado. Registre identificadores e resultados reais. Pesquisador e acompanhamento podem rodar em paralelo; avaliador recebe vagas descobertas; preparador só após escolha do candidato. Se delegação não existir, registre degradação, sem chamar simulação de subagente real.
5. Especialistas retornam objetos; não alteram a planilha e não enviam nada. Restrinja ferramentas por perfil quando a API nativa permitir. Caso contrário, declare que a restrição é instrucional. Não forneça o SQLite do coordenador a filhos.
6. Consolide por portal+organização+ID e URL canônica. Para campos de usuário, mapeie Sua leitura → `sua_leitura`, Sua decisão → `sua_decisao`, Suas notas → `suas_notas`, Suas correções → `suas_correcoes`. Use `merge_patch` com snapshot, releitura atual e proposta. Conflito exige releitura/revisão; nunca aplicar automaticamente um valor novo sobre correção manual. Leitura, disponibilidade e candidatura são independentes.
7. Grave somente campos necessários por ID, estenda tabelas/filtros e confira o resultado. Grave Histórico com fontes, contadores, limitações, IDs dos agentes e versão do pacote. Só então finalize a rodada. Notifique apenas eventos acionáveis não comunicados antes.

## Candidatura

Quero preparar só permite rascunho. Não confie em Autorizada isoladamente. Confira mensagem do candidato aprovando vaga, destino, documentos e respostas exatos. Registre `approve` com pacote e referência real da mensagem; documentos contêm SHA-256 dos bytes finais. Revalide a regra nativa de confirmação e a aprovação antes de agir.

`claim_submission` persiste a tentativa. Depois grave e confira Envio em verificação no Sheets; falha nessa escrita impede ação externa. Execute o envio uma vez, no navegador autorizado. Confirmação identificável permite `confirm` e Enviada no Sheets. Timeout, interrupção ou dúvida mantêm a tentativa pendente, sem reenvio automático, mesmo que o estado local tenha sido perdido. Consulte destino/Gmail para reconciliar.

O harness só controla ações encaminhadas por ele e não autentica a mensagem humana. As regras nativas continuam obrigatórias. Não comprar créditos, criar novas permissões ou instalar serviços para superar uma falha.

## Interface do harness

Comandos recebem um objeto JSON por entrada padrão e retornam JSON. Exemplo de reserva: `{"run_id":"rodada-identificada","searches":2,"descriptions":3}`. `status` não recebe payload. `job_key` recebe `{"job":{...}}`; `merge_patch` recebe `snapshot`, `current`, `proposed`. Os testes em `../../test_harness.py` mostram os contratos restantes.

Um arquivo em disco não prova registro de skill. Registre se as skills são carregadas explicitamente ou por descoberta nativa confirmada.
