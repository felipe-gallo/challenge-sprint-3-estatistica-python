"""Gera o relatório PDF da Challenge Sprint 3."""

from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from analise_estatistica import ajustar_regressao, calcular_probabilidades, carregar_dados


RAIZ = Path(__file__).resolve().parents[1]
COR_PRIMARIA = colors.HexColor("#174A7E")
COR_SECUNDARIA = colors.HexColor("#5CB8B2")
COR_DESTAQUE = colors.HexColor("#C33C54")
COR_TEXTO = colors.HexColor("#25313C")
COR_CLARA = colors.HexColor("#EAF2F8")
INTEGRANTES = [
    ("Arthur Maziviero Faria", "573928"),
    ("Jun Uehara", "570537"),
    ("Felipe de Souza Gallo", "569680"),
    ("Roberson Reguero Luiz Junior", "573031"),
    ("Tommaso C. Nagliatti", "572147"),
    ("Matheus Martins Lacerda", "570843"),
]


def moeda(valor: float) -> str:
    """Formata valor numérico no padrão brasileiro."""
    formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatado}"


def registrar_fontes() -> tuple[str, str]:
    """Registra Arial quando disponível e retorna fontes normal e negrito."""
    fonte_normal = Path("C:/Windows/Fonts/arial.ttf")
    fonte_negrito = Path("C:/Windows/Fonts/arialbd.ttf")
    if fonte_normal.exists() and fonte_negrito.exists():
        pdfmetrics.registerFont(TTFont("ArialProjeto", str(fonte_normal)))
        pdfmetrics.registerFont(TTFont("ArialProjetoBold", str(fonte_negrito)))
        return "ArialProjeto", "ArialProjetoBold"
    return "Helvetica", "Helvetica-Bold"


def criar_estilos(fonte: str, fonte_negrito: str) -> dict[str, ParagraphStyle]:
    estilos_base = getSampleStyleSheet()
    return {
        "capa": ParagraphStyle(
            "Capa",
            parent=estilos_base["Title"],
            fontName=fonte_negrito,
            fontSize=26,
            leading=31,
            textColor=COR_PRIMARIA,
            alignment=TA_LEFT,
            spaceAfter=18,
        ),
        "subcapa": ParagraphStyle(
            "Subcapa",
            parent=estilos_base["Normal"],
            fontName=fonte,
            fontSize=13,
            leading=19,
            textColor=COR_TEXTO,
        ),
        "h1": ParagraphStyle(
            "H1Projeto",
            parent=estilos_base["Heading1"],
            fontName=fonte_negrito,
            fontSize=18,
            leading=22,
            textColor=COR_PRIMARIA,
            spaceBefore=8,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "H2Projeto",
            parent=estilos_base["Heading2"],
            fontName=fonte_negrito,
            fontSize=13,
            leading=17,
            textColor=COR_DESTAQUE,
            spaceBefore=9,
            spaceAfter=7,
        ),
        "corpo": ParagraphStyle(
            "CorpoProjeto",
            parent=estilos_base["BodyText"],
            fontName=fonte,
            fontSize=10.3,
            leading=15.2,
            textColor=COR_TEXTO,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "nota": ParagraphStyle(
            "NotaProjeto",
            parent=estilos_base["BodyText"],
            fontName=fonte,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#4B5B68"),
            spaceAfter=6,
        ),
        "codigo": ParagraphStyle(
            "CodigoProjeto",
            parent=estilos_base["Code"],
            fontName="Courier",
            fontSize=7.6,
            leading=10.2,
            leftIndent=8,
            rightIndent=8,
            borderColor=colors.HexColor("#D6E1EA"),
            borderWidth=0.6,
            borderPadding=7,
            backColor=colors.HexColor("#F6F8FA"),
            textColor=colors.HexColor("#1F2933"),
            spaceBefore=4,
            spaceAfter=9,
        ),
        "rodape": ParagraphStyle(
            "RodapeProjeto",
            parent=estilos_base["Normal"],
            fontName=fonte,
            fontSize=8,
            textColor=colors.HexColor("#687986"),
            alignment=TA_CENTER,
        ),
    }


def codigo(texto: str, estilo: ParagraphStyle) -> Paragraph:
    seguro = html.escape(texto).replace(" ", "&nbsp;").replace("\n", "<br/>")
    return Paragraph(seguro, estilo)


def tabela_resultados(linhas: list[list[str]], fonte: str, fonte_negrito: str) -> Table:
    tabela = Table(linhas, colWidths=[6.6 * cm, 9.0 * cm], repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COR_PRIMARIA),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), fonte_negrito),
                ("FONTNAME", (0, 1), (-1, -1), fonte),
                ("FONTSIZE", (0, 0), (-1, -1), 9.3),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_CLARA]),
                ("LINEBELOW", (0, 0), (-1, 0), 1, COR_PRIMARIA),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D5DF")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return tabela


def desenhar_pagina(canvas, documento) -> None:
    canvas.saveState()
    largura, altura = A4
    canvas.setStrokeColor(colors.HexColor("#D6E1EA"))
    canvas.line(2 * cm, 1.45 * cm, largura - 2 * cm, 1.45 * cm)
    canvas.setFillColor(colors.HexColor("#687986"))
    canvas.setFont(documento.fonte_rodape, 8)
    canvas.drawString(2 * cm, 1.0 * cm, "Challenge Sprint 3 - Estatística com Python")
    canvas.drawRightString(largura - 2 * cm, 1.0 * cm, f"Página {documento.page}")
    canvas.restoreState()


def gerar_relatorio(destino: Path) -> None:
    fonte, fonte_negrito = registrar_fontes()
    estilos = criar_estilos(fonte, fonte_negrito)
    dados = carregar_dados(RAIZ / "dados" / "dados_familias.csv")
    probabilidades = calcular_probabilidades(dados)
    _, regressao = ajustar_regressao(dados)

    destino.parent.mkdir(parents=True, exist_ok=True)
    documento = SimpleDocTemplate(
        str(destino),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Challenge Sprint 3 - Estatística com Python",
        author=", ".join(nome for nome, _ in INTEGRANTES),
        subject="Distribuição Normal e Regressão Linear",
    )
    documento.fonte_rodape = fonte
    historia = []

    # Capa
    historia.extend(
        [
            Spacer(1, 3.0 * cm),
            Paragraph("CHALLENGE SPRINT 3", estilos["subcapa"]),
            Spacer(1, 0.25 * cm),
            Paragraph("Estatística com Python", estilos["capa"]),
            Paragraph(
                "Distribuição Normal, probabilidades e modelagem com Regressão Linear",
                estilos["subcapa"],
            ),
            Spacer(1, 1.5 * cm),
            Table(
                [
                    ["SEMESTRE", "2º semestre"],
                    ["AMBIENTE", "Google Colab / Python"],
                    ["BASE", "Renda e gasto de 50 famílias"],
                    ["INTEGRANTES", f"{INTEGRANTES[0][0]} - RM {INTEGRANTES[0][1]}"],
                    ["", f"{INTEGRANTES[1][0]} - RM {INTEGRANTES[1][1]}"],
                    ["", f"{INTEGRANTES[2][0]} - RM {INTEGRANTES[2][1]}"],
                    ["", f"{INTEGRANTES[3][0]} - RM {INTEGRANTES[3][1]}"],
                    ["", f"{INTEGRANTES[4][0]} - RM {INTEGRANTES[4][1]}"],
                    ["", f"{INTEGRANTES[5][0]} - RM {INTEGRANTES[5][1]}"],
                ],
                colWidths=[4.0 * cm, 11.4 * cm],
                style=TableStyle(
                    [
                        ("FONTNAME", (0, 0), (0, -1), fonte_negrito),
                        ("FONTNAME", (1, 0), (1, -1), fonte),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("TEXTCOLOR", (0, 0), (0, -1), COR_PRIMARIA),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.45, colors.HexColor("#D6E1EA")),
                        ("TOPPADDING", (0, 0), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                    ]
                ),
            ),
            Spacer(1, 1.2 * cm),
            Paragraph("Relatório técnico", estilos["subcapa"]),
            Paragraph("2026", estilos["subcapa"]),
            PageBreak(),
        ]
    )

    # Visão geral
    historia.extend(
        [
            Paragraph("1. Objetivo e visão geral", estilos["h1"]),
            Paragraph(
                "Este trabalho analisa a variável aleatória <b>gasto familiar</b> sob a hipótese de que ela segue uma Distribuição Normal. Em seguida, ajusta uma Regressão Linear Simples para explicar o gasto familiar a partir da renda familiar. Todo o procedimento foi desenvolvido em Python e estruturado para execução no Google Colab.",
                estilos["corpo"],
            ),
            Paragraph("Resultados principais", estilos["h2"]),
            tabela_resultados(
                [
                    ["Indicador", "Resultado"],
                    ["Probabilidade acima da mediana", f"{probabilidades['probabilidade_acima_mediana']:.2%} - provável"],
                    ["Probabilidade em média ± 2s", f"{probabilidades['probabilidade_intervalo_2s']:.2%} - quase certo"],
                    ["Equação estimada", f"gasto = {regressao['intercepto']:.4f} + {regressao['coeficiente_angular']:.4f} × renda"],
                    ["Coeficiente de determinação", f"R² = {regressao['r_quadrado']:.4f}"],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.35 * cm),
            Paragraph("Base de dados", estilos["h2"]),
            Paragraph(
                "A base contém 50 famílias e duas variáveis monetárias: renda familiar e gasto familiar. Os valores reproduzem o conjunto didático apresentado no conteúdo de correlação e regressão da Alura indicado no enunciado. Um identificador foi acrescentado apenas para diferenciar os registros.",
                estilos["corpo"],
            ),
            tabela_resultados(
                [
                    ["Variável", "Descrição"],
                    ["renda_familiar", "Renda total observada para cada família, em reais."],
                    ["gasto_familiar", "Gasto total observado para cada família, em reais."],
                    ["id_familia", "Identificador sequencial sem papel no modelo."],
                ],
                fonte,
                fonte_negrito,
            ),
            Paragraph("Critério de classificação dos eventos", estilos["h2"]),
            Paragraph(
                "Foram adotadas faixas explícitas: raro para probabilidade de até 5%; pouco provável acima de 5% e até 25%; provável acima de 25% e até 75%; e quase certo acima de 75%.",
                estilos["corpo"],
            ),
            PageBreak(),
        ]
    )

    # Exercício 1
    historia.extend(
        [
            Paragraph("2. Probabilidade acima da mediana", estilos["h1"]),
            Paragraph(
                "A mediana divide os dados observados em duas metades. Como o exercício solicita uma probabilidade baseada em uma Distribuição Normal parametrizada com a média e o desvio padrão amostrais, calculamos a área à direita da mediana amostral usando a função de sobrevivência da Normal.",
                estilos["corpo"],
            ),
            Paragraph("Código utilizado", estilos["h2"]),
            codigo(
                "gastos = dados['gasto_familiar']\n"
                "media = gastos.mean()\n"
                "mediana = gastos.median()\n"
                "desvio = gastos.std(ddof=1)\n"
                "prob_acima_mediana = norm.sf(\n"
                "    mediana, loc=media, scale=desvio\n"
                ")",
                estilos["codigo"],
            ),
            tabela_resultados(
                [
                    ["Cálculo", "Resultado"],
                    ["Mediana amostral", moeda(float(probabilidades["mediana"]))],
                    ["Média usada na Normal", moeda(float(probabilidades["media"]))],
                    ["Desvio padrão amostral", moeda(float(probabilidades["desvio_padrao"]))],
                    ["P(X > mediana)", f"{probabilidades['probabilidade_acima_mediana']:.4%}"],
                    ["Classificação", "Provável"],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.35 * cm),
            Paragraph("Interpretação", estilos["h2"]),
            Paragraph(
                "A probabilidade de um gasto selecionado ao acaso ultrapassar a mediana de R$ 2.127,00 é de aproximadamente <b>44,36%</b>. O evento é classificado como <b>provável</b>. O valor não precisa ser exatamente 50%: a mediana usada é a da amostra, enquanto a curva Normal é definida pela média e pelo desvio padrão estimados. Como média e mediana amostrais diferem, a área calculada também se afasta de 50%.",
                estilos["corpo"],
            ),
            Image(str(RAIZ / "resultados" / "distribuicao_normal.png"), width=16.3 * cm, height=8.9 * cm),
            Paragraph("Figura 1 - Distribuição Normal ajustada ao gasto familiar.", estilos["nota"]),
            PageBreak(),
        ]
    )

    # Exercício 2
    historia.extend(
        [
            Paragraph("3. Probabilidade no intervalo média ± 2s", estilos["h1"]),
            Paragraph(
                "O segundo evento corresponde à faixa compreendida entre dois desvios padrão abaixo e dois desvios padrão acima da média. Para uma Normal, a probabilidade é obtida subtraindo a função de distribuição acumulada no limite inferior da função acumulada no limite superior.",
                estilos["corpo"],
            ),
            Paragraph("Código utilizado", estilos["h2"]),
            codigo(
                "limite_inferior = media - 2 * desvio\n"
                "limite_superior = media + 2 * desvio\n"
                "prob_intervalo = (\n"
                "    norm.cdf(limite_superior, loc=media, scale=desvio)\n"
                "    - norm.cdf(limite_inferior, loc=media, scale=desvio)\n"
                ")",
                estilos["codigo"],
            ),
            tabela_resultados(
                [
                    ["Cálculo", "Resultado"],
                    ["Média", moeda(float(probabilidades["media"]))],
                    ["Desvio padrão amostral (s)", moeda(float(probabilidades["desvio_padrao"]))],
                    ["Limite inferior (média - 2s)", moeda(float(probabilidades["limite_inferior_2s"]))],
                    ["Limite superior (média + 2s)", moeda(float(probabilidades["limite_superior_2s"]))],
                    ["Probabilidade no intervalo", f"{probabilidades['probabilidade_intervalo_2s']:.4%}"],
                    ["Classificação", "Quase certo"],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.35 * cm),
            Paragraph("Interpretação", estilos["h2"]),
            Paragraph(
                "O intervalo vai de R$ 376,69 a R$ 3.645,55 e concentra aproximadamente <b>95,45%</b> da probabilidade do modelo Normal. O evento é classificado como <b>quase certo</b>. Esse resultado coincide com a regra empírica da Normal segundo a qual cerca de 95% dos valores ficam a até dois desvios padrão da média.",
                estilos["corpo"],
            ),
            Paragraph(
                "A faixa sombreada em azul na Figura 1 representa esse intervalo. A área laranja evidencia, ao mesmo tempo, o evento acima da mediana usado no primeiro exercício.",
                estilos["corpo"],
            ),
            PageBreak(),
        ]
    )

    # Exercício 3
    historia.extend(
        [
            Paragraph("4. Modelagem com Regressão Linear", estilos["h1"]),
            Paragraph(
                "Foi ajustada uma Regressão Linear Simples pelo método dos mínimos quadrados. A variável dependente é o gasto familiar e a variável explicativa é a renda familiar. O modelo assume a forma gasto = intercepto + coeficiente × renda + erro.",
                estilos["corpo"],
            ),
            Paragraph("Código utilizado", estilos["h2"]),
            codigo(
                "X = dados[['renda_familiar']]\n"
                "y = dados['gasto_familiar']\n"
                "modelo = LinearRegression()\n"
                "modelo.fit(X, y)\n"
                "previsoes = modelo.predict(X)\n"
                "r2 = r2_score(y, previsoes)\n"
                "rmse = np.sqrt(mean_squared_error(y, previsoes))",
                estilos["codigo"],
            ),
            tabela_resultados(
                [
                    ["Parâmetro ou métrica", "Estimativa"],
                    ["Intercepto", f"{regressao['intercepto']:.4f}"],
                    ["Coeficiente da renda", f"{regressao['coeficiente_angular']:.4f}"],
                    ["R²", f"{regressao['r_quadrado']:.4f}"],
                    ["RMSE", moeda(regressao["rmse"])],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.35 * cm),
            Paragraph(
                f"A reta estimada é: <b>gasto = {regressao['intercepto']:.4f} + {regressao['coeficiente_angular']:.4f} × renda</b>.",
                estilos["corpo"],
            ),
            Image(str(RAIZ / "resultados" / "regressao_linear.png"), width=16.3 * cm, height=9.45 * cm),
            Paragraph("Figura 2 - Observações e reta de Regressão Linear ajustada.", estilos["nota"]),
            PageBreak(),
        ]
    )

    historia.extend(
        [
            Paragraph("5. Interpretação da regressão", estilos["h1"]),
            Paragraph("Intercepto", estilos["h2"]),
            Paragraph(
                f"O intercepto estimado é {regressao['intercepto']:.4f}. Ele representa um gasto previsto de aproximadamente {moeda(regressao['intercepto'])} quando a renda é zero. Como a amostra começa em renda superior a R$ 1.000,00, essa interpretação é apenas matemática e corresponde a uma extrapolação para fora da faixa observada.",
                estilos["corpo"],
            ),
            Paragraph("Coeficiente angular", estilos["h2"]),
            Paragraph(
                f"O coeficiente da renda é {regressao['coeficiente_angular']:.4f}. Portanto, cada aumento de R$ 1,00 na renda está associado, em média, a um aumento esperado de cerca de R$ {regressao['coeficiente_angular']:.4f} no gasto. Em uma escala mais intuitiva, R$ 1.000,00 adicionais de renda correspondem a aproximadamente {moeda(regressao['coeficiente_angular'] * 1000)} adicionais de gasto previsto.",
                estilos["corpo"],
            ),
            Paragraph("Qualidade do ajuste", estilos["h2"]),
            Paragraph(
                f"O R² de {regressao['r_quadrado']:.4f} indica que cerca de {regressao['r_quadrado']:.2%} da variação observada no gasto é explicada linearmente pela renda nesta amostra. O RMSE de {moeda(regressao['rmse'])} representa a magnitude típica dos erros de previsão dentro dos dados utilizados no ajuste.",
                estilos["corpo"],
            ),
            Paragraph("Limites da interpretação", estilos["h2"]),
            Paragraph(
                "O modelo identifica uma associação linear forte, mas não demonstra que a renda seja a única causa do gasto. Tamanho da família, localização, dívidas e hábitos de consumo podem influenciar o resultado. Além disso, previsões muito além da faixa de renda observada devem ser evitadas.",
                estilos["corpo"],
            ),
            Paragraph("Relação entre estatística e aprendizado de máquina", estilos["h2"]),
            Paragraph(
                "A Distribuição Normal fornece uma linguagem probabilística para representar incerteza e classificar eventos. A Regressão Linear usa dados observados para estimar parâmetros e produzir previsões. Assim, a estatística sustenta o aprendizado de máquina ao oferecer medidas de tendência, variabilidade, erro e qualidade do ajuste. O modelo aprende uma regra numérica a partir dos exemplos, enquanto as métricas ajudam a avaliar o quanto essa regra representa os dados.",
                estilos["corpo"],
            ),
            PageBreak(),
        ]
    )

    # Organização e execução
    historia.extend(
        [
            Paragraph("6. Execução no Google Colab", estilos["h1"]),
            Paragraph(
                "O notebook challenge_sprint_3.ipynb foi organizado em células sequenciais. Para executar a análise no Colab, faça upload do notebook, execute todas as células e, quando solicitado, selecione o arquivo dados_familias.csv. O ambiente do Colab já inclui as bibliotecas principais utilizadas pelo trabalho.",
                estilos["corpo"],
            ),
            Paragraph("Bibliotecas", estilos["h2"]),
            codigo(
                "import matplotlib.pyplot as plt\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "from scipy.stats import norm\n"
                "from sklearn.linear_model import LinearRegression\n"
                "from sklearn.metrics import mean_squared_error, r2_score",
                estilos["codigo"],
            ),
            Paragraph("Arquivos da entrega", estilos["h2"]),
            tabela_resultados(
                [
                    ["Arquivo", "Finalidade"],
                    ["dados_familias.csv", "Base de dados obrigatória em formato CSV."],
                    ["analise_estatistica.py", "Código Python obrigatório com a análise completa."],
                    ["challenge_sprint_3.ipynb", "Notebook adicional pronto para o Google Colab."],
                    ["Sprint_3_Modelagem_Linear.pdf", "Relatório com códigos, gráficos e interpretações."],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.5 * cm),
            Paragraph("7. Conclusão", estilos["h1"]),
            Paragraph(
                "A análise respondeu aos três itens quantitativos do desafio. A chance de o gasto superar a mediana foi classificada como provável; a chance de permanecer a até dois desvios padrão da média foi classificada como quase certa; e a renda explicou aproximadamente 96,99% da variação dos gastos no modelo linear. Os resultados mostram uma aplicação integrada de probabilidade, estatística descritiva e aprendizado supervisionado.",
                estilos["corpo"],
            ),
        ]
    )

    documento.build(
        historia,
        onFirstPage=desenhar_pagina,
        onLaterPages=desenhar_pagina,
    )


if __name__ == "__main__":
    gerar_relatorio(RAIZ / "relatorio" / "Sprint_3_Modelagem_Linear.pdf")
