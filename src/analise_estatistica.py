"""Análise estatística da Challenge Sprint 3.

Compatível com execução local e com o Google Colab.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


COLUNA_RENDA = "renda_familiar"
COLUNA_GASTO = "gasto_familiar"


def classificar_evento(probabilidade: float) -> str:
    """Classifica uma probabilidade conforme faixas definidas no projeto."""
    if not 0 <= probabilidade <= 1:
        raise ValueError("A probabilidade deve estar entre 0 e 1.")
    if probabilidade <= 0.05:
        return "raro"
    if probabilidade <= 0.25:
        return "pouco provável"
    if probabilidade <= 0.75:
        return "provável"
    return "quase certo"


def carregar_dados(caminho: str | Path) -> pd.DataFrame:
    """Carrega e valida a base de famílias."""
    caminho = Path(caminho)
    if not caminho.exists():
        alternativas = [Path("dados_familias.csv"), Path("/content/dados_familias.csv")]
        caminho = next((item for item in alternativas if item.exists()), caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            "Base não encontrada. No Colab, envie dados_familias.csv antes da execução."
        )

    dados = pd.read_csv(caminho)
    colunas_obrigatorias = {COLUNA_RENDA, COLUNA_GASTO}
    ausentes = colunas_obrigatorias.difference(dados.columns)
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(ausentes)}")
    if dados[list(colunas_obrigatorias)].isna().any().any():
        raise ValueError("A base contém valores ausentes nas variáveis analisadas.")
    if len(dados) < 2:
        raise ValueError("A análise requer pelo menos duas observações.")
    return dados


def calcular_probabilidades(dados: pd.DataFrame) -> dict[str, float | str]:
    """Calcula as probabilidades solicitadas sob a hipótese Normal."""
    gastos = dados[COLUNA_GASTO]
    media = float(gastos.mean())
    mediana = float(gastos.median())
    desvio_padrao = float(gastos.std(ddof=1))

    prob_acima_mediana = float(norm.sf(mediana, loc=media, scale=desvio_padrao))
    limite_inferior = media - 2 * desvio_padrao
    limite_superior = media + 2 * desvio_padrao
    prob_intervalo = float(
        norm.cdf(limite_superior, loc=media, scale=desvio_padrao)
        - norm.cdf(limite_inferior, loc=media, scale=desvio_padrao)
    )

    return {
        "media": media,
        "mediana": mediana,
        "desvio_padrao": desvio_padrao,
        "probabilidade_acima_mediana": prob_acima_mediana,
        "classificacao_acima_mediana": classificar_evento(prob_acima_mediana),
        "limite_inferior_2s": limite_inferior,
        "limite_superior_2s": limite_superior,
        "probabilidade_intervalo_2s": prob_intervalo,
        "classificacao_intervalo_2s": classificar_evento(prob_intervalo),
    }


def ajustar_regressao(dados: pd.DataFrame) -> tuple[LinearRegression, dict[str, float]]:
    """Ajusta gasto familiar em função da renda familiar."""
    x = dados[[COLUNA_RENDA]]
    y = dados[COLUNA_GASTO]
    modelo = LinearRegression()
    modelo.fit(x, y)
    previsoes = modelo.predict(x)

    metricas = {
        "intercepto": float(modelo.intercept_),
        "coeficiente_angular": float(modelo.coef_[0]),
        "r_quadrado": float(r2_score(y, previsoes)),
        "rmse": float(np.sqrt(mean_squared_error(y, previsoes))),
    }
    return modelo, metricas


def gerar_grafico_distribuicao(
    dados: pd.DataFrame, resultados: dict[str, float | str], destino: Path
) -> None:
    """Gera a curva Normal com mediana e intervalo de dois desvios."""
    media = float(resultados["media"])
    desvio = float(resultados["desvio_padrao"])
    mediana = float(resultados["mediana"])
    inferior = float(resultados["limite_inferior_2s"])
    superior = float(resultados["limite_superior_2s"])

    eixo_x = np.linspace(media - 4 * desvio, media + 4 * desvio, 800)
    densidade = norm.pdf(eixo_x, loc=media, scale=desvio)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(eixo_x, densidade, color="#174A7E", linewidth=2.4, label="Distribuição Normal ajustada")
    ax.fill_between(
        eixo_x,
        densidade,
        where=(eixo_x >= inferior) & (eixo_x <= superior),
        color="#5CB8B2",
        alpha=0.38,
        label="Intervalo média ± 2s",
    )
    ax.fill_between(
        eixo_x,
        densidade,
        where=eixo_x >= mediana,
        color="#F2A65A",
        alpha=0.28,
        label="Área acima da mediana",
    )
    ax.axvline(media, color="#174A7E", linestyle="--", label=f"Média = R$ {media:,.2f}")
    ax.axvline(mediana, color="#B45309", linestyle=":", label=f"Mediana = R$ {mediana:,.2f}")
    ax.set_title("Distribuição Normal do gasto familiar")
    ax.set_xlabel("Gasto familiar (R$)")
    ax.set_ylabel("Densidade de probabilidade")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(destino, dpi=180, bbox_inches="tight")
    plt.close(fig)


def gerar_grafico_regressao(
    dados: pd.DataFrame, modelo: LinearRegression, destino: Path
) -> None:
    """Gera o gráfico de dispersão e a reta de regressão ajustada."""
    x = dados[COLUNA_RENDA].to_numpy()
    y = dados[COLUNA_GASTO].to_numpy()
    ordem = np.argsort(x)
    x_ordenado = x[ordem]
    y_previsto = modelo.predict(x_ordenado.reshape(-1, 1))

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.scatter(x, y, color="#5CB8B2", edgecolor="white", s=58, label="Famílias observadas")
    ax.plot(x_ordenado, y_previsto, color="#C33C54", linewidth=2.5, label="Reta ajustada")
    ax.set_title("Regressão linear: gasto familiar em função da renda")
    ax.set_xlabel("Renda familiar (R$)")
    ax.set_ylabel("Gasto familiar (R$)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(destino, dpi=180, bbox_inches="tight")
    plt.close(fig)


def imprimir_resultados(
    probabilidades: dict[str, float | str], regressao: dict[str, float]
) -> None:
    """Exibe resultados de forma organizada no terminal ou no Colab."""
    print("\n1) PROBABILIDADE ACIMA DA MEDIANA")
    print(f"Mediana do gasto: R$ {probabilidades['mediana']:,.2f}")
    print(f"Probabilidade: {probabilidades['probabilidade_acima_mediana']:.2%}")
    print(f"Classificação: {probabilidades['classificacao_acima_mediana']}")

    print("\n2) PROBABILIDADE NO INTERVALO MÉDIA ± 2s")
    print(f"Média: R$ {probabilidades['media']:,.2f}")
    print(f"Desvio padrão amostral: R$ {probabilidades['desvio_padrao']:,.2f}")
    print(
        "Intervalo: "
        f"[R$ {probabilidades['limite_inferior_2s']:,.2f}; "
        f"R$ {probabilidades['limite_superior_2s']:,.2f}]"
    )
    print(f"Probabilidade: {probabilidades['probabilidade_intervalo_2s']:.2%}")
    print(f"Classificação: {probabilidades['classificacao_intervalo_2s']}")

    print("\n3) REGRESSÃO LINEAR")
    print(
        "Equação: gasto_familiar = "
        f"{regressao['intercepto']:.4f} + "
        f"{regressao['coeficiente_angular']:.4f} × renda_familiar"
    )
    print(f"R²: {regressao['r_quadrado']:.4f}")
    print(f"RMSE: R$ {regressao['rmse']:,.2f}")


def executar(caminho_csv: str | Path, pasta_resultados: str | Path) -> dict[str, dict]:
    """Executa a análise completa e salva os gráficos."""
    dados = carregar_dados(caminho_csv)
    probabilidades = calcular_probabilidades(dados)
    modelo, regressao = ajustar_regressao(dados)

    pasta_resultados = Path(pasta_resultados)
    pasta_resultados.mkdir(parents=True, exist_ok=True)
    gerar_grafico_distribuicao(
        dados, probabilidades, pasta_resultados / "distribuicao_normal.png"
    )
    gerar_grafico_regressao(dados, modelo, pasta_resultados / "regressao_linear.png")
    imprimir_resultados(probabilidades, regressao)
    return {"probabilidades": probabilidades, "regressao": regressao}


def main() -> None:
    parser = argparse.ArgumentParser(description="Challenge Sprint 3 - Estatística")
    parser.add_argument(
        "--arquivo",
        default="dados/dados_familias.csv",
        help="Caminho do arquivo CSV",
    )
    parser.add_argument(
        "--saida",
        default="resultados",
        help="Pasta em que os gráficos serão salvos",
    )
    argumentos = parser.parse_args()
    executar(argumentos.arquivo, argumentos.saida)


if __name__ == "__main__":
    main()

