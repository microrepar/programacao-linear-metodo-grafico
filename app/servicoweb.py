"""Módulo responsável por servir as requisições web
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""

from app.metodografico import *


def resolver_metodo_grafico(request):
    """Função para resolução de ploblemas de programação linear pelo método gráfico
    
    Arguments:
        request {Object} -- objeto de request com as informações da requisição

    Returns:
        resultado {dict} -- dicionário com a seguinte listas: ['restricoes', 'lista_completa_pares_ordenados', 'pares_ord_validos', 'lista_func_vertices_validos', 'funcao_objetivo']
    """
    restricoes = []
    expressao = ''
    resultado = dict()

    # Atribuição dos valores da contidos na requisição para as variáveis locais
    qtde_restricoes = int(request.form['qtde_restricoes']) 
    varx = request.form['variavelx']
    vary = request.form['variavely']
    # Recupera da requesição a expressão da função objetivo
    exprFuncao = request.form['funcao_objetivo']

    if exprFuncao == '':
        return 'Por favor preencha o campo da função objetivo'

    if varx == '' or vary == '':
        return 'Por favor preencha a letra do rótulo'
    

    try:
        # contador para verificar a quantidade de campos preenchidos no formulário
        count = 0
        
        for i in range(qtde_restricoes):
            expressao = request.form[f'restricao{i + 1}']
            if expressao != '':
                kwargs = set_expressao(expressao, varx, vary)
                restricoes.append(Restricao(**kwargs))
                count += 1

        # verifica a quantidade de campos das restrições preenchidas
        if count < 2:
            return 'O problema não converge!'

        # Adiciona as restrições de positividade para o input-chekbox ativo
        if request.form.get('restricao_positiva', None) == 'ativo':
            restricoes.append(Restricao(**set_expressao(f'{varx}>=0', varx, vary)))
            restricoes.append(Restricao(**set_expressao(f'{vary}>=0', varx, vary)))

    except Exception as ex:
        print(ex, f'A expressão->> "{expressao}" está incorreta!')
        raise ex
    
    # Chama a função metodo_cramer e obtém uma lista de coordenadas não repetidas
    lista_coordenadas = metodo_cramer(restricoes)

    # Cria uma lista de coordenadas válidas
    coordenadas_validas = get_coordenadas_validas(lista_coordenadas[:], restricoes[:])

    # Prepara a keywords arguments para instanciar a função objetivo
    kwargs = set_expressao(exprFuncao, varx, vary)
    kwargs.setdefault('objetivo', request.form['objetivo'])

    # Cria uma estância da classe FuncaoObjetivo
    funcaoObjetivo = FuncaoObjetivo(**kwargs)

    # Adiciona o rótulo da variável x
    funcaoObjetivo.setRotuloVar1(request.form['rotulo_var1'])

    # Adiciona o rótulo da variável y
    funcaoObjetivo.setRotuloVar2(request.form['rotulo_var2'])

    # Obtém a solução ótima da lista de coordenadas válidas
    solucaoOtima = encontrar_solucao(funcaoObjetivo, coordenadas_validas)

    # Retorna mensagem de não conversão caso não encontre nenhuma solução e finaliza a função
    if not solucaoOtima:
        return 'O problema não converge!'

    # Adiciona a tupla da solução ótima na função objetivo
    funcaoObjetivo.setSolucao(solucaoOtima)

    # Obtém uma lista de funções objetivo com base na lista de coordenadas válidas
    listaFuncoesComVerticesValidos = lista_funcoes_obj_com_vertices_validos(funcaoObjetivo, coordenadas_validas, varx, vary)

    # Adiciona as listas obtidas no dicionário resultados para ser renderizado no template de resposta
    resultado.setdefault('restricoes', restricoes)
    resultado.setdefault('lista_completa_pares_ordenados', lista_coordenadas)
    resultado.setdefault('pares_ord_validos', coordenadas_validas)
    resultado.setdefault('lista_func_vertices_validos', listaFuncoesComVerticesValidos)
    resultado.setdefault('funcao_objetivo', funcaoObjetivo)    

    return resultado

