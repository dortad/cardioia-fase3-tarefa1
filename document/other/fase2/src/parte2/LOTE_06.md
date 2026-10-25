# Lote 6 — concluído sob autorização

Data: 2026-09-22. O responsável autorizou preparar os lotes restantes sem nova aprovação individual. Revisão didática pelo assistente Codex; não atribuir aprovação individual do usuário nem validação clínica a estas frases.

As dez frases são novas elaborações sintéticas com apoio de IA. As fontes contextualizam os cenários; não são origem literal das frases nem autoras dos rótulos. Todas foram incorporadas aos CSVs de treinamento e proveniência.

| ID | Frase | Classe | Referência | Justificativa didática | Família inicial |
|---|---|---|---|---|---|
| P51 | Não sinto dor nos braços, mas estou com pressão no peito, muito pálido e quase desmaiando. | alto risco | R1 | Desconforto torácico, palidez e sensação de desmaio afirmados; negação da dor nos braços não anula a combinação. | toracico_presincope |
| P52 | Meu coração está batendo muito forte e não consigo respirar direito; não tenho dor no peito. | alto risco | R2 | Palpitações com dificuldade respiratória; negação ao final da frase se aplica à dor, não aos demais sintomas. | palpitacao_respiratorio |
| P53 | Depois de uma colisão de carro, comecei a sentir dor nas costas, embora ainda consiga caminhar. | alto risco | R3 | Dor nas costas após acidente importante consta entre os sinais de atendimento imediato; caminhar não elimina esse contexto. | costas_trauma_alerta |
| P54 | Machucou pouco quando virei o pé, mas desde então não sinto os dedos e eles estão formigando. | alto risco | R4 | Perda de sensibilidade e formigamento após lesão são alertas na fonte; intensidade inicial pequena não elimina esses sinais. | pe_trauma_alerta |
| P55 | A dor nas costas começou de repente, ficou muito forte e estou me sentindo febril e com calafrios. | alto risco | R3 | Dor intensa de início súbito e sintomas sistêmicos são contextos de avaliação urgente na fonte; rótulo binário didático. | costas_alerta_sistemico |
| P56 | Meu polegar ainda incomoda um pouco desde a torção, mas a dor diminuiu e já consigo segurar objetos normalmente. | baixo risco | R4 | Queixa localizada pouco intensa em melhora com função preservada; não equivale a avaliação clínica. | polegar_torcao_melhora |
| P57 | Depois do exercício, a panturrilha ficou levemente dolorida; hoje ela não dói mais e caminho como de costume. | baixo risco | R4 | Queixa muscular após esforço resolvida no cenário sintético; rótulo por convenção do projeto. | panturrilha_esforco_melhora |
| P58 | Fiquei com um pequeno incômodo no joelho depois de caminhar mais que o habitual; ele vem diminuindo e consigo dobrar a perna normalmente. | baixo risco | R4 | Contexto de esforço localizado com melhora e mobilidade preservada, sem afirmar diagnóstico específico. | joelho_esforco_melhora |
| P59 | A dor leve no punho após a torção está melhorando; sinto os dedos normalmente, sem formigamento, e consigo usar a mão. | baixo risco | R4 | Queixa pouco intensa em melhora e função preservada com sensibilidade afirmada; rótulo sintético não fornecido pela fonte. | punho_torcao_melhora |
| P60 | Não estou sentindo nenhum desconforto hoje; minha respiração está normal e me sinto disposto. | baixo risco | criterio_interno | Bem-estar atual explícito, por critério interno; ausência de desconforto não comprova ausência de doença. | bem_estar |

## Fontes

Conferidas em 22/09/2026.

- **R1 — Ministério da Saúde:** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto).
- **R2 — NHLBI/NIH:** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms).
- **R3 — NHS:** [Back pain](https://www.nhs.uk/conditions/back-pain/).
- **R4 — NHS:** [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/).

O critério interno indica bem-estar explícito no cenário, sem fonte clínica individual. R3 e R4 também fundamentam sinais de alerta de queixas não cardíacas: alto risco nesta base significa prioridade didática de avaliação, não diagnóstico de doença cardíaca. Detalhes e limitações em [FONTES_DATASET.md](FONTES_DATASET.md) e [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md).
