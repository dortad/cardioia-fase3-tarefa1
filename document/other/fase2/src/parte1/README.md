# Parte 1 - Frases de sintomas + extração de informações

## Status

Parte 1 concluída. O responsável pelo projeto aprovou as saídas, a manutenção dos empates e as limitações descritas neste documento.

## Objetivo

Criar um mapa simples de sintomas e doenças para sugerir diagnósticos básicos a partir de relatos de pacientes.

## Arquivos

- `sintomas_pacientes.txt` — 10 frases simulando relatos clínicos
- `mapa_sintomas_doencas.csv` — associação entre sintomas e doenças
- `FONTES_MAPA.md` — referências e critérios de construção do mapa
- `diagnostico_sintomas.py` — extração por regras e sugestões explicadas
- `test_diagnostico_sintomas.py` — verificação das regras com unittest

## Execução

```bash
python src/parte1/diagnostico_sintomas.py
```

## Origem e elaboração dos relatos

Os dez relatos de `sintomas_pacientes.txt` são **dados sintéticos para fins didáticos**. Não foram coletados de pacientes, prontuários ou entrevistas, nem transcritos de publicações médicas.

A versão atual foi adaptada das dez frases que estavam na versão anterior do próprio arquivo `src/parte1/sintomas_pacientes.txt`, antes da revisão acompanhada pelo responsável pelo projeto. As reformulações foram propostas com apoio de IA (assistente Codex) e aprovadas pelo responsável pelo projeto nesta sessão de trabalho. Foram preservados os sintomas centrais e acrescentadas informações fictícias sobre início, duração e impacto na rotina. A redação também foi ajustada para representar a linguagem de um paciente.

O [enunciado da atividade](../../document/Enunciado.md), na Parte 1, é a referência para o formato: dez frases completas simulando sintomas, com informações sobre quando começaram e como afetam a rotina. Ele também apresenta exemplos de relatos de dor no peito e cansaço. Não há registro de uma fonte externa individual para cada frase original; portanto, não se atribui sua autoria a uma instituição de saúde.

O capítulo 10 das apostilas, **IA que Entende: Processamento de Linguagem Natural Baseado em Regras**, fundamenta o processamento posterior: normalização, reconhecimento de expressões e associação a um mapa de conhecimento. É uma referência metodológica, não a fonte literal dos relatos. Consulte o [mapeamento das apostilas](../../document/MAPEAMENTO_APOSTILAS_FASE2.md) para as seções e páginas pertinentes.

Os textos de saúde reunidos em `document/other/fase1/docs/` possuem suas próprias referências em [FONTES.md](../../document/other/fase1/docs/FONTES.md). Essas referências não devem ser apresentadas como origem destes dez relatos, pois eles não foram extraídos desses documentos.

As situações descritas são simulações para testar a extração de sintomas; não constituem casos clínicos validados. A fundamentação das associações está documentada separadamente em [FONTES_MAPA.md](FONTES_MAPA.md).

## Organização do mapa

O CSV contém 30 linhas de associações e quatro categorias. `Sintoma 1` e `Sintoma 2` representam alternativas de expressão, não sintomas que obrigatoriamente precisam aparecer juntos. Uma expressão pode estar associada a mais de uma condição; repetições do mesmo par expressão–condição foram eliminadas.

## Como o algoritmo funciona

A implementação usa apenas a biblioteca padrão do Python e aplica a abordagem simbólica do capítulo 10.

1. Lê o mapa e valida as três colunas. Arquivos UTF-8 com ou sem BOM são aceitos.
2. Normaliza caixa, acentos e espaços no texto e no mapa.
3. Procura expressões completas com limites de palavra. Há uma regra explícita para admitir “constante” em “desconforto no peito”, como no relato 10.
4. Em trechos sobrepostos, mantém a expressão mais longa: “fadiga extrema” prevalece sobre “fadiga”, usando as associações da expressão específica no CSV.
5. Identifica algumas negações locais, como “não tenho”, “não sinto”, “nego” e “sem”. Pontuação, adversativas e novas afirmações delimitam o escopo. “Não consigo dormir deitado” é uma dificuldade afirmada do mapa.
6. Agrupa variantes em conceitos linguísticos: “palpitações” e “coração dispara”, por exemplo, são contados uma vez. O dicionário GRUPOS no código documenta esses agrupamentos; as condições associadas continuam vindo do CSV.
7. Atribui um ponto por conceito distinto associado a cada condição. Mostra todas as condições pontuadas e suas evidências. Apresenta como sugestões as de maior contagem e preserva todos os empates.

A contagem é uma heurística didática, sem pesos clínicos ou probabilidades. Adicionar um novo Sintoma 1 ao CSV requer definir seu grupo linguístico no código. A ausência de uma condição entre as sugestões não a exclui.

## Verificação desta etapa

Comandos a partir da raiz, usando Python 3.10 ou superior:

```bash
python src/parte1/diagnostico_sintomas.py
python -B src/parte1/test_diagnostico_sintomas.py
```

Os 13 testes passaram na validação da implementação e verificam cobertura dos dez relatos, variantes, acentos, sobreposições, repetições, empates independentes da ordem do mapa, limites de palavra, casos sem correspondência e exemplos de negação.

| Relato | Resultado da regra didática |
|---|---|
| 1 | Empate: Angina, Arritmia e Infarto |
| 2 | Insuficiência Cardíaca |
| 3 | Empate: Angina, Arritmia e Infarto |
| 4 | Insuficiência Cardíaca |
| 5 | Arritmia; duas expressões, um conceito |
| 6 | Arritmia |
| 7 | Infarto |
| 8 | Insuficiência Cardíaca |
| 9 | Empate: Angina e Infarto |
| 10 | Infarto |

Esses resultados verificam o comportamento do programa sobre dados sintéticos; não são acurácia clínica nem diagnósticos de referência. As dez saídas foram revisadas com o responsável pelo projeto, que aprovou manter esse comportamento e encerrar a Parte 1. Os empates dos relatos 1, 3 e 9 são intencionais.

## Limitações

A extração depende de expressões cadastradas e de poucas regras explícitas. Não interpreta de forma geral tempo, intensidade, relação com esforço, histórico médico, ironia ou negações complexas. Os grupos simplificam diferenças linguísticas e clínicas. A escolha da expressão mais longa também torna o resultado sensível ao vocabulário do mapa.

Não é necessário adotar NLP avançado para cumprir a proposta simples do enunciado. O objetivo é apresentar regras compreensíveis, suas evidências e suas limitações.
