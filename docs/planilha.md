# Planilha: interface e contratos

Criar uma planilha privada com cinco abas. Os nomes e estados abaixo são o contrato; os identificadores da instância pertencem à configuração privada.

| Aba | Campos principais |
|---|---|
| Resumo | Novas relevantes, pendentes de leitura, candidaturas por etapa, decisões necessárias e última rodada |
| Vagas | ID estável, empresa, cargo, portal, ID no portal, URL original, URLs alternativas, requisitos, elegibilidade, aderência, justificativa, desconhecidos, disponibilidade, leitura, decisão, datas e evidências |
| Candidaturas | ID, ID da vaga, destino, versão do perfil, documentos, hashes, respostas, versão do pacote, referência da aprovação, etapa, tentativa, recibo, datas, próxima ação e correções |
| Histórico | Evento, instante, rodada, agente, entidade, ação, resultado, evidência, versão do pacote e cobertura |
| Perfil e configuração | Fatos, fontes, divergências, preferências, campos pendentes, limites, versão do código e estado de implantação |

## Três dimensões independentes

| Dimensão | Valores |
|---|---|
| Sua leitura | Não vista · Vista · Salva · Descartada |
| Disponibilidade | Aberta · Encerrada · Não verificada |
| Candidatura | Em preparação · Aguardando autorização · Autorizada · Envio em verificação · Enviada · Entrevista · Proposta · Rejeitada · Retirada |

A leitura feita pelo agente não marca a vaga como vista pelo candidato. Vaga encerrada continua no histórico. Silêncio não implica rejeição. Um convite para teste deve ser descrito na próxima ação, sem inventar entrevista.

Sua decisão pode usar Sem decisão, Quero preparar e Não tenho interesse. “Quero preparar” dispara somente a preparação. Aderência usa Alta, Parcial ou Baixa; elegibilidade usa confirmada, incompatível ou a confirmar.

## Propriedade e alterações

O candidato controla Sua leitura, Sua decisão, Suas notas e Suas correções. O coordenador mapeia os títulos para os nomes de contrato sua_leitura, sua_decisao, suas_notas e suas_correcoes antes de merge_patch. Outras correções observadas desde a leitura também geram conflito, em vez de sobrescrita.

Usar IDs estáveis, nunca números de linha como identidade. Reler, escrever somente as células necessárias e conferir o resultado. Estender tabela, filtros e fórmulas conforme cresce o conjunto. Não presumir que uma fórmula limitada a mil linhas cobre registros posteriores.

## Perfil e avaliação

Cada fato profissional tem fonte, grau de confirmação e eventual divergência. Preservar a trajetória e distinguir especialidade, prática e liderança. Inglês, salário, contratação e disponibilidade pendentes são desconhecidos.

Cada requisito obrigatório é atendido, não atendido ou desconhecido. Incompatibilidade territorial explícita prevalece sobre palavras semelhantes no título. Notificar Alta somente com anúncio aberto e elegibilidade verificados.

## Evidências e privacidade

Registrar trecho curto ou resumo fiel, URL e instante da consulta. Para e-mail, referenciar a mensagem pertinente ao processo; não copiar caixa de entrada inteira. Os dados reais não pertencem ao repositório público.
