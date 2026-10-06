# Validação

Este registro separa execução reproduzível do código e observações do ambiente privado. Data inicial: 2026-10-06.

## Reprodução pública

Execute python3 -m unittest -v test_harness.py e python3 demo.py. Resultado local: 17 testes passaram e a demonstração terminou com resultado OK. O modelo em ci/github-actions.yml executa ambos com Python 3.11 e 3.12 quando for ativado. O CI ainda não está ativo: o GitHub recusou a gravação de workflow pela conexão atual, sem o escopo workflow.

A suíte cobre identidade de vagas, orçamento global, exclusão de rodadas, preservação de campos humanos, falta de autorização, alterações de material, formato de hash, estado ausente, inicialização que não sobrescreve dados, interrupção, reabertura em processo separado, tentativa duplicada com outro ID de candidatura, recibo obrigatório e reconciliação com evidência.

Não há chamada de rede, candidatura real, acesso a caixa de entrada ou dependência de credencial nesses testes.

## Ambiente privado

| Item | Evidência disponível | Limite |
|---|---|---|
| Planilha de cinco abas | Criação, leitura de retorno e inspeção da interface | IDs e conteúdo não publicados |
| Rotina a cada duas horas | Configuração nativa salva | Recorrência futura depende do serviço |
| Confirmação para candidaturas | Regra nativa conferida | Não houve novo envio real |
| Busca, extração, Sheets e Gmail | Chamadas do piloto e histórico privado | Não garante permissões em outra conta |
| Subagentes nativos | Dot reportou criação, troca de mensagens e retorno em contextos separados | Relato operacional, não teste de isolamento |
| Python na nuvem | Dot reportou execução e reabertura de arquivo entre contextos | Não prova retenção após reinício do ambiente |
| Skills do pacote | Cinco arquivos com contratos e carga explícita prevista | Descoberta automática não presumida |
| Harness e implantação multiagente | Código testável neste repositório; ativação na nuvem em verificação | Não confundir publicação com ativação |

## Pendências

Conferir a versão publicada executando na nuvem e uma rodada agendada posterior. Exercitar recuperação de estado em ambiente substituído. Medir relevância com revisão humana. Verificar um envio real apenas se houver aprovação de uma candidatura concreta.

Não há afirmação de entrevistas obtidas, contratação, redução percentual de esforço ou garantia de execução contínua.
