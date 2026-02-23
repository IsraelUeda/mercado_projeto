from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome: str
    preco: float

class ProdutoResponse(BaseModel):
    codigo: int
    nome: str
    preco: float

    class Config:
        from_attributes = True