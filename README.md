# Challenge Sprint 3 - Estatística com Python

Projeto acadêmico desenvolvido para a Challenge Sprint 3 do 2º semestre. A entrega analisa uma variável aleatória sob a hipótese de Distribuição Normal e aplica Regressão Linear Simples em Python.

## Integrantes

| Nome completo | RM |
| --- | ---: |
| Arthur Maziviero Faria | 573928 |
| Jun Uehara | 570537 |
| Felipe de Souza Gallo | 569680 |
| Roberson Reguero Luiz Junior | 573031 |
| Tommaso C. Nagliatti | 572147 |
| Matheus Martins Lacerda | 570843 |

## Objetivos

- calcular a probabilidade de o gasto familiar ficar acima da mediana;
- calcular a probabilidade de o gasto familiar ficar no intervalo média ± 2 desvios padrão;
- ajustar uma regressão linear entre renda familiar e gasto familiar;
- apresentar código, gráfico, resultados e interpretações em um relatório PDF.

## Resultados

| Análise | Resultado | Classificação |
| --- | ---: | --- |
| Probabilidade de gasto acima da mediana | 44,36% | Provável |
| Probabilidade no intervalo média ± 2s | 95,45% | Quase certo |
| Regressão Linear | `gasto = 207,9033 + 0,2973 × renda` | R² = 0,9699 |

As classificações seguem as faixas definidas no projeto: raro (até 5%), pouco provável (acima de 5% até 25%), provável (acima de 25% até 75%) e quase certo (acima de 75%).

## Estrutura

```text
.
├── dados/
│   └── dados_familias.csv
├── src/
│   └── analise_estatistica.py
├── notebooks/
│   └── challenge_sprint_3.ipynb
├── resultados/
│   ├── distribuicao_normal.png
│   └── regressao_linear.png
├── relatorio/
│   └── relatorio_challenge_sprint_3.pdf
├── tests/
│   └── test_analise_estatistica.py
├── requirements.txt
└── README.md
```

## Execução no Google Colab

1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Selecione **Arquivo > Fazer upload de notebook**.
3. Envie `notebooks/challenge_sprint_3.ipynb`.
4. Selecione **Ambiente de execução > Executar tudo**.
5. Quando solicitado, envie `dados/dados_familias.csv`.

O notebook executa todos os cálculos, apresenta as interpretações e exibe os gráficos. O arquivo `src/analise_estatistica.py` contém a mesma análise em formato Python, conforme a exigência de entrega.

## Execução do arquivo Python

```bash
pip install -r requirements.txt
python src/analise_estatistica.py
```

Os gráficos são gravados na pasta `resultados/`.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Arquivos para envio no Portal

- `relatorio/relatorio_challenge_sprint_3.pdf`;
- `dados/dados_familias.csv`;
- `src/analise_estatistica.py`.

O notebook `.ipynb` pode ser enviado como arquivo adicional se o Portal permitir. O enunciado determina que os arquivos sejam anexados diretamente, não apenas compartilhados por link.

## Referências

- [Cálculo da probabilidade da distribuição normal - Alura](https://cursos.alura.com.br/forum/topico-calculo-da-probabilidade-da-distribuicao-normal-com-quaisquer-valores-de-media-e-desvio-padrao-195298)
- [Estatística com Python: Correlação e Regressão - Alura](https://www.alura.com.br/conteudo/estatistica-correlacao-regressao)
