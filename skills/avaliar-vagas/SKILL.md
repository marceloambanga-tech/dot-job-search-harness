---
name: avaliar-vagas
description: Avaliar aderência de vagas ao perfil documentado do candidato, distinguindo fatos, lacunas e requisitos desconhecidos.
---

Receba vagas e fatos profissionais com fontes e estado de revisão. Distinga certificação de fluência, liderança de prática diária e fatos confirmados de métricas sem fonte. Documentos divergentes exigem revisão.

Para cada obrigatório, registre `atendido`, `nao_atendido` ou `desconhecido`, com evidência. Restrição presencial/híbrida ou território incompatível torna a vaga inelegível. Dado profissional pendente não é um requisito comprovadamente não atendido. Inglês, contratação, salário e início pendentes não eliminam por si sós.

Alta exige correspondência concreta ao perfil e requisitos principais suficientemente fundamentados. Requisito obrigatório desconhecido pede Parcial e esclarecimento. Parecido no título não basta. Disponibilidade é independente da aderência; anunciar uma vaga Alta exige anúncio original aberto e remoto Brasil verificado pelo coordenador.

Retorne `run_id`, `agent_id`, `assessments`: cada item com chave da vaga, `fit` (Alta/Parcial/Baixa), `met`, `gaps`, `unknowns`, `eligibility`, `rationale`, `evidence_refs`. Não reescreva o currículo nem altere a planilha. Sem necessidade de ferramentas de escrita.
