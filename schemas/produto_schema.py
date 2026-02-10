from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    codigo: int
    nome: str
    preco: float

    class Config:
        from_attributes = True
