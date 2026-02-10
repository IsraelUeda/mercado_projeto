import json
from typing import List
from models.produto import Produto

ARQUIVO = "produtos.json"

def carregar() -> List[Produto]:
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Produto.from_dict(p) for p in dados]
    except FileNotFoundError:
        return []

def salvar(produtos: List[Produto]) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in produtos], f, indent=4)

def proximo_codigo(produtos: List[Produto]) -> int:
    if not produtos:
        return 1
    return max(p.codigo for p in produtos) + 1
