"""Módulo para resolver problemas de Programação linear com até 2 variáveis de decisão
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""
from app import util

mapa_inclinacao = {'--': 'Decr.', '-+': 'Cresc.',
                   '++': 'Decr.', '+-': 'Cresc.',
                   'FalseTrue': 'Vert.', 'TrueFalse': 'Horiz.'
                   }


class Funcao(object):
    """Classe Funcao - super classe das classes Restricao e FuncaoObjetivo
    """
    trono = [0]
    rotulos = ['', '']
    letras = ['x', 'y']

    def __init__(self, oper0='+', var1=0., oper1='+', var2=0., oper2='>=', valor=0., letras=['x', 'y'], **kwargs):

        self.var1 = var1
        self.var2 = var2
        self.oper0 = oper0
        self.oper1 = oper1
        self.oper2 = oper2
        self.valor = valor
        self.inclinacao = ''
        if letras[0] not in 'xX' and letras[1] not in 'yY':
            self.letras[0], self.letras[1] = letras[0], letras[1]

        if self.var1 == 0 or self.var2 == 0:
            if self.var1 + self.var2 != 0:
                self.inclinacao = mapa_inclinacao.get(f'{self.var1 == 0}{self.var1 != 0}')
            else:
                self.inclinacao = None                
        else:
            self.inclinacao = mapa_inclinacao.get(f'{self.oper0 + self.oper1}')

    def __str__(self):
        return (f'{self.var1}{self.letras[0]} {self.oper1} {self.var2}{self.letras[1]} {self.oper2} {self.valor:.2f}')

    def __repr__(self):
        return (f'({self.var1}{self.letras[0]} {self.oper1} {self.var2}{self.letras[1]} {self.oper2} {self.valor:.2f})')

    def getPontosDaReta(self):
        pontos_da_reta = []
        if self.var1 != 0:
            ponto = (self.valor / self.var1, 0)
            pontos_da_reta.append(ponto)
        else:
            ponto = (self.trono[0], self.valor / self.var2)
            pontos_da_reta.append(ponto)

        if self.var2 != 0:
            ponto = (0, self.valor / self.var2)
            pontos_da_reta.append(ponto)
        else:
            ponto = (self.valor / self.var1, self.trono[0])
            pontos_da_reta.append(ponto)

        return pontos_da_reta

    def setRotuloVar1(self, rotulo):
        self.rotulos[0] = rotulo

    def setRotuloVar2(self, rotulo):
        self.rotulos[1] = rotulo


class Restricao(Funcao):
    """Define a classe para criação de restrições da PL
    """
    def __init__(self, oper0='+', var1=0., oper1='+', var2=0., oper2='>=', valor=0., letras=['x', 'y'], **kwargs):
        super().__init__(oper0, var1, oper1, var2, oper2, valor, letras, **kwargs)


class FuncaoObjetivo(Funcao):
    """Define a classe a criação da função objeto da PL
    """
    def __init__(self, oper0='+', var1=0., oper1='+', var2=0., oper2='>=', valor=0., letras=['x', 'y'], **kwargs):
        super().__init__(oper0, var1, oper1, var2, oper2, valor, letras, **kwargs)
        self.objetivo = kwargs.get('objetivo')

    def setSolucao(self, solucao):
        self.solucao = solucao
        self.valor = calcular(
            self.oper1, solucao[0] * self.var1, solucao[1] * self.var2)
        try:
            pre_trono = (self.valor / self.var1) if (self.valor /
                                                     self.var1) > (self.valor / self.var2) else (self.valor / self.var2)
            self.trono[0] = pre_trono if pre_trono > self.trono[0] else self.trono[0]
        except Exception as ex:
            print(f'O valor do resultado da função ainda não foi definido\n{ex}')

    def __repr__(self):
        representa = f'{self.var1} x {self.solucao[0]} {self.oper1} {self.var2} x {self.solucao[1]} {self.oper2} {self.valor} ; {self.objetivo} '
        return representa


def set_expressao(expressao, varx, vary):
    """Prepara a string contendo a expressão matematica para instância de um do tipo da Classe Funcao

    Arguments:
        expressao {str} -- string com a formula das funções objetivo e restrições

    Raises:
        RuntimeError -- lenvanta um erro caso os operadores da expressão estiverem incorretos
        error -- levanta um erro caso não consiga efetuar a conversão de string para float

    Returns:
        dict -- dicionário de dados contendo os parametros para instanciar um objeto Funcao
    """
    # insere uma expressão nula para os campos do formulários que não forem preenchidos
    if expressao == '':
        expressao = '0x+0y=0'
        
    expressao = util.prepara_string_to_map(expressao, varx, vary)

    # cria uma lista de tuplas do tipo chave, valor
    args = [(x, i) for x, i in zip('oper0 var1 oper1 var2 oper2 valor'.split(), expressao.split())]
    
    # passa a lista de tuplas para a dict função para converter a lista de tuplas em um dicionário
    kwargs = dict(args)

    letras = [kwargs.get('var1')[-1], kwargs.get('var2')[-1]]

    # concatena os sinais nos valores das variáveis x e y
    kwargs['var1'] = (kwargs.get('oper0') + kwargs.get('var1'))
    kwargs['var2'] = (kwargs.get('oper1') + kwargs.get('var2'))

    # valida os sinais e operadores da expressão
    if kwargs.get('oper1') not in ['+', '-'] or \
            kwargs.get('oper2') not in ['<=', '>=', '=']:
        raise RuntimeError()

    try:
        if letras[0] not in '0123456789' and letras[1] not in '0123456789':
            kwargs['letras'] = letras
            kwargs['var1'] = float(kwargs.get('var1')[:-1])
            kwargs['var2'] = float(kwargs.get('var2')[:-1])

        elif letras[0] not in '0123456789':
            kwargs['var1'] = float(kwargs.get('var1')[:-1])
            kwargs['var2'] = float(kwargs.get('var2'))
        elif letras[1] not in '0123456789':
            kwargs['var1'] = float(kwargs.get('var1'))
            kwargs['var2'] = float(kwargs.get('var2')[:-1])
        else:
            kwargs['var1'] = float(kwargs.get('var1'))
            kwargs['var2'] = float(kwargs.get('var2'))

        kwargs['valor'] = float(kwargs.get('valor')[:])

        return kwargs
    except ValueError as error:
        print('SET_EXPRESSAO->>',error)
        raise error
        

def metodo_cramer(restricoes):
    """Efetua calculo matricial pelo metodo de Cramer

    Arguments:
        restricoes {list{Restricao}} -- Lista de objetos do tipo Restricao
    Returns:
        {list{tuple}} -- lista de coordenadas (x, y) com base nas restrições impostas
    """
    pontos = list()
    for i in range(len(restricoes)):
        for j in range(len(restricoes)):
            if i - j == 0:
                continue
            determinante = (restricoes[i].var1 * restricoes[j].var2) - \
                (restricoes[j].var1 * restricoes[i].var2)
            if determinante == 0:
                continue
            determinantex = (restricoes[i].valor * restricoes[j].var2) - \
                (restricoes[j].valor * restricoes[i].var2)
            determinantey = (restricoes[i].var1 * restricoes[j].valor) - \
                (restricoes[j].var1 * restricoes[i].valor)
            x, y = determinantex / determinante, determinantey / determinante
            # print(restricoes[i])
            # print(restricoes[j])
            # print(f'PONTOS->>',x,y)
            pontos.append((x,y))
    # insere a lista de pontos em uma set para retirar as tuplas de coordenadas repetidas
    resultado_cramer = list(set(pontos))
    return resultado_cramer


def get_coordenadas_validas(lista_coordenadas, restricoes):
    """Filtra as lista de coordenadas com base nas restrições

    Arguments:
        lista_coordenadas {list} -- lista de tuplas contendo as coordenadas encontradas
        restricoes {list} -- lista de objetos de restrições para validar as coordenadas

    Returns:
        coordenadas_validas {list} -- lista de coordenadas validadas pelas restrições
    """

    coordenadas_validas = []
    for x, y in lista_coordenadas:
        count = 0
        for restricao in restricoes:
            valor = calcular(restricao.oper1, restricao.var1 *
                             x, restricao.var2 * y)
            if not eh_coordenada_valida(restricao.oper2, valor, restricao.valor):
                count += 1
        if count == 0:
            coordenadas_validas.append((x, y))
    return coordenadas_validas


def sub(num1, num2):
    """Efetua a operação de subtração
    """
    return num1 - num2


def soma(num1, num2):
    """Efetua a operação de soma
    """
    return num1 + num2


def calcular(operador, *args):
    """Verifica qual operação de calculo com base no operador dos objetos do tipo Funcao
    """
    operacao = {'+': soma, '-': sub}
    return operacao.get(operador)(*args)


def eh_menor_igual(valor, restricao):
    return valor <= restricao


def eh_maior_igual(valor, restricao):
    return valor >= restricao


def eh_igual(valor, restricao):
    return valor == restricao


def eh_menor_que(valor, restricao):
    return valor < restricao


def eh_maior_que(valor, restricao):
    return valor > restricao


def eh_coordenada_valida(operador, valor, restricao_valor):
    """Função para retorna a função que compara os valores conforme operador

    Arguments:
        operador {str} -- operadora para comparação
        valor {float} -- valor a ser comparado
        restricao_valor {float} -- valor da restrição para efetuar comparação
    Returns:
        bool -- retorna um valor boleano conforme resultado da comparação
    """
    operacao = {'<=': eh_menor_igual, '=': eh_igual, '>=': eh_maior_igual,
                '<': eh_menor_que, '>': eh_maior_que
                }
    # Utiliza a função mapeada utilizando o operador como chave e executa a função
    # enviando os valores a serem comparados
    return operacao.get(operador)(valor, restricao_valor)


def encontrar_solucao(funcao, coordenadas_validas):
    """Função encontra a solução ótima da lista de coordenadas válidas
    
    Arguments:
        funcao {FuncaoObjetivo} -- objeto FuncaoObjetivo para validar solução ótima
        coordenadas_validas {lis[tuple]} -- lista de tuplas com coordenadas válidas
    
    Returns:
        solucao_otima {tuple} -- tupla com a coordenada da solução ótima
    """
    valores_solucao = []
    objetivo = {'max': max, 'min': min}
    if len(coordenadas_validas) == 0:
        return coordenadas_validas
    for x, y in coordenadas_validas:
        valores_solucao.append([calcular(funcao.oper1, funcao.var1 * x, funcao.var2 * y)])
    solucao_otima = coordenadas_validas[valores_solucao.index(objetivo.get(funcao.objetivo)(valores_solucao))]
    return solucao_otima


def lista_funcoes_obj_com_vertices_validos(funcaoObjetivo, lista_coordenadas, varx, vary):
    lista_funcoes_objetivo = []
    expressao = str(funcaoObjetivo)
    objetivo = funcaoObjetivo.objetivo

    for vertice in lista_coordenadas:
        kwargs = set_expressao(expressao, varx, vary)
        kwargs.setdefault('objetivo', objetivo)

        fObjetivo = FuncaoObjetivo(**kwargs)

        fObjetivo.setSolucao(vertice)

        lista_funcoes_objetivo.append(fObjetivo)

    return lista_funcoes_objetivo


def main():
    # restricoes = []
    # expressao = ''
    # try:
    #     for _ in range(5):
    #         expressao = input('Entre com as restrições:')
    #         kwargs = set_expressao(expressao, varx='x', vary='y')
    #         restricoes.append(Restricao(**kwargs))
    # except Exception as ex:
    #     print(ex, f'A expressão->> "{expressao}" está incorreta!')

    # lista_coordenadas = metodo_cramer(restricoes)
    # # print(lista_coordenadas)

    # coordenadas_validas = get_coordenadas_validas(
    #     lista_coordenadas[:], restricoes[:])
    # # print(coordenadas_validas)

    # funcao = input('Insira a função objetivo:')
    # kwargs = set_expressao(funcao, varx=varx, vary=vary)
    # funcaoObjetivo = FuncaoObjetivo(objetivo='max', **kwargs)
    # # print(funcaoObjetivo, funcaoObjetivo.objetivo)

    # solucaoOtima = encontrar_solucao(funcaoObjetivo, coordenadas_validas)

    # funcaoObjetivo.setSolucao(solucaoOtima)
    # # print('SOLUCAO OTIMA ->>', funcaoObjetivo.__repr__())
    pass


if __name__ == '__main__':
    main()
    # args = 4.0,5
    # print(calcular('+',*args))
