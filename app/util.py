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
    resultado = list()
    processada = expressao

    processada = processada.replace(' ', '')

    if processada[0] not in '-+':
        processada = f'+{processada}'

    for i in '= < >':
        if '<=' not in processada and '>=' not in processada:
            processada = processada.replace(i, f' {i} ')

    for i in '+ - <= >='.split():
        processada = processada.replace(i, f' {i} ')

    termos = processada.split()
    print('TERMOS->>',termos)

    if len(termos) == 6:
        if varx not in termos[1]:
            return f'Atenção! A letra da 1º icógnita não corresponte com a variável da expressão informada: "{expressao}".'
        elif vary not in termos[3]:
            return f'Atenção! A letra da 2º icógnita não corresponte com a variável da expressão informada: "{expressao}".'
    if len(termos) == 4:
        if varx not in termos[1] and vary not in termos[1]:
            return f'Atenção! A letra da expressão informada: "{expressao}", não corresponde com nenhuma das variáveis.'
        


    for i, termo in enumerate(tuple(termos)):
        if varx in termo:
            temp = f'1{termo}' if termo[0] not in '0123456789' else termo
            resultado.append(temp)
        elif vary in termo:
            temp = f'1{termo}' if termo[0] not in '0123456789' else termo
            resultado.append(temp)
        else:
            resultado.append(termo)

    if len(resultado) == 4 and varx not in ''.join(resultado):
        resultado.insert(0, '+')
        resultado.insert(1, '0x')
    elif len(resultado) == 4 and vary not in ''.join(resultado):
        resultado.insert(2, '+')
        resultado.insert(3, '0y')

    if resultado[-1][-1] not in '0123456789':
        resultado[-1] = f'{0.0}'
    normalizado = ' '.join(resultado)
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
