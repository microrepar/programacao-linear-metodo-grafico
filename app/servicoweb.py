"""[summary]
"""
from app.metodografico import *


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

    listaFuncoesComVerticesValidos = lista_funcoes_obj_com_vertices_validos(
        funcaoObjetivo, coordenadas_validas)
    resultado.setdefault('lista_func_vertices_validos',
                         listaFuncoesComVerticesValidos)

    funcaoObjetivo.setSolucao(solucaoOtima)

    resultado.setdefault('funcao_objetivo', funcaoObjetivo)
    # print(funcaoObjetivo, funcaoObjetivo.objetivo)
    # print('SOLUCAO OTIMA ->>', funcaoObjetivo)
    # print('SOLUCAO OTIMA ->>', funcaoObjetivo.getPontosDaReta())

    return resultado

