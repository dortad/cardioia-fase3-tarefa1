# Fundamentação do mapa de sintomas e condições

## Estrutura e finalidade

O `mapa_sintomas_doencas.csv` é uma seleção didática de associações, conforme a Parte 1 do [enunciado](../../document/Enunciado.md). Não é uma ontologia clínica completa nem um instrumento validado de diagnóstico.

São mantidas as colunas `Sintoma 1`, `Sintoma 2` e `Doença Associada`. As duas primeiras contêm formas alternativas de expressar um sintoma; não exigem ocorrência conjunta. O nome da terceira coluna segue o enunciado; Angina é uma manifestação clínica, e Arritmia é uma categoria ampla.

As fontes abaixo fundamentam as associações. A seleção, tradução e adaptação das expressões para linguagem coloquial foram elaboradas no projeto com apoio de IA, não são transcrições literais. Elas não representam a origem dos dez relatos fictícios, documentada no [README](README.md).

## Rastreabilidade das associações

Cada linha do CSV encontra sua referência pela condição e pelo grupo de expressões abaixo. F1 a F5 identificam as referências completas ao final.

| Condição | Expressões do mapa (agrupadas) | Fundamentação | Fonte |
|---|---|---|---|
| Infarto | dor no peito / dor torácica; desconforto no peito / desconforto torácico; aperto no peito / aperto no tórax; pressão no peito / pressão no tórax | Dor ou desconforto peitoral com sensação de peso ou aperto. | F1 |
| Infarto | dor no braço esquerdo / dor no braço do lado esquerdo | A dor pode irradiar para o braço esquerdo. A expressão isolada não comprova irradiação. | F1 |
| Infarto | suor frio / sudorese fria; falta de ar / dificuldade para respirar | Manifestações associadas descritas na fonte. | F1 |
| Infarto | enjoo / náusea | Náusea está entre os sintomas possíveis. | F2 |
| Angina | dor no peito / dor torácica; desconforto no peito / desconforto torácico; aperto no peito / aperto no tórax; pressão no peito / pressão no tórax | Dor ou desconforto torácico pode ser descrito como pressão ou aperto. | F3 |
| Angina | falta de ar / dificuldade para respirar; enjoo / náusea; cansaço extremo / fadiga extrema | Falta de ar, náusea e cansaço extremo são manifestações possíveis. | F3 |
| Insuficiência Cardíaca | cansaço constante / fadiga; cansaço extremo / fadiga extrema | Fadiga, inclusive cansaço extremo após descanso. | F4 |
| Insuficiência Cardíaca | falta de ar / dificuldade para respirar | Dificuldade respiratória em atividades habituais e ao deitar. | F4 |
| Insuficiência Cardíaca | inchaço nas pernas / pernas inchadas | Inchaço de pernas, pés e tornozelos. | F4 |
| Insuficiência Cardíaca | dificuldade para dormir deitado / não consigo dormir deitado | Incapacidade de dormir deitado; a expressão exige contexto e não equivale a insônia genérica. | F4 |
| Insuficiência Cardíaca | enjoo / náusea | Náusea entre as manifestações da insuficiência cardíaca direita. | F4 |
| Arritmia | palpitação / palpitações; coração acelerado / coração dispara; batimentos irregulares / coração batendo irregularmente | Percepção de batimentos fortes, acelerados ou irregulares. | F5 |
| Arritmia | tontura / sensação de tontura; desmaio / desmaiei | Tontura e desmaio são sintomas possíveis. | F5 |
| Arritmia | cansaço / fadiga; dor no peito / dor torácica; desconforto no peito / desconforto torácico; falta de ar / dificuldade para respirar | Cansaço, dor ou desconforto torácico e dificuldade respiratória também são descritos. | F5 |

## Critérios de curadoria

- Cada par expressão–condição aparece uma única vez. A expressão pode aparecer para condições diferentes, pois sintomas não são exclusivos.
- O mapa é um recorte, não uma lista exaustiva. Uma associação ausente não significa impossibilidade clínica; ausência de correspondência não exclui doença.
- Não foram criadas categorias extras nem regras clínicas baseadas somente em nervosismo, duração ou impacto na rotina. Esses dados contextualizam os relatos.
- As variantes são adaptações linguísticas. Por exemplo, “coração dispara” representa coloquialmente a percepção de batimentos acelerados.
- Variantes podem diferir em intensidade e especificidade. O agrupamento simplifica essas diferenças para a atividade e não permite inferir gravidade.

## Algoritmo implementado nesta etapa

O script normaliza caixa, acentos e espaços, procura expressões completas e prioriza a expressão mais longa nos trechos sobrepostos. A contagem ocorre por conceito linguístico, com grupos definidos no dicionário GRUPOS do código. As associações a condições continuam vindo exclusivamente do CSV.

A regra de sugestão atribui um ponto por conceito distinto associado a cada condição e apresenta todas as condições com a maior contagem, explicitando empates. A saída também mostra as expressões e todas as condições pontuadas. Não se trata de probabilidade ou ponderação clínica.

Exemplos de agrupamento: “palpitações” e “coração dispara” não geram dois pontos; dor, desconforto, pressão e aperto no peito pertencem ao mesmo grupo didático. “Fadiga extrema” prevalece sobre “fadiga” no mesmo trecho. Foi incluída uma variação controlada para “desconforto constante no peito”.

Há tratamento limitado de negações locais. “Não tenho falta de ar” é diferente de “não consigo dormir deitado”, que afirma uma dificuldade. Construções complexas permanecem uma limitação, conforme o README.

Essas regras são decisões computacionais do projeto, não recomendações das fontes médicas. O capítulo 10 fundamenta normalização, regras e representação do conhecimento; consulte o [mapeamento didático](../../document/MAPEAMENTO_APOSTILAS_FASE2.md).

## Referências

Consulta realizada em 20/09/2026. Fontes institucionais de informação em saúde; o mapa não foi submetido a validação por profissional de saúde.

- **F1 — Ministério da Saúde.** [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto), seção “Sintomas”. Fundamenta associações peitorais, irradiação para o braço, suor frio e falta de ar.
- **F2 — NHLBI/NIH.** [Heart Attack — Symptoms](https://www.nhlbi.nih.gov/health/heart-attack/symptoms), seção “What are the symptoms of a heart attack?”. Complementa a associação de náusea ao infarto.
- **F3 — NHLBI/NIH.** [Angina (Chest Pain) — Symptoms](https://www.nhlbi.nih.gov/health/angina/symptoms), seção “Common symptoms”. Fundamenta as expressões relacionadas a angina. A fonte aponta a dificuldade de distinguir seus sintomas dos de infarto.
- **F4 — NHLBI/NIH.** [Heart Failure — Symptoms](https://www.nhlbi.nih.gov/health/heart-failure/symptoms). Fundamenta as associações de insuficiência cardíaca, distinguindo manifestações dos lados esquerdo e direito.
- **F5 — NHLBI/NIH.** [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms). Fundamenta as expressões relacionadas a arritmias.
