# Lote 5 — concluído sob autorização

Data: 2026-09-22. O responsável autorizou preparar os lotes restantes sem nova aprovação individual. Revisão didática pelo assistente Codex; não atribuir aprovação individual do usuário nem validação clínica a estas frases.

As dez frases são novas elaborações sintéticas com apoio de IA. As fontes contextualizam os cenários; não são origem literal das frases nem autoras dos rótulos. Todas foram incorporadas aos CSVs de treinamento e proveniência.

| ID | Frase | Classe | Referência | Justificativa didática | Família inicial |
|---|---|---|---|---|---|
| P41 | O aperto no peito aliviou por alguns minutos, mas voltou e agora estou com suor frio. | alto risco | R1 | Desconforto torácico atual associado a suor frio; melhora anterior não elimina os sinais atuais. Evolução temporal é elaboração sintética. | toracico_suor |
| P42 | Percebo meu coração batendo devagar e, ao mesmo tempo, sinto dor no peito e uma tontura forte. | alto risco | R2 | Batimentos lentos percebidos com dor torácica e tontura; não se infere causa específica. | palpitacao_toracico_presincope |
| P43 | Além da dor nas costas, apareceu uma dificuldade para urinar que eu não tinha antes. | alto risco | R3 | Alteração urinária nova associada a dor nas costas consta entre os sinais de atendimento imediato da fonte. | costas_alerta_neurologico |
| P44 | Torci o tornozelo, o inchaço está aumentando muito e não consigo dar mais que alguns passos. | alto risco | R4 | Piora importante do inchaço e incapacidade de caminhar após lesão motivam avaliação urgente na fonte; a classe é a convenção binária do projeto. | tornozelo_trauma_alerta |
| P45 | Meu dedo ficou torto depois de uma pancada; a dor é pequena, mas ele está com um formato diferente. | alto risco | R4 | Deformidade após lesão é sinal de alerta na fonte; pouca dor isoladamente não determina classe baixa. | dedo_trauma_alerta |
| P46 | Senti uma dorzinha no braço depois de levantar pesos ontem; ela está diminuindo e não sinto falta de ar nem aperto no peito. | baixo risco | R4 | Contexto sintético de esforço localizado, melhora e sintomas negados; ausência de sintomas torácicos isoladamente não define segurança. | braco_esforco_melhora |
| P47 | Meu joelho ficou um pouco dolorido após o exercício, mas hoje está melhor, sem inchaço, e ando normalmente. | baixo risco | R4 | Queixa localizada pouco intensa e em melhora, por convenção didática; não se afirma diagnóstico de lesão. | joelho_esforco_melhora |
| P48 | O antebraço que incomodou depois de carregar compras não dói mais; consigo usar o braço normalmente e estou bem. | baixo risco | R4 | Queixa após esforço resolvida e bem-estar atual no cenário sintético. | braco_esforco_melhora |
| P49 | Depois de arrastar uma caixa, fiquei com um incômodo discreto na lombar; ele está melhorando e não tenho dormência nas pernas. | baixo risco | R3 | Queixa localizada pouco intensa e em melhora; a negação de dormência é contexto adicional, não critério isolado. | costas_esforco_melhora |
| P50 | Hoje estou bem, sem suor frio ou sensação de desmaio, e consegui cumprir minha rotina sem incômodo. | baixo risco | criterio_interno | Bem-estar explícito e sintomas negados; sem atribuição de fonte clínica individual. | bem_estar |

## Fontes

Conferidas em 22/09/2026.

- **R1 — Ministério da Saúde:** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto).
- **R2 — NHLBI/NIH:** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms).
- **R3 — NHS:** [Back pain](https://www.nhs.uk/conditions/back-pain/).
- **R4 — NHS:** [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/).

O critério interno indica bem-estar explícito no cenário, sem fonte clínica individual. R3 e R4 também fundamentam sinais de alerta de queixas não cardíacas: alto risco nesta base significa prioridade didática de avaliação, não diagnóstico de doença cardíaca. Detalhes e limitações em [FONTES_DATASET.md](FONTES_DATASET.md) e [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md).
