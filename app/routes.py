"""[summary]
"""
from flask import render_template, request, redirect, url_for, flash
from app import app, servicoweb, plotter


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            qtde_restricoes = int(request.form['qtde_restricoes'])
            if not qtde_restricoes or qtde_restricoes < 2 or qtde_restricoes > 11:
                flash(f'Você deve inserir a quantidade de 2 a 10 restrições')
                return redirect(url_for('home'))
            else:
                return redirect(url_for('form_calculadora', qtde_restricoes=qtde_restricoes))
        except Exception:
            flash(
                f'Quantidade "{request.form["qtde_restricoes"]}" está incorreta! Por favor insira apenas números inteiros.')
            return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/formCalculadora/<int:qtde_restricoes>/restricoes', methods=['GET', 'POST'])
def form_calculadora(qtde_restricoes):
    if qtde_restricoes < 2 or qtde_restricoes > 11:
        flash('Você deve inserir a quantidade de 2 a 10 restrições')
        return redirect(url_for('home'))
    if request.method == 'POST':
        if request.form['acao'] == 'resolver':
            try:
                resultado = servicoweb.resolver_metodo_grafico(request)
                if type(resultado) is type(''):
                    flash(resultado)
                    return redirect(url_for('form_calculadora', qtde_restricoes=qtde_restricoes))
                chart = plotter.gerar_graficoXY(resultado)
                chart1 = plotter.gerar_grafico_line(resultado)
                return render_template('resultado.html', resultado=resultado, chart=chart, chart1=chart1)
            except Exception as ex:
                print(ex)
                flash(f'Por favor preencha apenas expressões validas conforme exemplos. ')
                return redirect(url_for('home'))

    return render_template('formCalculadora.html', qtde_restricoes=qtde_restricoes)


@app.route('/saberMais')
def saber_mais():
    return render_template('saberMais.html')


