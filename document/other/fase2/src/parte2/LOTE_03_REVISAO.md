> **Estado atual em 22/09/2026:** os seis lotes foram consolidados em 60 frases. Este documento preserva o registro de aprovação deste lote; contagens e pendências mencionadas abaixo descrevem aquele momento. Consulte [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md) para o estado atual.

# Lote 3 — aprovado

Preparado em 22/09/2026. **Status: aprovado pelo responsável pelo projeto em 22/09/2026.** P21–P30 foram incorporadas à proveniência com seus textos exatos. São 30 frases aprovadas, 15 por classe. O CSV de treinamento mantém os 12 registros anteriores durante a curadoria.

Origem textual de todas as frases: nova elaboração sintética com apoio de IA (assistente Codex). Rótulos propostos pelo projeto segundo os critérios didáticos aprovados. As instituições citadas não são autoras das frases nem dos rótulos; não há validação clínica.

| ID | Frase proposta | Classe proposta | Referência e justificativa do rótulo | Família inicial |
|---|---|---|---|---|
| P21 | Meu coração parece bater muito devagar e estou com dificuldade para respirar mesmo em repouso. | alto risco | R2: percepção de batimentos lentos associada a dificuldade respiratória; não se infere diagnóstico específico. | palpitacao_respiratorio |
| P22 | Começou uma pressão no peito enquanto eu descansava e agora sinto a dor chegar ao rosto. | alto risco | R1: desconforto torácico com irradiação para o rosto. | toracico_irradiacao_rosto |
| P23 | Não estou suando, mas sinto um aperto no peito junto com falta de ar desde que acordei. | alto risco | R1: sintomas torácicos e respiratórios afirmados; negar suor não os anula. | toracico_respiratorio |
| P24 | Já parei de caminhar, mas o peso no peito continua e estou com suor frio. | alto risco | R1: desconforto torácico persistente associado a suor frio. | toracico_suor |
| P25 | Parece que meu coração pula algumas batidas; junto disso, estou com dor no peito e tontura. | alto risco | R2: percepção de falhas nos batimentos associada a dor torácica e tontura. | palpitacao_toracico_presincope |
| P26 | Meu polegar ficou um pouco dolorido depois de uma pequena torção; hoje está melhor e consigo mexê-lo sem dificuldade. | baixo risco | R4: cenário localizado, pouco intenso e em melhora; rótulo didático, sem diagnóstico de entorse. | polegar_torcao_melhora |
| P27 | Senti um incômodo leve na panturrilha depois do treino, mas ele passou com o descanso e hoje estou bem. | baixo risco | R4: contexto sintético de esforço muscular com queixa resolvida e bem-estar atual. | panturrilha_esforco_melhora |
| P28 | O incômodo leve na lombar depois de carregar uma mala está diminuindo; não tenho formigamento nem fraqueza nas pernas e sigo minha rotina. | baixo risco | R3: melhora, pouca intensidade e contexto de esforço, com negação de manifestações nas pernas; ausência isolada de um sinal não define segurança. | costas_esforco_melhora |
| P29 | A pequena dor no punho após a torção está quase passando; não há inchaço e consigo usar a mão normalmente. | baixo risco | R4: cenário localizado em melhora com função preservada; rótulo é uma convenção do exercício. | punho_torcao_melhora |
| P30 | Não sinto palpitações nem tontura; estou bem e fiz minhas atividades habituais sem desconforto. | baixo risco | Critério interno de bem-estar explícito com sintomas negados; sem referência clínica individual. | bem_estar |

## Fontes

Conferidas em 22/09/2026. Identificadores mantidos de [FONTES_DATASET.md](FONTES_DATASET.md).

- **R1 — Ministério da Saúde:** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto), seção Sintomas: desconforto torácico, irradiação para rosto, suor frio e falta de ar.
- **R2 — NHLBI/NIH:** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms): batimentos lentos, irregulares ou percebidos como falhas, além de dor torácica, dificuldade respiratória e tontura/desmaio.
- **R3 — NHS:** [Back pain](https://www.nhs.uk/conditions/back-pain/): possíveis causas musculares, evolução e sinais de alerta. Não fornece o rótulo baixo risco de P28.
- **R4 — NHS:** [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/): lesões musculares/ligamentares, regiões afetadas e evolução. Não diagnostica as lesões fictícias nem fornece os rótulos de P26, P27 e P29.

## Diversidade e limites

P21 introduz batimento percebido como lento; P22, irradiação ao rosto. P23 e P30 incluem negações em classes diferentes. Ainda há exemplos próximos dos lotes anteriores: P21 com P04/P13; P23 com P01/P05; P24 com P02/P14; P25 com P15; P28 com P06/P08/P19; P29 com P07; P30 com os relatos de bem-estar.

Antes do treino, revisar famílias globalmente, inclusive a semelhança entre locais diferentes de queixas após esforço/torção. Os nomes atuais são provisórios; mudar o local ou a redação não garante independência. Esses exemplos ajudam a estudar limitações do TF-IDF (capítulo 11) e vieses de seleção (capítulo 07), mas não comprovam compreensão de negações nem generalização clínica. A predominância de queixas torácicas na classe alta e musculoesqueléticas/bem-estar na baixa permanece uma limitação a documentar.

A aprovação deste lote está registrada: 30 frases aprovadas, 15 por classe. Restam elaborar e revisar 30 frases, 15 por classe. O CSV de treinamento será consolidado depois da curadoria final.