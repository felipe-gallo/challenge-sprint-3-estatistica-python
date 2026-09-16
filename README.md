# Sprint 3 - Modelagem Linear

Trabalho da Sprint 3 da matéria **Modelagem Linear para Aprendizado de Máquina**.

Usamos uma base com dados de renda e gasto de 50 famílias. A partir dela, calculamos probabilidades usando a Distribuição Normal e montamos uma regressão linear para analisar a relação entre renda e gasto.

## Integrantes

| Nome | RM |
| --- | ---: |
| Arthur Maziviero Faria | 573928 |
| Jun Uehara | 570537 |
| Felipe de Souza Gallo | 569680 |
| Roberson Reguero Luiz Junior | 573031 |
| Tommaso C. Nagliatti | 572147 |
| Matheus Martins Lacerda | 570843 |

## O que foi feito

- probabilidade de o gasto ficar acima da mediana;
- probabilidade de o gasto ficar entre a média e dois desvios padrão;
- regressão linear do gasto familiar em função da renda;
- gráficos e interpretação dos resultados.

Os principais resultados foram:

- **44,36%** de probabilidade acima da mediana;
- **95,45%** de probabilidade no intervalo média ± 2 desvios;
- **R² de 0,9699** na regressão linear.

## Arquivos principais

- `dados/dados_familias.csv`: base utilizada;
- `src/analise_estatistica.py`: código em Python;
- `notebooks/challenge_sprint_3.ipynb`: versão para o Google Colab;
- `relatorio/Relatório Sprint 3 Modelagem Linear.pdf`: relatório final;
- `resultados/`: gráficos gerados pelo código.

## Como executar no Colab

1. Abra o arquivo `notebooks/challenge_sprint_3.ipynb` no Google Colab.
2. Execute todas as células.
3. Quando aparecer a opção de upload, selecione `dados/dados_familias.csv`.

Também é possível executar o arquivo Python diretamente:

```bash
pip install -r requirements.txt
python src/analise_estatistica.py
```
