"""[summary]
"""
from app.metodografico import *
import pygal


def resolver_metodo_grafico(request):
    restricoes = []
    expressao = ''
    resultado = dict()
    # print('RESULTADO QTDE ->>', request.form['qtde_restricoes'])
    qtde_restricoes = int(request.form['qtde_restricoes'])
    try:
        count = 0
        for i in range(qtde_restricoes):
            expressao = request.form[f'restricao{i + 1}']
            if expressao:
                kwargs = set_expressao(expressao)
                restricoes.append(Restricao(**kwargs))
                count += 1
        if count < 2:
            return 'O problema não converge!'
    except Exception as ex:
        print(ex, f'A expressão->> "{expressao}" está incorreta!')
        raise ex
    resultado.setdefault('restricoes', restricoes)

    lista_coordenadas = metodo_cramer(restricoes)
    # print(lista_coordenadas)
    resultado.setdefault('lista_completa_pares_ordenados', lista_coordenadas)
    coordenadas_validas = get_coordenadas_validas(
        lista_coordenadas[:], restricoes[:])
    resultado.setdefault('pares_ord_validos', coordenadas_validas)
    # print(coordenadas_validas)

    exprFuncao = request.form['funcao_objetivo']
    # print('F.O. ->>', funcao)
    kwargs = set_expressao(exprFuncao)
    kwargs.setdefault('objetivo', request.form['objetivo'])
    # print('OBJETIVO ->>', kwargs.get('objetivo'))

    funcaoObjetivo = FuncaoObjetivo(**kwargs)

    funcaoObjetivo.setRotuloVar1(request.form['rotulo_var1'])
    funcaoObjetivo.setRotuloVar2(request.form['rotulo_var2'])
    
    solucaoOtima = encontrar_solucao(funcaoObjetivo, coordenadas_validas)

    listaFuncoesComVerticesValidos = lista_funcoes_obj_com_vertices_validos(funcaoObjetivo, coordenadas_validas)
    resultado.setdefault('lista_func_vertices_validos', listaFuncoesComVerticesValidos)

    funcaoObjetivo.setSolucao(solucaoOtima)

    resultado.setdefault('funcao_objetivo', funcaoObjetivo)    
    # print(funcaoObjetivo, funcaoObjetivo.objetivo)
    # print('SOLUCAO OTIMA ->>', funcaoObjetivo)
    # print('SOLUCAO OTIMA ->>', funcaoObjetivo.getPontosDaReta())
    
    return resultado


def gerar_grafico(resultado):
    problema_de = {'max':'MAXIMIZAÇÃO', 'min': 'MINIMIZAÇÃO'}
    fObjetivo = resultado.get('funcao_objetivo')
    restricoes = resultado.get('restricoes')

    xy_chart = pygal.XY(show_y_guides=True, legend_at_bottom=True,
                        dynamic_print_values=True, print_values_position='top',
                        legend_at_bottom_columns=2, interpolate='cubic')

    xy_chart.title = f'PROBLEMA DE {problema_de[fObjetivo.objetivo]}\n Solução Ótima: {fObjetivo.rotulos[0]}:{fObjetivo.solucao[0]} e {fObjetivo.rotulos[1]}:{fObjetivo.solucao[1]} '

    xy_chart.add(f'{fObjetivo.objetivo.upper()}: {str(fObjetivo)}',
                 fObjetivo.getPontosDaReta(), stroke_style={'width': 5, 'dasharray': '3,6', 'linecap': 'round'})


    xy_chart.add(f'SOLUÇÃO ÓTIMA: {fObjetivo.solucao}',  [{'value': fObjetivo.solucao, 'node': {'r': 6}, 'style': 'stroke: black; stroke-width: 10'},
                                    {'value': fObjetivo.solucao,
                                        'node': {'r': 0}}
                                    ], stroke_style={'width': 2})
    for i, restricao in enumerate(restricoes):
        # print(restricao, '->', restricao.trono)
        xy_chart.add(f'R{i+1}: {str(restricao)}:', restricao.getPontosDaReta(),
                     stroke_style={'width': 2})

    # xy_chart.add(None, [{'value': (0, 40), 'node': {'r': 0}, 'style': 'fill: red; stroke: black; stroke-width: 10'},
    #                         {'value': (0, 0), 'node': {'r': 0}}
    #                         ], stroke_style={'dasharray': '0', 'width': 2, 'linecap': 'round', 'linejoin': 'round', 'line': 'black'
    #                                          })
    return xy_chart.render_data_uri()
