from flask import Flask, render_template, request, send_from_directory, url_for, flash, redirect
from calculos import calcular_simulacao
from gerar_pdf import gerar_pdf_premium
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'troque-esta-chave-para-producao'

BASE_DIR = os.path.dirname(__file__)
REL_DIR = os.path.join(BASE_DIR, 'relatorios')
os.makedirs(REL_DIR, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/simulador', methods=['GET'])
def simulador():
    return render_template('form.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    form = request.form.to_dict()
    form['importado'] = True if request.form.get('importado')=='on' else False
    form['st'] = True if request.form.get('st')=='on' else False
    form['monofasico'] = True if request.form.get('monofasico')=='on' else False

    resultado = calcular_simulacao(form)

    filename = f"simulacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REL_DIR, filename)
    try:
        gerar_pdf_premium(form, resultado, filepath)
        pdf_url = url_for('baixar_pdf', filename=filename)
    except Exception as e:
        pdf_url = None
        flash('Erro ao gerar PDF: ' + str(e))

    return render_template('resultado.html', formulario=form, resultado=resultado, pdf_path=pdf_url)

@app.route('/relatorios/<path:filename>')
def baixar_pdf(filename):
    return send_from_directory(REL_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
