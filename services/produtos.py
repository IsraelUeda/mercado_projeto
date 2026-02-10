import json
from pathlib import Path

ARQUIVO = Path("data/produtos.json")

def carregar_produtos() -> list:
    if not ARQUIVO.exists():
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_produtos(produtos: list) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

def cadastrar_produto(nome: str, preco: float) -> dict:
    produto = {
        "nome": nome,
        "preco": preco
    }
    return produto

from services.produtos import carregar_produtos

@app.get("/produtos")
def listar_produtos():
    return carregar_produtos()
