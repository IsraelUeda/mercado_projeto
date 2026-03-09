from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    quantidade_estoque: int

class ProdutoResponse(BaseModel):
    codigo: int
    nome: str
    preco: float
    quantidade_estoque: int

    class Config:
        from_attributes = True