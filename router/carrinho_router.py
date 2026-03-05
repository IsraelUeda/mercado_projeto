from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from services import carrinho_service
from schemas.carrinho_schema import ItemCreate, CarrinhoResponse

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])


@router.post("/")
def criar(db: Session = Depends(get_db)):
    return carrinho_service.criar_carrinho(db)


@router.post("/{carrinho_id}/item")
def adicionar(carrinho_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return carrinho_service.adicionar_item(
        db,
        carrinho_id,
        item.produto_id,
        item.quantidade,
        item.valor_unitario
    )
