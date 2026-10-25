> **Estado atual em 22/09/2026:** os seis lotes foram consolidados em 60 frases. Este documento preserva o registro de aprovação deste lote; contagens e pendências mencionadas abaixo descrevem aquele momento. Consulte [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md) para o estado atual.

# Lote 2 — aprovado

Preparado em 22/09/2026. **Status: aprovado pelo responsável pelo projeto em 22/09/2026.** P11–P20 foram incorporadas à proveniência, mantendo seus textos exatos. São 20 frases aprovadas, dez por classe. O CSV de treinamento permanece com os 12 registros anteriores.

Todas as frases abaixo são novas elaborações sintéticas com apoio de IA (assistente Codex). As referências contextualizam os sintomas; não forneceram as frases nem os rótulos. As classes são propostas didáticas pelos critérios aprovados, sem validação clínica.

| ID | Frase proposta | Classe proposta | Referência e justificativa do rótulo | Família inicial |
|---|---|---|---|---|
| P11 | Estou com um peso no peito há meia hora e a dor se espalhou para as costas. | alto risco | R1: desconforto torácico prolongado com extensão para as costas. | toracico_irradiacao_costas |
| P12 | Sinto um aperto no peito, fiquei pálido e parece que vou desmaiar. | alto risco | R1: desconforto torácico associado a palidez e sensação de desmaio. | toracico_presincope |
| P13 | Não estou com dor no peito, mas meu coração bate irregularmente e estou com muita falta de ar. | alto risco | R2: alteração percebida dos batimentos e dificuldade respiratória; a negação da dor não anula os sintomas afirmados. | palpitacao_respiratorio |
| P14 | O incômodo no peito é leve, mas começou junto com suor frio e dificuldade para respirar. | alto risco | R1: sintomas associados motivam o rótulo; a palavra leve não determina a classe. | toracico_suor |
| P15 | Meu coração está disparado, sinto dor no peito e estou quase desmaiando. | alto risco | R2: palpitações com dor torácica e sensação de desmaio. | palpitacao_toracico_presincope |
| P16 | Torci o tornozelo ontem; hoje a dor está menor, o inchaço diminuiu e consigo apoiar o pé. | baixo risco | R4: cenário sintético localizado e em melhora; apoiar o pé isoladamente não determina risco. | tornozelo_torcao_melhora |
| P17 | Depois de correr, senti um pequeno incômodo na coxa; ele diminuiu com o descanso e caminho normalmente. | baixo risco | R4: contexto de possível esforço muscular, sem afirmar diagnóstico; melhora e pouca intensidade são critérios didáticos combinados. | coxa_esforco_melhora |
| P18 | O braço ficou um pouco dolorido depois de carregar sacolas ontem; hoje está melhor, sem dor no peito nem falta de ar. | baixo risco | R4: cenário localizado após esforço e em melhora, com negação explícita de sintomas; dor no braço isoladamente não deve definir a classe. | braco_esforco_melhora |
| P19 | A dor que senti nas costas depois de mudar os móveis passou; hoje estou bem e voltei à minha rotina. | baixo risco | R3: queixa anterior resolvida e bem-estar atual, por convenção didática. | costas_esforco_melhora |
| P20 | Acordei disposto, fiz minhas tarefas e terminei o dia sem nenhum incômodo. | baixo risco | Critério interno de bem-estar explícito; sem fonte clínica individual atribuída. | bem_estar |

## Fontes e alcance

Fontes conferidas em 22/09/2026; identificadores mantidos de [FONTES_DATASET.md](FONTES_DATASET.md).

- **R1 — Ministério da Saúde:** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto), seção Sintomas. Fundamenta o contexto de desconforto torácico, irradiação, suor frio, palidez, falta de ar e sensação de desmaio.
- **R2 — NHLBI/NIH:** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms). Fundamenta o contexto de batimentos alterados, dificuldade respiratória, dor torácica e tontura/desmaio.
- **R3 — NHS:** [Back pain](https://www.nhs.uk/conditions/back-pain/). Contextualiza dor nas costas e evolução; não atribui baixo risco ao relato sintético.
- **R4 — NHS:** [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/). Contextualiza lesões e esforços musculares e seus sinais de alerta; não fornece rótulos de baixo risco nem confirma diagnóstico para essas frases.

## Cuidados de avaliação

P13 compartilha família com P04; P14 com P02; P19 com P06/P08; P20 com P09/P10. Esses agrupamentos devem ser revistos globalmente antes da divisão treino/teste. Mudar a redação não transforma automaticamente um cenário em exemplo independente.

P14 introduz a palavra leve na classe alta e P18 introduz dor no braço na classe baixa. O objetivo é permitir examinar atalhos lexicais, não garantir que TF-IDF compreenda contexto ou negação. Persistem limitações: predominância de cenários torácicos na classe alta e musculoesqueléticos/bem-estar na classe baixa. Relatar esse viés na avaliação; não interpretar acurácia como desempenho clínico.

A aprovação foi registrada em proveniencia_frases.csv. O terceiro lote [P21–P30](LOTE_03_REVISAO.md) também foi aprovado. O total atual é de 30 frases aprovadas; restam 30 para completar 60.