---
name: preparar-candidatura
description: Preparar currículo e respostas para uma vaga escolhida pelo candidato, produzindo um pacote revisável sem envio.
---

Receba vaga selecionada, perfil revisável e fatos confirmados. Preserve a trajetória; adapte destaque e organização. Não invente métricas, tecnologias, datas, idioma, salário ou disponibilidade. Uma divergência relevante bloqueia aquele campo e gera pergunta específica.

Produza pacote com `vacancy_id`, `destination`, `documents`, `answers`, `version`, `pending_questions` e `source_facts`. Documentos devem ter nome, conteúdo final e SHA-256 dos bytes finais quando materializados. Respostas devem conter texto exato e pergunta correspondente; quando não houver perguntas, registre isso explicitamente. Inclua versão do perfil utilizado.

Não submeta, não preencha portais que transmitam dados, não faça upload pessoal e não contate recrutador. O coordenador materializa arquivos privados e apresenta o pacote ao candidato. Preparar não concede autorização; o hash não é evidência de aprovação humana. Mudança de conteúdo invalida a versão anteriormente aprovada.

Testes pessoais de seleção, como DISC, ficam parao candidato responder. Não produzir respostas fingindo a personalidade do candidato.
