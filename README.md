# Sprint 3 - Modelagem Linear

Projeto acadêmico de Estatística com Python desenvolvido para analisar dados de renda e gasto de 50 famílias. O trabalho combina Distribuição Normal e Regressão Linear Simples e pode ser executado no Google Colab.

## Integrantes

- Arthur Maziviero Faria - RM 573928
- Jun Uehara - RM 570537
- Felipe de Souza Gallo - RM 569680
- Roberson Reguero Luiz Junior - RM 573031
- Tommaso Conceição Nagliatti - RM 572147
- Matheus Martins Lacerda - RM 570843

## Conteúdo do projeto

- `relatorio/Relatório Sprint 3 Modelagem Linear.pdf`: relatório científico em formato ABNT;
- `dados/dados_familias.csv`: base de dados utilizada na análise;
- `src/analise_estatistica.py`: código completo em Python;
- `notebooks/challenge_sprint_3.ipynb`: notebook preparado para o Google Colab;
- `resultados/`: gráficos da Distribuição Normal e da Regressão Linear.

## Como executar no Google Colab

Abra o notebook `challenge_sprint_3.ipynb`, selecione **Executar tudo** e envie o arquivo `dados_familias.csv` quando solicitado.

Também é possível enviar `analise_estatistica.py` e `dados_familias.csv` para o Colab e executar:

```python
%run analise_estatistica.py --arquivo dados_familias.csv
```

## Resultados principais

- Probabilidade de o gasto superar a mediana: 44,36%;
- Probabilidade no intervalo da média mais ou menos dois desvios padrão: 95,45%;
- Coeficiente de determinação da regressão: R² = 0,9699.
