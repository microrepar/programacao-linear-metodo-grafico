"""Módulo para resolver problemas de Programação linear com até 2 variáveis de decisão
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""


from app import util

# mapea a combinação de sinais para encontrar a inclinação da reta
mapa_inclinacao = {'--': 'Decr.', '-+': 'Cresc.',
                   '++': 'Decr.', '+-': 'Cresc.',
                   'FalseTrue': 'Vert.', 'TrueFalse': 'Horiz.'
                   }


class Funcao(object):
    """Classe Funcao -- super classe
    """
    trono = [0]
    rotulos = ['', '']
    letras = ['x', 'y']

    def __init__(self, oper0='+', var1=0., oper1='+', var2=0., oper2='>=', valor=0., letras=['x', 'y'], **kwargs):
        """Método construtor da classe Funcao
        
        Keyword Arguments:
            oper0 {str} -- sinal do valor multiplicador de x (default: {'+'})
            var1 {float} -- valor do multiplicador de x (default: {0.})
            oper1 {str} -- sinal do valor multiplicador de y (default: {'+'})
            var2 {float} -- valor do multiplicador de y (default: {0.})
            oper2 {str} -- sinal da operação a ser realizada (default: {'>='})
            valor {float} -- resultado da igualdade ou inequação (default: {0.})
            letras {list(str)} -- icógnitas utilizadas na função ou inequação (default: {['x', 'y']})
        """
        self.var1 = var1
        self.var2 = var2
        self.oper0 = oper0
        self.oper1 = oper1
        self.oper2 = oper2
        self.valor = valor
        self.inclinacao = ''

        # altera o padrão das icógnitas se forem diferentes de x e y
        if letras[0] not in 'xX' and letras[1] not in 'yY':
            self.letras[0], self.letras[1] = letras[0], letras[1]

        # descobre a inclinação da reta da função ou inequação
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
        """Retorna os pontos da reta conforme sua inclinação
        """
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
        # Efetua a chamada para a super classe Funcao enviando parametros para o construtor da super classe
        super().__init__(oper0, var1, oper1, var2, oper2, valor, letras, **kwargs)


class FuncaoObjetivo(Funcao):
    """Define a classe da função objeto da PL
    """
    def __init__(self, oper0='+', var1=0., oper1='+', var2=0., oper2='>=', valor=0., letras=['x', 'y'], **kwargs):
        # Efetua a chamada para a super classe Funcao enviando parametros para o construtor da super classe
        super().__init__(oper0, var1, oper1, var2, oper2, valor, letras, **kwargs)
        
        # Atribui o tipo de problema: maximização ou minimização
        self.objetivo = kwargs.get('objetivo')

    def setSolucao(self, solucao):
        """Adiciona a solução ótima na variável de instância
        
        Arguments:
            solucao {tuple} -- tupla das coordenadas da solução ótima
        """
        self.solucao = solucao
        self.valor = calcular(self.oper1, solucao[0] * self.var1, solucao[1] * self.var2)

        # Seta o valor do trono com o maior valor para utilizar na plotagem dos gráfico
        try:
            pre_trono = (self.valor / self.var1) if (self.valor /self.var1) > (self.valor / self.var2) else (self.valor / self.var2)
            self.trono[0] = pre_trono if pre_trono > self.trono[0] else self.trono[0]
        except Exception as ex:
            print('CALCULO TRONO->>',f'O valor do resultado da função ainda não foi definido\n{ex}')

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
            valor = calcular(restricao.oper1, restricao.var1 * x, restricao.var2 * y)
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
    mapa_max_min = {'max': max, 'min': min}

    # Retorna lista 
    if len(coordenadas_validas) == 0:
        return False

    # Adiciona a lista valores_solução, todos os resultados para as coordenadas da lista de coordenadas válidas
    for x, y in coordenadas_validas:
        valores_solucao.append(
            [calcular(funcao.oper1, funcao.var1 * x, funcao.var2 * y)]
        )

    # Atribui para solucao_otima o melhor resultado dos valores obtidos do calculo das coordenadas válidas
    # coordenadas_validas retorna a tupla do indice obtido pelo metodo index da lista de valores_solucao
    # obtido pela função mapa_min_max informando a chave funcao.objetivo e passando a lista de valores_solucao
    # para a função retornada
    solucao_otima = coordenadas_validas[valores_solucao.index(mapa_max_min.get(funcao.objetivo)(valores_solucao))]
    return solucao_otima


def lista_funcoes_obj_com_vertices_validos(funcaoObjetivo, lista_coordenadas, varx, vary):
    """Função para criar uma lista de resultados da lista de coordenadas válidas
    
    Arguments:
        funcaoObjetivo {FuncaoObjetivo} -- objeto função objetivo
        lista_coordenadas {list(tuple)} -- lista de tuplas com coordenadas válidas
        varx {str} -- icógnita utilizada para a variável x
        vary {str} -- icógnita utilizada para a variável y
    Returns:
        lista_funcao_objetivo {list(FuncaoObjetivo)} -- retorna uma lista com resultados de cada coordenada válida
    """
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
    pass


if __name__ == '__main__':
    main()
    