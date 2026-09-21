# Sprint 3 - Modelagem Linear

Projeto acadêmico de Estatística com Python desenvolvido a partir dos dados de renda e gasto de 50 famílias. A análise foi preparada para execução no Google Colab.

## Objetivo

O projeto aplica conceitos de Distribuição Normal e Regressão Linear Simples. Os cálculos avaliam a probabilidade de o gasto superar a mediana, a probabilidade de o gasto permanecer no intervalo da média mais ou menos dois desvios padrão e a relação entre renda e gasto familiar.

## Código

O arquivo src/analise_estatistica.py concentra a análise principal. O código está organizado em funções para carregar e validar os dados, calcular as probabilidades, classificar os eventos, ajustar a regressão e gerar os gráficos.

Foram utilizadas as bibliotecas pandas, NumPy, SciPy, Matplotlib e scikit-learn.

## Estrutura do projeto

- dados/dados_familias.csv - base de dados das famílias
- src/analise_estatistica.py - código completo da análise
- notebooks/challenge_sprint_3.ipynb - notebook para o Google Colab
- resultados - gráficos gerados pelo código
- relatorio/Relatório Sprint 3 Modelagem Linear.pdf - relatório científico em formato ABNT

## Execução

No Google Colab, abra o arquivo challenge_sprint_3.ipynb, execute todas as células e selecione dados_familias.csv quando solicitado. O código também pode ser executado diretamente pelo arquivo analise_estatistica.py.

## Resultados principais

- Probabilidade acima da mediana: 44,36%
- Probabilidade no intervalo da média mais ou menos dois desvios padrão: 95,45%
- Coeficiente de determinação da regressão: R² de 0,9699

## Integrantes

- Arthur Maziviero Faria - RM 573928
- Jun Uehara - RM 570537
- Felipe de Souza Gallo - RM 569680
- Roberson Reguero Luiz Junior - RM 573031
- Tommaso Conceição Nagliatti - RM 572147
- Matheus Martins Lacerda - RM 570843
