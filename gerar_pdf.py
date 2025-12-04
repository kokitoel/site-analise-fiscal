from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

def _draw_header(c, largura, altura, title, theme='#2ecc71'):
    c.setFillColor(colors.HexColor(theme))
    c.rect(0, altura-40, largura, 40, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, altura-28, title)

def _draw_kpi_box(c, x, y, w, h, label, value, theme='#2ecc71'):
    c.setFillColor(colors.HexColor('#f6f9f6'))
    c.roundRect(x, y-h, w, h, 6, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(colors.HexColor(theme))
    c.drawString(x+8, y-18, label)
    c.setFont('Helvetica-Bold', 14)
    c.setFillColor(colors.black)
    c.drawString(x+8, y-36, str(value))

def gerar_pdf_premium(dados, resultado, caminho_saida, theme='#2ecc71'):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    largura, altura = A4
    c = canvas.Canvas(caminho_saida, pagesize=A4)
    _draw_header(c, largura, altura, 'Relatório de Análise Fiscal', theme=theme)

    y = altura - 60
    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#333333'))
    c.drawString(40, y, f"Data de emissão: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 18

    kpi_w = 160
    kpi_h = 48
    _draw_kpi_box(c, 40, y, kpi_w, kpi_h, 'Lucro Líquido (R$)', resultado.get('lucro_liquido', 0), theme=theme)
    _draw_kpi_box(c, 220, y, kpi_w, kpi_h, 'Margem Real (%)', f"{resultado.get('margem_real_pct',0)}%", theme=theme)
    _draw_kpi_box(c, 400, y, kpi_w, kpi_h, 'Tributos Totais (R$)', resultado.get('tributos_totais',0), theme=theme)
    y -= (kpi_h + 20)

    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y, 'Dados informados:')
    y -= 14
    c.setFont('Helvetica', 10)
    for key in ['empresa','custo','compras_internas','compras_interestaduais','media_vendas']:
        val = dados.get(key)
        if val is not None and str(val).strip()!='':
            c.drawString(50, y, f"{key}: {val}")
            y -= 12

    y -= 8
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y, 'Resultados calculados:')
    y -= 16
    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#eeeeee'))
    c.rect(40, y-18, largura-80, 18, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.drawString(48, y-14, 'Item')
    c.drawString(300, y-14, 'Valor')
    y -= 28
    for chave, valor in resultado.items():
        c.drawString(48, y, str(chave))
        c.drawString(300, y, str(valor))
        y -= 14
        if y < 80:
            c.showPage()
            largura, altura = A4
            _draw_header(c, largura, altura, 'Relatório de Análise Fiscal', theme=theme)
            y = altura - 80

    c.setFont('Helvetica', 8)
    c.setFillColor(colors.HexColor('#999999'))
    c.drawString(40, 30, 'Gerado por Simulador Fiscal - https://seudominio.com')
    c.save()
    return caminho_saida
