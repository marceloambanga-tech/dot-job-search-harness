# Case: busca recorrente de vagas com revisão humana

## Problema

Encontrar vagas é apenas uma parte da procura por emprego. É preciso verificar se a oportunidade ainda existe, se aceita candidatos no território desejado, distinguir a leitura de uma vaga do envio de uma candidatura e acompanhar respostas sem perder o histórico.

A proposta reúne essas atividades em uma planilha controlada pelo candidato, com um Dot responsável pela rotina e especialistas delegados para tarefas que exigem contextos diferentes.

## Objetivo e escopo

Descobrir e avaliar oportunidades remotas, preparar materiais com fatos profissionais confirmados e acompanhar processos. A busca pode ser recorrente; o envio depende de aprovação específica. O projeto não tem como objetivo maximizar candidaturas automáticas.

O primeiro recorte inclui liderança técnica, engenharia sênior, IA e desenvolvimento mobile, com elegibilidade para trabalhar remotamente a partir do Brasil. Preferências ainda não informadas permanecem desconhecidas, sem serem inventadas.

## Decisões de engenharia

| Decisão | Motivo | Custo ou limite |
|---|---|---|
| Um coordenador e especialistas sob demanda | Centralizar decisões sem misturar todos os contextos | Depende de delegação real no ambiente |
| Sheets como interface | Permitir revisar, marcar leitura e corrigir dados diretamente | Concorrência por célula exige cuidado |
| Skills separadas por tarefa | Reutilizar procedimentos e contratos | Arquivos precisam ser carregados explicitamente |
| MCPs existentes | Usar conectores já disponíveis | Permissões e disponibilidade variam entre contas |
| Harness pequeno, sem dependências | Tornar decisões críticas testáveis fora do modelo | Não substitui o runtime nem executa integrações |
| Reserva central de orçamento | Conter consumo mesmo com tarefas paralelas | Cobertura por rodada é limitada |
| Tentativa registrada antes do envio | Evitar repetição após falha ou timeout | Resultados ambíguos exigem reconciliação |
| Aprovação vinculada ao pacote | Evitar usar aprovação antiga para material modificado | Requer conferir a evidência e os bytes finais |

## O que o repositório demonstra

Há código executável para estado, orçamento, deduplicação básica e controle de tentativa; cinco skills com contratos; exemplos sintéticos; testes automatizados e instruções de implantação. O desenho separa descoberta, avaliação, preparação, aprovação, execução e acompanhamento.

No piloto privado, a planilha e o agendamento nativo foram configurados, integrações responderam e uma rodada de validação com dez vagas em cache foi concluída por pesquisador, acompanhamento e avaliador nativos, com resultados registrados e relidos. Os 17 testes também passaram na nuvem; o mesmo agendamento foi atualizado para carregar o pacote fixado. Isso é evidência de viabilidade naquele ambiente, não uma garantia de acesso equivalente em toda conta. Os registros públicos de validação estão em [validacao.md](validacao.md).

## Como medir resultado sem inflar o case

| Indicador | Definição |
|---|---|
| Cobertura | Fontes consultadas e descrições lidas dentro do orçamento |
| Duplicatas | Registros já conhecidos corretamente associados, sem fundir vagas distintas |
| Precisão da triagem | Vagas sinalizadas como relevantes que o candidato confirma como relevantes |
| Rastreabilidade | Proporção de afirmações de disponibilidade/etapa com evidência identificável |
| Integridade do controle | Edições humanas preservadas e tentativas incertas reconciliadas |
| Resultado profissional | Entrevistas/propostas atribuíveis a candidaturas rastreadas |

Os indicadores são critérios propostos. Ainda não há dados suficientes para afirmar ganho de produtividade, precisão de recomendação ou aumento de entrevistas. Testes de software e resultados profissionais são medidas diferentes.

## Próximos marcos

1. Conferir o pacote executando em uma rodada agendada posterior, com o mesmo estado.
2. Exercitar recuperação em outro ambiente sem repetir tentativas.
3. Avaliar relevância com revisão humana de amostras reais.
4. Demonstrar um envio aprovado e sua confirmação somente quando existir autorização para uma candidatura concreta.

Os artefatos operacionais privados ficam fora do case público. Exemplos fictícios permitem reproduzir as decisões do harness sem publicar currículo, mensagens ou credenciais.
