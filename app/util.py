"""Módulo para funções utilitárias
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""

def prepara_string_to_map(expressao, varx='x', vary='y'):
    """Normaliza a string para que seja mapeada para uma kwargs
    
    Arguments:
        expressao {str} -- expressão matemática de uma função linear com duas variáveis
    
    Keyword Arguments:
        varx {str} -- caracter utilizado para representar a variável x (default: {'x'})
        vary {str} -- caracter utilizado para representar a variável y (default: {'y'})
    
    Returns:
        normalizado {str} -- expressão normalizada pronta para o mapeamento em uma keyword args (kwargs)
    """
    # Verifica se as letras de varx e vary são iguais
    if varx.upper() == vary.upper():
        return f'Atenção! As letras da 1º e 2º variável dos rótulos devem ser diferentes.'

    # Inicia a lista que conterá o resultado após processamento da string
    resultado = list()

    # Atribui a string enviada por parâmetro para ser processada
    processada = expressao

    # Tira todos os espaços da string
    processada = processada.replace(' ', '')

    # Adiciona o sinal de '+' se no início da string se não conter nenhum sinal
    if processada[0] not in '-+':
        processada = f'+{processada}'

    # Efetua loop com cada sinal '= < >', para inserção de espaços na string
    for i in '= < >':
        # verifica se não há do operadores <= ou >= para efetuar a inserção dos espaços entre os operadores
        if '<=' not in processada and '>=' not in processada:
            processada = processada.replace(i, f' {i} ')


    # Efetua loop com cada sinal da lista ['+', '-', '<=', '>='], para inserção de espaços na string
    for i in '+ - <= >='.split():       # O método .split() retorna uma lista da string separada pelos espaços.
        processada = processada.replace(i, f' {i} ')

    # Cria uma lista de termos a partir da string, onde cada termo é parte da string separada por espaço
    termos = processada.split()

    # Efetua a verificação da correspondência entre as letras das restrições e as letras dos rótulos
    # se as letras não corresponderem, retorna a mensagem de Atenção!
    if len(termos) == 6:
        if varx not in termos[1]:
            return f'Atenção! A letra da 1º variável da expressão informada: "{expressao}", não corresponde com a letra "{varx}" do 1º rótulo.'
        elif vary not in termos[3]:
            return f'Atenção! A letra da 2º variável da expressão informada: "{expressao}", não corresponde com a letra "{vary}" do 2º rótulo.'
    if len(termos) == 4:
        if varx not in termos[1] and vary not in termos[1]:
            return f'Atenção! A letra da expressão informada: "{expressao}", não corresponde com nenhuma das variáveis.'
        
    # Inseri o numero 1 quando o termo da variavel não contiver numeros e adiciona todos os termos na lista resultado
    for i, termo in enumerate(tuple(termos)):
        if varx in termo:
            temp = f'1{termo}' if termo[0] not in '0123456789' else termo
            resultado.append(temp)
        elif vary in termo:
            temp = f'1{termo}' if termo[0] not in '0123456789' else termo
            resultado.append(temp)
        else:
            resultado.append(termo)

    # Inseri o sinal '+' e o valor '0' na posição correspondente da variável que não existir na expressão
    if len(resultado) == 4 and varx not in ''.join(resultado):
        resultado.insert(0, '+')
        resultado.insert(1, '0x')
    elif len(resultado) == 4 and vary not in ''.join(resultado):
        resultado.insert(2, '+')
        resultado.insert(3, '0y')

    if resultado[-1][-1] not in '0123456789':
        resultado[-1] = f'{0.0}'

    # Transforma a lista resultado em uma string juntando cada item da lista com um espaço entre eles
    normalizado = ' '.join(resultado)
    
    # retorna uma a expressão normalizada
    return normalizado


if __name__ == "__main__":
    """Instrução de decisão para rodar o código abaixo quando o módulo for executado como script
    """
    print(prepara_string_to_map('x+y<=L', 'x', 'y'))
    print(prepara_string_to_map('x+y=L', 'x', 'y'))
    print(prepara_string_to_map('10x+y<=L', 'x', 'y'))
    print(prepara_string_to_map('10x+y>=L', 'x', 'y'))
    print(prepara_string_to_map('10x-y>=1500', 'x', 'y'))
    print(prepara_string_to_map('10x+35y<=50', 'x', 'y'))
    print(prepara_string_to_map('-10x+35y<=L', 'x', 'y'))
    print(prepara_string_to_map('-10x+35y=L', 'x', 'y'))
    print(prepara_string_to_map('y<=5', 'x', 'y'))
    print(prepara_string_to_map('-x<8', 'x', 'y'))
    print(prepara_string_to_map('x>8', 'x', 'y'))
    print(prepara_string_to_map('-x>8', 'x', 'y'))
    print(prepara_string_to_map('+x>=8', 'x', 'y'))
