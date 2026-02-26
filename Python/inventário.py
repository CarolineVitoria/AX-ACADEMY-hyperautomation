
dicionario = {"comida": [], "medicina": []}

def somaItems(inventario, categoria):
    return sum(
        qtd for _, qtd in inventario[categoria]
    )


def inventario(nome, quantidade, categoria):

    print("O item inserido é: ")
    print(nome, quantidade, categoria)

    item = [(nome, quantidade)]

    if categoria in dicionario:
        dicionario[categoria].append(item)
    else:
        print("Categoria não disponível")



qtd_chamada = int(input("Digite a quantidade de items para inserir: "))
contador = 0

while qtd_chamada>contador:
    item = input("Digite o item: ")
    print(item.split())
    nome, quantidade, categoria = item.split()
    inventario(nome, quantidade, categoria)
    contador+=1

comidaTotal = print("Quantidade de comida: ", somaItems(dicionario, "comida"))
remedioTotal = print("Quantidade de Remédio: ", somaItems(dicionario, "medicina"))
