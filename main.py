from fastapi import FastAPI
from schemas.produto_schema import ProdutoCreate, ProdutoResponse
from services import produto_service

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API do mercado rodando"}

@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos():
    return produto_service.listar_produtos()

@app.post("/produtos", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate):
    return produto_service.criar_produto(
        produto.nome,
        produto.preco
    )
