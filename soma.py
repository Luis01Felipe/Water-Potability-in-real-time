def soma(a, b):
    return a+b


stop = False
result = 0

while not stop:
    print("Insira um numero para somar, ou pressione 'enter' para sair")
    number = input()
    if number == "":
        stop = True
    else:
        result = soma(result, int(number))
        print(result)

print("O resultado final é: ", result)


