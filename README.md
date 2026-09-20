# Sprint 3 - Modelagem Linear

Trabalho da Sprint 3 da matéria **Modelagem Linear para Aprendizado de Máquina**.

Usamos uma base com dados de renda e gasto de 50 famílias. A partir dela, calculamos probabilidades usando a Distribuição Normal e montamos uma regressão linear para analisar a relação entre renda e gasto.

## Integrantes

Consulte `integrantes.txt`.

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

Abra `notebooks/challenge_sprint_3.ipynb` no Google Colab e selecione **Executar tudo**. A primeira célula obtém automaticamente os arquivos necessários do repositório, em uma versão fixa para reproduzir os resultados. É necessário acesso à internet. A última célula executa todos os testes do projeto e dos resultados do notebook.

Localmente, instale `requirements.txt` e execute o notebook na pasta do projeto.

O relatório preenchido está em `modelo.md`; o PDF está em `relatorio/`; os nomes e RMs estão em `integrantes.txt`.
