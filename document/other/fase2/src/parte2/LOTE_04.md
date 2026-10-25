# Lote 4 — concluído sob autorização

Data: 2026-09-22. O responsável autorizou preparar os lotes restantes sem nova aprovação individual. Revisão didática pelo assistente Codex; não atribuir aprovação individual do usuário nem validação clínica a estas frases.

As dez frases são novas elaborações sintéticas com apoio de IA. As fontes contextualizam os cenários; não são origem literal das frases nem autoras dos rótulos. Todas foram incorporadas aos CSVs de treinamento e proveniência.

| ID | Frase | Classe | Referência | Justificativa didática | Família inicial |
|---|---|---|---|---|---|
| P31 | Sinto uma pressão forte no peito que agora se espalha para o braço direito. | alto risco | R1 | Desconforto torácico com irradiação ao braço; a fonte inclui o braço direito como apresentação menos frequente. | toracico_braco |
| P32 | Acordei durante a noite com o coração batendo fora do ritmo e estou ofegante mesmo depois de me sentar. | alto risco | R2 | Batimentos percebidos como irregulares associados a dificuldade respiratória; o contexto noturno não altera o critério. | palpitacao_respiratorio |
| P33 | Estou com dor nas costas e comecei a sentir dormência e fraqueza nas duas pernas. | alto risco | R3 | A fonte lista sintomas bilaterais nas pernas associados a dor nas costas entre sinais de atendimento imediato. | costas_alerta_neurologico |
| P34 | Depois que torci o punho, minha mão ficou dormente e o punho parece fora do lugar. | alto risco | R4 | Perda de sensibilidade e deformidade após lesão correspondem a sinais de atendimento imediato descritos na fonte. | punho_trauma_alerta |
| P35 | Virei o pé numa queda e agora ele está frio, com os dedos azulados. | alto risco | R4 | Mudança de cor e extremidade fria após lesão são sinais de alerta descritos na fonte. | pe_trauma_alerta |
| P36 | Após o treino, meu antebraço ficou um pouco dolorido; a dor diminuiu e consigo mexer a mão e o cotovelo normalmente. | baixo risco | R4 | Cenário sintético de esforço muscular localizado, pouco intenso e em melhora; rótulo didático, não fornecido pela fonte. | braco_esforco_melhora |
| P37 | A coxa ainda está um pouco sensível depois da corrida de ontem, mas hoje incomoda menos e caminho sem dificuldade. | baixo risco | R4 | Queixa muscular localizada em melhora com função preservada, segundo a convenção do exercício. | coxa_esforco_melhora |
| P38 | O tornozelo que torci há alguns dias já não dói nem está inchado; voltei a caminhar normalmente. | baixo risco | R4 | Resolução de queixa localizada e função recuperada no cenário fictício; não é diagnóstico nem alta clínica. | tornozelo_torcao_melhora |
| P39 | A pequena dor lombar que tive ao levantar um balde está quase sumindo, sem atrapalhar minhas tarefas. | baixo risco | R3 | Queixa pouco intensa após esforço e em melhora, conforme os critérios didáticos. | costas_esforco_melhora |
| P40 | Passei o dia bem, sem dor, tontura ou dificuldade para respirar. | baixo risco | criterio_interno | Bem-estar atual afirmado, acompanhado de sintomas negados; sem fonte clínica individual. | bem_estar |

## Fontes

Conferidas em 22/09/2026.

- **R1 — Ministério da Saúde:** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto).
- **R2 — NHLBI/NIH:** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms).
- **R3 — NHS:** [Back pain](https://www.nhs.uk/conditions/back-pain/).
- **R4 — NHS:** [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/).

O critério interno indica bem-estar explícito no cenário, sem fonte clínica individual. R3 e R4 também fundamentam sinais de alerta de queixas não cardíacas: alto risco nesta base significa prioridade didática de avaliação, não diagnóstico de doença cardíaca. Detalhes e limitações em [FONTES_DATASET.md](FONTES_DATASET.md) e [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md).
