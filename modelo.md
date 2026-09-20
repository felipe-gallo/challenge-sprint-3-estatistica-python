# Sprint 3 - Modelagem Linear para Aprendizado de Máquina

FIAP - Aclimação · Ciências da Computação  
Disciplina: Estatística com Python · São Paulo, 2026  
Integrantes e RMs: [integrantes.txt](integrantes.txt)

## 1. Objetivo e base de dados

Analisar o gasto familiar sob a hipótese de Distribuição Normal e ajustar uma Regressão Linear Simples para explicar o gasto em função da renda. A base didática contém 50 famílias, com as variáveis `renda_familiar` e `gasto_familiar`, em reais. `id_familia` identifica cada observação e não participa do modelo.

A análise utiliza Python, pandas, NumPy, SciPy, scikit-learn e Matplotlib. O notebook está preparado para execução no Google Colab.

## 2. Critério de classificação

| Probabilidade | Classificação |
| --- | --- |
| De 0% até 5% | Raro |
| Acima de 5% até 25% | Pouco provável |
| Acima de 25% até 75% | Provável |
| Acima de 75% até 100% | Quase certo |

Essas faixas são critérios adotados pelo projeto. Probabilidades fora de [0, 1] são rejeitadas.

## 3. Probabilidade acima da mediana

A Normal foi parametrizada pela média e pelo desvio padrão amostral do gasto, calculado com `ddof=1`.

```python
gastos = dados['gasto_familiar']
media = gastos.mean()
mediana = gastos.median()
desvio = gastos.std(ddof=1)
prob_acima_mediana = norm.sf(mediana, loc=media, scale=desvio)
```

| Indicador | Resultado |
| --- | ---: |
| Média | R$ 2.011,12 |
| Mediana | R$ 2.127,00 |
| Desvio padrão amostral | R$ 817,21 |
| P(X > mediana) | 44,3619% |
| Classificação | Provável |

A probabilidade é aproximadamente 44,36%. Ela difere de 50% porque o ponto de corte é a mediana da amostra, enquanto a distribuição teórica é centrada na média amostral. Não se trata da proporção empírica de registros acima da mediana.

## 4. Probabilidade no intervalo média ± 2s

```python
limite_inferior = media - 2 * desvio
limite_superior = media + 2 * desvio
prob_intervalo = (
    norm.cdf(limite_superior, loc=media, scale=desvio)
    - norm.cdf(limite_inferior, loc=media, scale=desvio)
)
```

| Indicador | Resultado |
| --- | ---: |
| Limite inferior | R$ 376,69 |
| Limite superior | R$ 3.645,55 |
| Probabilidade | 95,4500% |
| Classificação | Quase certo |

Sob a hipótese Normal, o intervalo concentra aproximadamente 95,45% da probabilidade. Esse resultado corresponde à regra de dois desvios padrão da Normal; não comprova que os dados seguem essa distribuição.

![Distribuição Normal ajustada ao gasto familiar](resultados/distribuicao_normal.png)

## 5. Regressão Linear Simples

O gasto é a variável dependente e a renda é a variável explicativa. O ajuste usa mínimos quadrados.

```python
X = dados[['renda_familiar']]
y = dados['gasto_familiar']
modelo = LinearRegression().fit(X, y)
previsoes = modelo.predict(X)
r2 = r2_score(y, previsoes)
rmse = np.sqrt(mean_squared_error(y, previsoes))
```

**Equação estimada:** gasto = 207,9033 + 0,2973 × renda.

| Parâmetro ou métrica | Estimativa |
| --- | ---: |
| Intercepto | 207,9033 |
| Coeficiente angular | 0,2973 |
| R² | 0,9699 |
| RMSE | R$ 140,36 |

O intercepto corresponde ao gasto previsto quando a renda é zero. Como esse valor está fora da faixa observada, sua interpretação é matemática e envolve extrapolação.

Cada R$ 1,00 adicional de renda está associado a cerca de R$ 0,2973 de gasto adicional previsto. Usando o coeficiente sem arredondamento, R$ 1.000,00 adicionais correspondem a aproximadamente R$ 297,29.

O R² indica que cerca de 96,99% da variação dos gastos é explicada linearmente pela renda nesta amostra. O RMSE representa a magnitude típica dos erros dentro da própria amostra. Não foi realizada avaliação em um conjunto independente, e associação não demonstra causalidade.

![Observações e reta de regressão](resultados/regressao_linear.png)

## 6. Execução no Google Colab

1. Abra `notebooks/challenge_sprint_3.ipynb` no Google Colab.
2. Selecione **Ambiente de execução → Executar tudo**.
3. A primeira célula baixa automaticamente os arquivos necessários, caso não estejam presentes. É necessário acesso à internet.
4. Confira os resultados e os gráficos. A última célula executa a suíte completa de testes.

O download está fixado na versão `cccec5561bda4cf37627e7f40ef678263ff4c1b6` do repositório, que contém a base, o módulo estatístico e os cinco testes originais. As seis verificações adicionais estão no próprio notebook.

## 7. Validação automatizada

A última célula reúne todos os testes existentes em `tests/` e seis testes do notebook. Verifica a base, as estatísticas descritivas, as probabilidades, os limites das classificações, entradas inválidas, os coeficientes e métricas da regressão e a consistência com o módulo Python.

**Resultado: 11 testes aprovados, sem falhas.** O resultado da execução está salvo na última célula do notebook. A execução é interrompida em caso de falha. A validação foi realizada em ambiente Python local; o notebook inclui preparação para Google Colab.

## 8. Conclusão

A probabilidade de superar a mediana foi classificada como provável, e a de permanecer no intervalo média ± 2s foi classificada como quase certa. A regressão apresentou associação linear forte entre renda e gasto, com R² de aproximadamente 0,9699 na amostra analisada.

A análise mostra como a estatística descreve a incerteza e sustenta modelos preditivos interpretáveis. As conclusões dependem da hipótese Normal e da base didática; não demonstram causalidade nem desempenho fora da amostra.

## Referências e arquivos

- Base do projeto: `dados/dados_familias.csv`.
- Código: `src/analise_estatistica.py`.
- Notebook: `notebooks/challenge_sprint_3.ipynb`.
- Testes originais: `tests/test_analise_estatistica.py`.
- Integrantes: `integrantes.txt`.
- Alura: Cálculo da probabilidade da distribuição normal com quaisquer valores de média e desvio padrão; Estatística com Python: Correlação e Regressão. Referências informadas na versão original do trabalho.
- Repositório: https://github.com/felipe-gallo/challenge-sprint-3-estatistica-python
