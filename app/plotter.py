"""Módulo para plotagem de gráficos
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""

import pygal
import copy


def gerar_graficoXY(resultado):
    """Função para plotar gráfico do tipo XY
    
    Arguments:
        resultado {dict} -- dicionário com a seguinte listas: ['restricoes', 'lista_completa_pares_ordenados', 'pares_ord_validos', 'lista_func_vertices_validos', 'funcao_objetivo']

    Returns:
        xy_chart.render_data_uri() -- grafico para ser renderizado pelo flask
    """
    problema_de = {'max': 'MAXIMIZAÇÃO', 'min': 'MINIMIZAÇÃO'}
    fObjetivo = resultado.get('funcao_objetivo')
    restricoes = resultado.get('restricoes')

    # Cria uma estância do gráfico do tipo XY
    xy_chart = pygal.XY(show_y_guides=True, legend_at_bottom=True,
                        dynamic_print_values=True, print_values_position='top',
                        legend_at_bottom_columns=2, interpolate='cubic')

    # Define o titulo do gráfico
    xy_chart.title = f'PROBLEMA DE {problema_de[fObjetivo.objetivo]}\n Solução Ótima-> {fObjetivo.rotulos[0]}({fObjetivo.letras[0]}):{fObjetivo.solucao[0]:.3f} | {fObjetivo.rotulos[1]}({fObjetivo.letras[1]}):{fObjetivo.solucao[1]:.3f} '

    # Adiciona no gráfico os pontos da reta da função objetivo
    xy_chart.add(f'{fObjetivo.objetivo.upper()}: {str(fObjetivo)}',
                 fObjetivo.getPontosDaReta(), stroke_style={'width': 5, 'dasharray': '3,6', 'linecap': 'round'})

    # Adiciona no gráfico os pontos da reta de todas as restrições
    for i, restricao in enumerate(restricoes):
        xy_chart.add(f'R{i+1}: {str(restricao)}: {restricao.inclinacao}', restricao.getPontosDaReta(),
                     stroke_style={'width': 2})

    # Adiciona o ponto da solução ótima
    xy_chart.add(f'SOLUÇÃO ÓTIMA: {fObjetivo.solucao}',  [{'value': fObjetivo.solucao, 'node': {'r': 0}},
                                                          {'value': fObjetivo.solucao, 'node': {
                                                              'r': 6}, 'style': 'stroke: black; stroke-width: 5'}
                                                          ], stroke_style={'width': 2})

    for vertice in resultado['pares_ord_validos']:
        if fObjetivo.solucao == vertice:
            continue
        xy_chart.add(None, [{'value': vertice, 'node': {'r': 6}},
                            {'value': vertice, 'node': {'r': 0}}
                            ], stroke_style={'width': 2})

    # xy_chart.add(None, [{'value': (0, 40), 'node': {'r': 0}, 'style': {'fill: red; stroke: black; stroke-width: 10'},
    #                         {'value': (0, 0), 'node': {'r': 0}}
    #                         ], stroke_style={'dasharray': '0', 'width': 2, 'linecap': 'round', 'linejoin': 'round', 'line': 'black'
    #                                          })

    return xy_chart.render_data_uri()


def gerar_grafico_line(resultado):
    """Função para protar o gráfico do tipo linha
    
    Arguments:
        resultado {dict} -- dicionário com a seguinte listas: ['restricoes', 'lista_completa_pares_ordenados', 'pares_ord_validos', 'lista_func_vertices_validos', 'funcao_objetivo']

    Returns:
        xy_chart.render_data_uri() -- grafico para ser renderizado pelo flask
    """
    problema_de = {'max': 'MAXIMIZAÇÃO', 'min': 'MINIMIZAÇÃO'}
    fObjetivo = resultado.get('funcao_objetivo')
    vertices = resultado['pares_ord_validos']

    # Cria estância do grafico a ser plotado
    chart = pygal.XY(xrange=(0, int(fObjetivo.trono[0])),  show_y_guides=True, legend_at_bottom=True,
                     dynamic_print_values=True, print_values_position='top',
                     legend_at_bottom_columns=2)

    # Adiciona o título do gráfico
    chart.title = f'{ordenar_vertices(vertices)}\nPROBLEMA DE {problema_de[fObjetivo.objetivo]}\n Solução Ótima-> {fObjetivo.rotulos[0]}({fObjetivo.letras[0]}):{fObjetivo.solucao[0]:.3f} | {fObjetivo.rotulos[1]}({fObjetivo.letras[1]}):{fObjetivo.solucao[1]:.3f}'

    # Adiciona a lista de pontos válidos no grafico e preenche a cor da área plotada
    chart.add('REGIÃO VIÁVEL', ordenar_vertices(vertices) ,  fill=True)

    # Adiciona pontos da reta da função objetivo
    chart.add('FUNÇÃO OBJETIVA MAX.', fObjetivo.getPontosDaReta())

    # Adiciona o ponto da função objetivo
    chart.add('SOLUÇÃO ÓTIMA', [fObjetivo.solucao], dots_size=6)
    
    return chart.render_data_uri()


def ordenar_vertices(vertices):
    """Função para ordenar os vertices
    
    Arguments:
        vertices {list(tuple)} -- lista de tuplas com as coordenadas válidas

    Returns:
        vertices_sorted {list(tuple)} -- lista de tuplas ordenadas para plotagem
    """
    vertices_sorted = sorted(copy.deepcopy(vertices))

    for i in range(len(vertices_sorted) - 1):
        if i < len(vertices_sorted)//2:
            continue
        if vertices_sorted[i][0] == vertices_sorted[i+1][0]:
            if vertices_sorted[i][1] < vertices_sorted[i+1][1]:
                vertices_sorted[i], vertices_sorted[i+1] = vertices_sorted[i+1], vertices_sorted[i]

    if len(vertices_sorted) > 3:
        vertices_sorted.append(vertices_sorted[0])
        
    return vertices_sorted

