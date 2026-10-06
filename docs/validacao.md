# Validação

Este registro separa execução reproduzível do código e observações do ambiente privado. Data inicial: 2026-10-06.

## Reprodução pública

Execute python3 -m unittest -v test_harness.py e python3 demo.py. Resultado local: 17 testes passaram e a demonstração terminou com resultado OK. A execução foi repetida em uma cópia clonada do GitHub, com o mesmo resultado.

| Ambiente verificado | Python | Suíte | Demonstração |
|---|---|---|---|
| Checkout de publicação | 3.13.7 | 17/17 passaram | OK |
| Clone novo do repositório público | 3.12.14 | 17/17 passaram | OK |
| Computador do Dot na nuvem, conforme execução registrada no Histórico privado | 3.12.14 | 17/17 passaram | OK |

SHA-256 de harness.py validado: ed5353028044c6278220968b47ef330848e9380361027b059dd2edd1ceacd5c8.

 O modelo em ci/github-actions.yml executa ambos com Python 3.11 e 3.12 quando for ativado. O CI ainda não está ativo: o GitHub recusou a gravação de workflow pela conexão atual, sem o escopo workflow.

A suíte cobre identidade de vagas, orçamento global, exclusão de rodadas, preservação de campos humanos, falta de autorização, alterações de material, formato de hash, estado ausente, inicialização que não sobrescreve dados, interrupção, reabertura em processo separado, tentativa duplicada com outro ID de candidatura, recibo obrigatório e reconciliação com evidência.

Não há chamada de rede, candidatura real, acesso a caixa de entrada ou dependência de credencial nesses testes.

## Ambiente privado

| Item | Evidência disponível | Limite |
|---|---|---|
| Planilha de cinco abas | Criação, leitura de retorno e inspeção da interface | IDs e conteúdo não publicados |
| Rotina a cada duas horas | Configuração nativa salva | Recorrência futura depende do serviço |
| Confirmação para candidaturas | Regra nativa conferida | Não houve novo envio real |
| Busca, extração, Sheets e Gmail | Chamadas do piloto e histórico privado | Não garante permissões em outra conta |
| Subagentes nativos | Pesquisador, acompanhamento e avaliador retornaram resultados em contextos separados, com IDs reais registrados e relidos no Histórico | Contextos separados não são teste de isolamento de ferramentas |
| Python na nuvem | 17 testes e demonstração executados; resultado e hash do harness registrados e relidos na planilha | Não prova retenção após reinício do ambiente |
| Skills do pacote | Cinco arquivos validados; rotina nativa salva exige leitura explícita antes de delegar | Descoberta automática não presumida |
| Harness e implantação multiagente | Pacote fixado instalado; SQLite inicializado após reconciliação; agendamento atualizado e conferido na interface | Rodada concluída, gravações conferidas, integridade SQLite OK e backup consistente registrado |

O pacote implantado corresponde ao commit 301efb8a66d9f59f8929d9f91d6453597bd2115d, árvore Git 3d9859c5e94059ac9fcecc51baafde8273d5014a. Os 18 arquivos foram conferidos pelo Dot contra os objetos do repositório. A atualização da rotina foi registrada às 18h22 de Brasília e seu conteúdo com caminho, hashes, skills, delegação e comandos do harness foi conferido na interface. Os IDs operacionais e os caminhos privados permanecem fora deste relatório.

## Rodada multiagente concluída

A rodada de validação reutilizou dez vagas em cache e consumiu zero consultas e zero descrições novas. Pesquisador, acompanhamento e avaliador foram acionados nativamente; o preparador não foi acionado porque nenhuma vaga foi selecionada para preparação.

O avaliador retornou oito aderências Parciais e duas Baixas, sem Alta. O coordenador preservou as classificações existentes, corrigiu duas confirmações insuficientes de elegibilidade territorial para A confirmar e manteve os campos humanos. A data original da fonte em cache foi preservada.

Foram conferidas 23 células de vagas, os registros da implantação e a configuração. O harness encerrou a rodada como complete depois da leitura de retorno. Integridade SQLite e backup consistente foram registrados. Nenhuma nova candidatura, mensagem, documento pessoal ou resposta a teste foi enviada. Esses resultados constam do Histórico privado, relido pelo responsável pela implantação; dados e referências pessoais não foram publicados.

## Pendências

Verificar uma rodada agendada posterior. Exercitar recuperação de estado em ambiente substituído. Medir relevância com revisão humana. Verificar um envio real apenas se houver aprovação de uma candidatura concreta.

Não há afirmação de entrevistas obtidas, contratação, redução percentual de esforço ou garantia de execução contínua.
