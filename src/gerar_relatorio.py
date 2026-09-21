# ARTHUR MAZIVIERO FARIA - RM 573928
# JUN UEHARA - RM 570537
# FELIPE DE SOUZA GALLO - RM 569680
# ROBERSON REGUERO LUIZ JUNIOR - RM 573031
# TOMMASO CONCEIÇÃO NAGLIATTI - RM 572147
# MATHEUS MARTINS LACERDA - RM 570843

"""Gera o relatório PDF da Challenge Sprint 3."""

from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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
INTEGRANTES = [tuple(linha.rsplit(" - RM ", 1))
               for linha in (RAIZ / "integrantes.txt").read_text(encoding="utf-8-sig").splitlines()
               if linha.strip()]


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
            fontSize=24,
            leading=29,
            textColor=COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "subcapa": ParagraphStyle(
            "Subcapa",
            parent=estilos_base["Normal"],
            fontName=fonte,
            fontSize=13,
            leading=19,
            textColor=COR_TEXTO,
            alignment=TA_CENTER,
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
            fontSize=11.5,
            leading=17.25,
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
        "codigo_completo": ParagraphStyle(
            "CodigoCompletoProjeto",
            parent=estilos_base["Code"],
            fontName="Courier",
            fontSize=6.2,
            leading=8.1,
            leftIndent=6,
            rightIndent=6,
            borderColor=colors.HexColor("#D6E1EA"),
            borderWidth=0.6,
            borderPadding=6,
            backColor=colors.HexColor("#F6F8FA"),
            textColor=colors.HexColor("#1F2933"),
            spaceBefore=3,
            spaceAfter=7,
        ),
        "integrantes_titulo": ParagraphStyle(
            "IntegrantesTitulo",
            parent=estilos_base["Normal"],
            fontName=fonte_negrito,
            fontSize=14,
            leading=18,
            textColor=COR_PRIMARIA,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "integrante": ParagraphStyle(
            "Integrante",
            parent=estilos_base["Normal"],
            fontName=fonte,
            fontSize=11,
            leading=18,
            textColor=COR_TEXTO,
            alignment=TA_CENTER,
            spaceAfter=5,
        ),
        "link_capa": ParagraphStyle(
            "LinkCapa",
            parent=estilos_base["Normal"],
            fontName=fonte,
            fontSize=8.5,
            leading=12,
            textColor=COR_PRIMARIA,
            alignment=TA_CENTER,
        ),
    }


def codigo(texto: str, estilo: ParagraphStyle) -> Paragraph:
    seguro = html.escape(texto).replace(" ", "&nbsp;").replace("\n", "<br/>")
    return Paragraph(seguro, estilo)


def blocos_codigo_arquivo(
    caminho: Path, estilo: ParagraphStyle, linhas_por_bloco: int = 44
) -> list[Paragraph]:
    """Transforma um arquivo-fonte em blocos legíveis e pagináveis no PDF."""
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    return [
        codigo("\n".join(linhas[inicio : inicio + linhas_por_bloco]), estilo)
        for inicio in range(0, len(linhas), linhas_por_bloco)
    ]


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


def tabela_dados_familias(dados, fonte: str, fonte_negrito: str) -> Table:
    """Monta a tabela completa da base de famílias para o apêndice."""
    linhas = [["Família", "Renda familiar (R$)", "Gasto familiar (R$)"]]
    linhas.extend(
        [
            str(int(registro.id_familia)),
            f"{int(registro.renda_familiar):,}".replace(",", "."),
            f"{int(registro.gasto_familiar):,}".replace(",", "."),
        ]
        for registro in dados.itertuples(index=False)
    )
    tabela = Table(linhas, colWidths=[3.1 * cm, 6.25 * cm, 6.25 * cm], repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COR_PRIMARIA),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), fonte_negrito),
                ("FONTNAME", (0, 1), (-1, -1), fonte),
                ("FONTSIZE", (0, 0), (-1, -1), 8.3),
                ("LEADING", (0, 0), (-1, -1), 10.2),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_CLARA]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D5DF")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tabela


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
        leftMargin=3 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm,
        title="Sprint 3 - Modelagem Linear para Aprendizado de Máquina",
        author=", ".join(nome for nome, _ in INTEGRANTES),
        subject="Distribuição Normal e Regressão Linear",
    )
    historia = []

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
                "A base contém 50 famílias e duas variáveis monetárias: renda familiar e gasto familiar. Um identificador diferencia os registros, enquanto a coluna autores_trabalho documenta os nomes completos e RMs do grupo. Essas duas colunas não participam dos cálculos. A análise considera a hipótese de normalidade para a variável gasto familiar.",
                estilos["corpo"],
            ),
            tabela_resultados(
                [
                    ["Variável", "Descrição"],
                    ["renda_familiar", "Renda total observada para cada família, em reais."],
                    ["gasto_familiar", "Gasto total observado para cada família, em reais."],
                    ["id_familia", "Identificador sequencial sem papel no modelo."],
                    ["autores_trabalho", "Identificação do grupo; excluída dos cálculos."],
                ],
                fonte,
                fonte_negrito,
            ),
            Paragraph("Critério de classificação dos eventos", estilos["h2"]),
            Paragraph(
                "Foram adotadas faixas explícitas: raro para probabilidade de até 5%; pouco provável acima de 5% e até 25%; provável acima de 25% e até 75%; e quase certo acima de 75%. Essa convenção foi mantida em todas as classificações para assegurar consistência metodológica.",
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
                "A mediana divide os dados observados em duas metades. A probabilidade foi estimada por uma Distribuição Normal parametrizada com a média e o desvio padrão amostrais, calculando-se a área à direita da mediana por meio da função de sobrevivência.",
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
            Image(str(RAIZ / "resultados" / "distribuicao_normal.png"), width=14.6 * cm, height=8.0 * cm),
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
                "A faixa sombreada em azul na Figura 1 representa esse intervalo. A área laranja evidencia, ao mesmo tempo, o evento acima da mediana analisado anteriormente.",
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
            Image(str(RAIZ / "resultados" / "regressao_linear.png"), width=15.6 * cm, height=9.05 * cm),
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
                "O notebook challenge_sprint_3.ipynb foi organizado em células sequenciais e reúne a leitura da base, os cálculos, os gráficos e os testes automatizados. A execução no Google Colab utiliza o arquivo dados_familias.csv e não depende de carregamento de código externo. A última célula verifica a consistência dos resultados obtidos.",
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
            Paragraph("Arquivos do projeto", estilos["h2"]),
            tabela_resultados(
                [
                    ["Arquivo", "Finalidade"],
                    ["dados_familias.csv", "Base de dados utilizada nos cálculos."],
                    ["analise_estatistica.py", "Código Python da análise completa."],
                    
                    ["Relatório Sprint 3 Modelagem Linear.pdf", "Relatório com códigos, gráficos e interpretações."],
                ],
                fonte,
                fonte_negrito,
            ),
            Spacer(1, 0.5 * cm),
            Paragraph("7. Conclusão", estilos["h1"]),
            Paragraph(
                "A análise integrou três etapas quantitativas. A chance de o gasto superar a mediana foi classificada como provável; a chance de permanecer a até dois desvios padrão da média foi classificada como quase certa; e a renda explicou aproximadamente 96,99% da variação dos gastos no modelo linear. Os resultados demonstram uma aplicação conjunta de probabilidade, estatística descritiva e aprendizado supervisionado.",
                estilos["corpo"],
            ),
        ]
    )

    historia.extend([
        Paragraph("8. Validação automatizada", estilos["h1"]),
        Paragraph("O notebook foi executado integralmente. Sua última célula executou os 10 testes do projeto e 6 testes dos resultados do notebook, totalizando 16 testes aprovados, sem falhas. As verificações abrangem a base de 50 famílias, as estatísticas, as probabilidades, os limites de classificação, a regressão e a consistência com o módulo Python.", estilos["corpo"]),
    ])
    historia.extend([
        PageBreak(),
        Paragraph("Apêndice A - Repositório e código-fonte", estilos["h1"]),
        Paragraph(
            "O repositório público reúne os arquivos utilizados no desenvolvimento da análise estatística e permite consultar o histórico técnico do projeto.",
            estilos["corpo"],
        ),
        Paragraph(
            '<link href="https://github.com/felipe-gallo/challenge-sprint-3-estatistica-python" color="#174A7E">https://github.com/felipe-gallo/challenge-sprint-3-estatistica-python</link>',
            estilos["corpo"],
        ),
        Paragraph("Código completo de analise_estatistica.py", estilos["h2"]),
        Paragraph(
            "O código a seguir realiza a leitura e a validação dos dados, os cálculos probabilísticos, a classificação dos eventos, o ajuste da Regressão Linear e a geração dos gráficos.",
            estilos["corpo"],
        ),
        *blocos_codigo_arquivo(
            RAIZ / "src" / "analise_estatistica.py", estilos["codigo_completo"]
        ),
        PageBreak(),
        Paragraph("Apêndice B - Base de dados das famílias", estilos["h1"]),
        Paragraph(
            "A tabela apresenta os 50 registros utilizados na análise. Cada observação contém o identificador da família, a renda familiar e o gasto familiar. A coluna de autoria presente no arquivo CSV possui finalidade documental e não participa dos cálculos estatísticos.",
            estilos["corpo"],
        ),
        tabela_dados_familias(dados, fonte, fonte_negrito),
    ])
    documento.build(historia)
    from capa_abnt import gerar_capa
    from pypdf import PdfReader, PdfWriter
    from io import BytesIO
    frente = BytesIO()
    gerar_capa(frente)
    frente.seek(0)
    corpo = PdfReader(BytesIO(destino.read_bytes()))
    writer = PdfWriter()
    for pagina in PdfReader(frente).pages:
        writer.add_page(pagina)
    for pagina in corpo.pages:
        writer.add_page(pagina)
    with destino.open('wb') as arquivo:
        writer.write(arquivo)


if __name__ == "__main__":
    gerar_relatorio(RAIZ / "relatorio" / "Relatório Sprint 3 Modelagem Linear.pdf")
