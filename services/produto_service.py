from typing import List
from models.produto import Produto
from repositories import produto_repository as repo

def listar_produtos() -> List[Produto]:
    return repo.carregar()

def criar_produto(nome: str, preco: float) -> Produto:
    produtos = repo.carregar()
    codigo = repo.proximo_codigo(produtos)

    produto = Produto(codigo, nome, preco)
    produtos.append(produto)

    repo.salvar(produtos)
    return produto
