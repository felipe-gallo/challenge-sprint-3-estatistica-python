def gerar_capa(destino):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from pypdf import PdfReader,PdfWriter
    from pathlib import Path
    pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBold',r'C:\Windows\Fonts\arialbd.ttf'))
    W,H=A4
    left,right=85.04,W-56.69
    mid=(left+right)/2
    c=canvas.Canvas(destino,pagesize=A4)
    names = [linha.replace(' - RM ', '. RM: ') for linha in (Path(__file__).resolve().parents[1] / 'integrantes.txt').read_text(encoding='utf-8-sig').splitlines() if linha.strip()]
    def center(text,y,bold=False):
     c.setFont('ArialBold' if bold else 'Arial',12);c.drawCentredString(mid,H-y,text)
    def authors(y):
     for i,n in enumerate(names):center(n,y+i*18)
    def title(y):
     center('SPRINT 3',y,True)
     center('MODELAGEM LINEAR PARA APRENDIZADO',y+24,True)
     center('DE MÁQUINA',y+42,True)
     center('Estatística com Python',y+66)
    def foot():
     center('SÃO PAULO',H-78)
     center('2026',H-60)
    center('FIAP - ACLIMAÇÃO',97,True)
    center('Ciências da Computação',115,True)
    authors(240)
    title(445)
    foot();c.showPage()
    authors(97)
    title(335)
    s=ParagraphStyle('note',fontName='Arial',fontSize=12,leading=14,alignment=4)
    p=Paragraph('Relatório da Sprint 3 apresentado ao curso de Ciências da Computação da Instituição de Ensino Superior FIAP - ACLIMAÇÃO, na disciplina Estatística com Python.',s)
    w,h=p.wrap((right-left)/2,200);p.drawOn(c,mid,H-495-h)
    url='https://github.com/felipe-gallo/challenge-sprint-3-estatistica-python'
    c.setFont('Arial',10);c.drawString(left,H-645,'Repositório do projeto:')
    c.setFont('Arial',9);c.drawString(left,H-662,url);c.linkURL(url,(left,H-666,right,H-651),relative=0)
    foot();c.save()

