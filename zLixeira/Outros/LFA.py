# Trabalho para entrega de LFA: Automoto de pilha
# Luis Felipe Moraes Gomes Couto, CC5A68

def verificar_se_letra(char):
    return char.isalpha()


def verificar_se_operador(char):
    return char in ['+', '-', '*', '/']


def verificar_expressao_valida(pilha):
    if len(pilha) == 3:
        valid = verificar_se_letra(pilha[0]) and verificar_se_operador(pilha[1]) and verificar_se_letra(pilha[2])
    elif len(pilha) == 2:
        valid = verificar_se_letra(pilha[0]) and verificar_se_operador(pilha[1])
    elif len(pilha) == 1:
        valid = verificar_se_letra(pilha[0])
    else:
        valid = all(verificar_se_letra(pilha[i]) or verificar_se_operador(pilha[i]) for i in range(1, len(pilha) - 1))
        valid = valid and pilha[0] == '(' and pilha[-1] == ')'
    print(f"Checando expressão: {pilha}, validade: {valid}")
    return valid


def automato(string):
    pilha = []
    for i in range(len(string)):
        char = string[i]
        if char == '(':
            # Verificar se o caractere anterior é uma letra
            if i > 0 and verificar_se_letra(string[i - 1]):
                print(f"Expressão inválida: {string}")
                return False
            pilha.append(char)
        elif char == ')':
            temp_pilha = []
            while pilha and pilha[-1] != '(':
                temp_pilha.append(pilha.pop())
            if not pilha or not verificar_expressao_valida(temp_pilha[::-1]):
                print(f"Expressão inválida: {string}")
                return False
            pilha.pop()  # remove '('
        elif verificar_se_letra(char) or verificar_se_operador(char):
            pilha.append(char)
        else:
            print(f"Caracter inválido '{char}' na: {string}, validade: Falso, Caracteres válidos: '(', ')', 'x', 'y', "
                  f"'z', '+', '-', '*', '/'")
            return False
    if len(pilha) != 0 and pilha[-1] == '(':
        print(f"Faltou fechar parênteses: {string}")
        return False
    if len(pilha) > 0 and not verificar_expressao_valida(pilha):
        print(f"Expressão inválida no final: {string}")
        return False
    return True


# Loop princiapl onde usuario pode testar expressões
while True:
    entrada_usuario = input("Digite a expressão: ")
    automato(entrada_usuario)
    escolha = input("Deseja testar outra expressão? (s/n): ")
    if escolha.lower() == 'n':
        break

# Expressões para teste
# automato('x')  # True
# automato('(x)')  # True
# automato('(x+y)')  # True
# automato('(x-z)')  # True
# automato('(x*x)')  # True
# automato('(z/y)')  # True
# automato('(z/y)')  # True
# automato('(x%y)')  # False
# automato('(x+z')  # False
# automato('x+z')  # False
# automato('xz')  # False
# automato('+z')  # False
