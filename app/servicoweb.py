"""[summary]
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""
from app.metodografico import *



def resolver_metodo_grafico(request):
    restricoes = []
    expressao = ''
    resultado = dict()
    # print('RESULTADO QTDE ->>', request.form['qtde_restricoes'])
    qtde_restricoes = int(request.form['qtde_restricoes']) 
    varx = request.form['variavelx']
    vary = request.form['variavely']
    try:
        count = 0
        for i in range(qtde_restricoes):
            expressao = request.form[f'restricao{i + 1}']
            if expressao != '':
                kwargs = set_expressao(expressao, varx, vary)
                # print("KWARGS->>",i, kwargs)
                restricoes.append(Restricao(**kwargs))
                count += 1
        if count < 2:
            return 'O problema não converge!'

        if request.form.get('restricao_positiva', None) == 'ativo':
            restricoes.append(Restricao(**set_expressao(f'{varx}>=0', varx, vary)))
            restricoes.append(Restricao(**set_expressao(f'{vary}>=0', varx, vary)))

    except Exception as ex:
        print(ex, f'A expressão->> "{expressao}" está incorreta!')
        raise ex

    
    lista_coordenadas = metodo_cramer(restricoes)
    resultado.setdefault('restricoes', restricoes)
    # print(lista_coordenadas)
    resultado.setdefault('lista_completa_pares_ordenados', lista_coordenadas)
    coordenadas_validas = get_coordenadas_validas(
        lista_coordenadas[:], restricoes[:])
    resultado.setdefault('pares_ord_validos', coordenadas_validas)
    # print(coordenadas_validas)

    exprFuncao = request.form['funcao_objetivo']
    kwargs = set_expressao(exprFuncao, varx, vary)
    kwargs.setdefault('objetivo', request.form['objetivo'])

    funcaoObjetivo = FuncaoObjetivo(**kwargs)

    funcaoObjetivo.setRotuloVar1(request.form['rotulo_var1'])
    funcaoObjetivo.setRotuloVar2(request.form['rotulo_var2'])

    solucaoOtima = encontrar_solucao(funcaoObjetivo, coordenadas_validas)

    # retorna mensagem de não conversão caso não encontre nenhuma solução
    if len(solucaoOtima) == 0:
        return 'O problema não converge!'

    listaFuncoesComVerticesValidos = lista_funcoes_obj_com_vertices_validos(funcaoObjetivo, coordenadas_validas, varx, vary)
    resultado.setdefault('lista_func_vertices_validos', listaFuncoesComVerticesValidos)

    funcaoObjetivo.setSolucao(solucaoOtima)

    resultado.setdefault('funcao_objetivo', funcaoObjetivo)    

    return resultado

