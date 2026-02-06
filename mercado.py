from typing import List, Dict
from time import sleep
import json
from models.produto import Produto

ARQUIVO = "produtos.json"

def carregar_produtos() -> List[Produto]:
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Produto.from_dict(p) for p in dados]
    except FileNotFoundError:
        return []

def salvar_produtos(produtos: List[Produto]) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(
            [p.to_dict() for p in produtos],
            f,
            indent=4,
            ensure_ascii=False
        )

def gerar_codigo(produtos: List[Produto]) -> int:
    if not produtos:
        return 1
    return max(p.codigo for p in produtos) + 1




produtos: List[Produto] = []
carrinho: Dict[int, int] = {}




def main() -> None:
    menu()

def menu() -> None:
    print("=====================================")
    print("============= Bem-vindo(a) ==========")
    print("================ store ==============")
    print("=====================================")


    print("selecione uma opção abaixo: ")
    print('1 - Cadastrar produto')
    print('2 - Listar produto')
    print('3 - Comprar produto')
    print('4 - Vizualizar carrinho')
    print('5 - Fechar pedido')
    print('6 - Sair')

    opcao:int = int(input("Qual sua opcão?"))

    if opcao == 1:
        cadastrar_produto()
    elif opcao == 2:
        listar_produto()
    elif opcao == 3:
        comprar_produto()
    elif opcao == 4:
        visualizar_carrinho()
    elif opcao == 5:
        fechar_pedido()
    elif opcao == 6:
        print("Volte sempre")
        sleep(2)
        exit(0)
    else:
        print("Opcao inválida")
        sleep(1)
        menu()


def cadastrar_produto() -> None:
    print('Cadastro de produto')
    print('===================')

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))

    produtos = carregar_produtos()

    codigo = gerar_codigo(produtos)
    produto = Produto(codigo, nome, preco)

    produtos.append(produto)
    salvar_produtos(produtos)

    print(f'O produto {produto.nome} foi cadastrado com sucesso')
    sleep(2)
    menu()

def listar_produto() -> None:
    produtos = carregar_produtos()

    if produtos:
        print("Listagem de produtos:")
        for produto in produtos:
            print(produto)
            print('----------------')
            sleep(1)
    else:
        print("Não há produtos cadastrados")

    sleep(2)
    menu()

def comprar_produto() -> None:
    produtos = carregar_produtos()

    def adicionar_ao_carrinho(produto: Produto) -> None:
        if produto.codigo in carrinho:
            carrinho[produto.codigo] += 1
        else:
            carrinho[produto.codigo] = 1

        print(f'Produto {produto.nome} adicionado ao carrinho')

    if produtos:
        print('Informe o código do produto:')
        for produto in produtos:
            print(produto)
            print('----------------')

        codigo = int(input())
        produto = pega_produto_por_codigo(codigo)

        if produto:
            adicionar_ao_carrinho(produto)
        else:
            print('Produto não encontrado')
    else:
        print('Ainda não existem itens para vender.')

    sleep(2)
    menu()

def visualizar_carrinho() -> None:
    if carrinho:
        print('Produtos no carrinho')

        for codigo, quantidade in carrinho.items():
            produto = pega_produto_por_codigo(codigo)
            if produto:
                print(produto)
                print(f'Quantidade: {quantidade}')
                print('--------------------')
                sleep(1)
    else:
        print("Ainda não existem produtos no carrinho.")

    sleep(2)
    menu()

def fechar_pedido() -> None:
    if carrinho:
        valor_total = 0
        print("Produtos no carrinho")

        for codigo, quantidade in carrinho.items():
            produto = pega_produto_por_codigo(codigo)
            if produto:
                print(produto)
                print(f'Quantidade: {quantidade}')
                valor_total += produto.preco * quantidade
                print('----------------')

        print(f'Valor total: {valor_total:.2f}')
        print('Volte sempre')

        carrinho.clear()
        sleep(3)
    else:
        print("Ainda não existem produtos no carrinho")

    sleep(2)
    menu()

def pega_produto_por_codigo(codigo: int) -> Produto:
    produtos = carregar_produtos()

    for produto in produtos:
        if produto.codigo == codigo:
            return produto
    return None


if __name__ == '__main__':
    main()