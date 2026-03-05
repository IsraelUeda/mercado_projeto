from pydantic import BaseModel
from typing import List

class ItemCreate(BaseModel):
    produto_id: int
    quantidade: int
    valor_unitario: float


class ItemResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    valor_unitario: float

    class Config:
        from_attributes = True


class CarrinhoResponse(BaseModel):
    id: int
    status: str
    itens: List[ItemResponse]

    class Config:
        from_attributes = True