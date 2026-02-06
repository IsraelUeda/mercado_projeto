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
    """
    Lê o arquivo JSON de produtos e converte cada item
    em um objeto Produto.

    Retorna:
        Lista de objetos Produto.
        Se o arquivo não existir, retorna uma lista vazia.
    """

def salvar_produtos(produtos: List[Produto]) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(
            [p.to_dict() for p in produtos],
            f,
            indent=4,
            ensure_ascii=False
        )
    """
    Salva a lista de produtos no arquivo JSON.
    Cada produto é convertido para dicionário antes de salvar.
    """

def gerar_codigo(produtos: List[Produto]) -> int:
    """
    Gera um novo código único para o produto.
    O código é sempre maior que o maior já existente.
    """
    if not produtos:
        return 1
    return max(p.codigo for p in produtos) + 1




produtos: List[Produto] = []
carrinho: Dict[int, int] = {}




def main() -> None:
    menu()


def menu() -> None:
    """
    Exibe o menu principal e controla o fluxo do programa.
    O menu fica em loop até o usuário escolher sair.
    """

    while True:
        print("=====================================")
        print("============= Bem-vindo(a) ==========")
        print("================ store ==============")
        print("=====================================")

        print("1 - Cadastrar produto")
        print("2 - Listar produto")
        print("3 - Comprar produto")
        print("4 - Visualizar carrinho")
        print("5 - Fechar pedido")
        print("6 - Sair")

        try:
            opcao = int(input("Qual sua opção? "))

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
                break
            else:
                print("Opção inválida")

        except ValueError:
            print("Entrada inválida. Digite apenas números.")

        sleep(1)



def cadastrar_produto() -> None:
    """
    Solicita dados do usuário, cria um produto
    e salva no arquivo JSON.
    """

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
    return

def listar_produto() -> None:
    """
    Carrega e exibe todos os produtos cadastrados.
    """
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
    return

def comprar_produto() -> None:
    """
    Permite adicionar produtos ao carrinho em loop,
    até o usuário digitar 'exit'.
    """
    produtos = carregar_produtos()

    if not produtos:
        print('Ainda não existem itens para vender.')
        sleep(2)
        return

    def adicionar_ao_carrinho(produto: Produto) -> None:
        if produto.codigo in carrinho:
            carrinho[produto.codigo] += 1
        else:
            carrinho[produto.codigo] = 1

        print(f'Produto {produto.nome} adicionado ao carrinho')

    while True:
        print('\nProdutos disponíveis:')
        for produto in produtos:
            print(produto)
            print('----------------')

        print('Informe outro código ou digite "exit" para voltar ao menu')

        entrada = input('> ').strip()

        if entrada.lower() == 'exit':
            break

        if not entrada:
            print('Entrada vazia. Digite um código ou "exit".')
            continue

        try:
            codigo = int(entrada)
        except ValueError:
            print('Entrada inválida. Digite um número ou "exit".')
            continue

        produto = pega_produto_por_codigo(codigo)

        if produto:
            adicionar_ao_carrinho(produto)
        else:
            print('Produto não encontrado')

        sleep(1)


def fechar_pedido() -> None:
    """
    Exibe os produtos do carrinho,
    calcula o valor total e limpa o carrinho.
    """
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
    return

def pega_produto_por_codigo(codigo: int) -> Produto:
    """
    Retorna um produto pelo código.
    Se não existir, retorna None.
    """
    produtos = carregar_produtos()

    for produto in produtos:
        if produto.codigo == codigo:
            return produto
    return None


if __name__ == '__main__':
    main()