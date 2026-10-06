# Implantação no Dot

Este procedimento exige uma conta com Dot, computador na nuvem, delegação nativa e os conectores necessários. A disponibilidade precisa ser verificada na conta de destino. Não há instalador que contorne essas dependências.

## Preparação

1. Criar ou reutilizar um Dot coordenador e uma única planilha privada conforme [planilha.md](planilha.md).
2. Conferir acesso de leitura e escrita ao Sheets, busca pública e leitura restrita de Gmail. Manter habilitadas confirmações nativas para candidatura, envio de documentos e contato com recrutadores.
3. Obter uma versão revisada deste repositório e fixar o commit. Ler o código antes de executá-lo; não atualizar automaticamente a partir de main em cada rodada.
4. Guardar o pacote e o estado em um diretório privado no computador do Dot, fora de área temporária. Copiar config.example.json para config.local.json e preencher somente ali os identificadores.
5. Executar os testes e a demonstração no ambiente de destino:

```sh
python3 -m unittest -v test_harness.py
python3 demo.py
```

6. Na primeira implantação, reconciliar as candidaturas existentes. Só então criar estado novo:

```sh
mkdir -p state
python3 harness.py --db state/state.sqlite3 init
```

O construtor Python permite criar bancos para testes. O CLI operacional exige init explícito e recusa estado ausente nas outras ações. init nunca sobrescreve um arquivo existente. Não usar init automaticamente após erro ou perda de arquivos.

## Ativação e carga das skills

Ler manifest.json e skills/coordenar-vagas/SKILL.md. Antes de delegar, ler a skill do especialista e passá-la com entrada delimitada, parcela do orçamento e contrato de saída. Não basta colocar arquivos em disco e presumir descoberta automática.

Verificar uma delegação nativa que produza identificador e resultado separado. Um texto simulando quatro papéis no mesmo contexto não satisfaz o teste.

Reutilizar o agendamento já existente a cada duas horas. Apenas o coordenador grava no Sheets. O preparador é acionado por seleção humana; Gmail é consultado somente para processos rastreados.

### Instrução para a rotina nativa

> Execute o pacote revisado na versão fixada registrada na configuração privada. Leia a skill de coordenação e carregue explicitamente cada skill antes de delegar. Releia perfil, decisões e histórico da planilha. Verifique estado privado e tentativas pendentes. Reserve o orçamento global antes de criar agentes. Consolide e confira atualizações por ID, preservando correções humanas. Registre versão, IDs de agentes, consumo, evidências e falhas. Avise apenas vagas de alta aderência com disponibilidade e elegibilidade confirmadas, mudanças relevantes de processo, falhas persistentes ou decisões necessárias. Não envie candidaturas nem contate recrutadores sem autorização específica do pacote exato. Estado ausente ou resultado ambíguo exige reconciliação, nunca repetição automática.

A instrução é um modelo para a configuração nativa, não uma automação criada pelo repositório.

## Interface do harness

Todos os comandos, exceto init e status, recebem JSON pela entrada padrão. A saída de sucesso é JSON; erro produz código de saída diferente de zero.

```sh
printf '%s' '{"run_id":"run-example-001"}' |
  python3 harness.py --db state/state.sqlite3 start
printf '%s' '{"run_id":"run-example-001","searches":3,"descriptions":5}' |
  python3 harness.py --db state/state.sqlite3 reserve
python3 harness.py --db state/state.sqlite3 status
printf '%s' '{"run_id":"run-example-001","result":"Leituras conferidas e histórico registrado"}' |
  python3 harness.py --db state/state.sqlite3 finish
```

Os contratos de approve, claim_submission, confirm, job_key e merge_patch são exercitados em test_harness.py e demo.py. As aprovações da demonstração são fictícias e não valem para uma candidatura real.

## Recuperação

- **Rodada ativa após interrupção:** consultar agentes ainda em execução, consumo, histórico e gravações; encerrar filhos pendentes antes de liberar o bloqueio. Registrar resultado reconciliado com finish e recovered=true. Não iniciar outra rodada para renovar orçamento.
- **Tentativa em verificação:** consultar recibo do portal e mensagens associadas. A ausência de confirmação não libera novo envio. O pacote não possui comando de reenvio automático.
- **Banco ausente, ilegível ou incompatível:** interromper candidaturas e registrar incidente. Reconciliar primeiro planilha, histórico, evidências e backup; uma planilha “Autorizada” isolada não é suficiente.
- **Backup:** guardar cópia consistente do SQLite por sua API de backup em armazenamento privado. Não copiar apenas o arquivo principal enquanto há WAL ativo. Registrar versão, instante e integridade; nunca publicar o backup.
- **Migração:** a versão 0.1.0 cria um esquema inicial; não contém migração automática de bancos de protótipos anteriores. Preservar o original e planejar migração explicitamente.
- **Falha de conector:** conservar dados existentes, registrar cobertura incompleta e prosseguir apenas nas atividades independentes.

## Critério de implantação

Registrar caminho real na nuvem, commit, resultado dos testes, modo de carga das skills, IDs reais dos agentes, gravações conferidas e a atualização do agendamento. Depois verificar uma rodada agendada posterior. Reabrir um arquivo em outro processo demonstra persistência local; não demonstra recuperação após troca ou expiração do computador na nuvem.
