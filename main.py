from fastapi import FastAPI, HTTPException
from typing import List

from models.produto import Produto
from schemas.produto_schema import ProdutoSchema
from repositories.produto_repository import (
    carregar_produtos,
    salvar_produtos,
    gerar_codigo
)

app = FastAPI(title="API Mercado")

@app.get("/produtos", response_model=List[ProdutoSchema])
def listar_produtos():
    produtos = carregar_produtos()
    return [p.to_dict() for p in produtos]


@app.post("/produtos", response_model=ProdutoSchema)
def cadastrar_produto(produto: ProdutoSchema):
    produtos = carregar_produtos()

    novo_produto = Produto(
        codigo=gerar_codigo(produtos),
        nome=produto.nome,
        preco=produto.preco
    )

    produtos.append(novo_produto)
    salvar_produtos(produtos)

    return novo_produto.to_dict()
