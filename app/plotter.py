import pygal


def gerar_graficoXY(resultado):
    problema_de = {'max': 'MAXIMIZAÇÃO', 'min': 'MINIMIZAÇÃO'}
    fObjetivo = resultado.get('funcao_objetivo')
    restricoes = resultado.get('restricoes')

    xy_chart = pygal.XY(show_y_guides=True, legend_at_bottom=True,
                        dynamic_print_values=True, print_values_position='top',
                        legend_at_bottom_columns=2, interpolate='cubic')

    xy_chart.title = f'PROBLEMA DE {problema_de[fObjetivo.objetivo]}\n Solução Ótima: {fObjetivo.rotulos[0]}:{fObjetivo.solucao[0]} e {fObjetivo.rotulos[1]}:{fObjetivo.solucao[1]} '

    xy_chart.add(f'{fObjetivo.objetivo.upper()}: {str(fObjetivo)}',
                 fObjetivo.getPontosDaReta(), stroke_style={'width': 5, 'dasharray': '3,6', 'linecap': 'round'})

    for i, restricao in enumerate(restricoes):
        # print(restricao, '->', restricao.trono)
        xy_chart.add(f'R{i+1}: {str(restricao)}:', restricao.getPontosDaReta(),
                     stroke_style={'width': 2})

    xy_chart.add(f'SOLUÇÃO ÓTIMA: {fObjetivo.solucao}',  [{'value': fObjetivo.solucao, 'node': {'r': 0}},
                                                          {'value': fObjetivo.solucao, 'node': {
                                                              'r': 6}, 'style': 'stroke: black; stroke-width: 5'}
                                                          ], stroke_style={'width': 2})

    # xy_chart.add(None, [{'value': (0, 40), 'node': {'r': 0}, 'style': {'fill: red; stroke: black; stroke-width: 10'},
    #                         {'value': (0, 0), 'node': {'r': 0}}
    #                         ], stroke_style={'dasharray': '0', 'width': 2, 'linecap': 'round', 'linejoin': 'round', 'line': 'black'
    #                                          })

    for vertice in resultado['pares_ord_validos']:
        if fObjetivo.solucao == vertice:
            continue
        xy_chart.add(None, [{'value': vertice, 'node': {'r': 6}},
                            {'value': vertice, 'node': {'r': 0}}
                            ], stroke_style={'width': 2})

    return xy_chart.render_data_uri()


def gerar_grafico_line(resultado):

    problema_de = {'max': 'MAXIMIZAÇÃO', 'min': 'MINIMIZAÇÃO'}
    fObjetivo = resultado.get('funcao_objetivo')
    restricoes = resultado.get('restricoes')
    vertices = resultado['pares_ord_validos']

   
    chart = pygal.XY(xrange=(0, int(fObjetivo.trono[0])),  show_y_guides=True, legend_at_bottom=True,
                     dynamic_print_values=True, print_values_position='top',
                     legend_at_bottom_columns=2)
    chart.title = f'PROBLEMA DE {problema_de[fObjetivo.objetivo]}\n Solução Ótima: {fObjetivo.rotulos[0]}:{fObjetivo.solucao[0]} e {fObjetivo.rotulos[1]}:{fObjetivo.solucao[1]}'

    chart.add('line', [(0, 0), (0, 24), (8, 24), (16, 8), (16, 0), (0, 0)],  fill=True)
    chart.add('Funcão Objetivo Max', fObjetivo.getPontosDaReta())
    chart.add('Solução Ótima', [fObjetivo.solucao], dots_size=6)
    
    return chart.render_data_uri()
