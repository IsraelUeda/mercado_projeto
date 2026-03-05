from sqlalchemy.orm import Session
from models.carrinho_model import Carrinho, ItemCarrinho


def criar_carrinho(db: Session):
    carrinho = Carrinho()
    db.add(carrinho)
    db.commit()
    db.refresh(carrinho)
    return carrinho


def buscar_carrinho(db: Session, carrinho_id: int):
    return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()


def buscar_item(db: Session, carrinho_id: int, produto_id: int):
    return db.query(ItemCarrinho).filter(
        ItemCarrinho.carrinho_id == carrinho_id,
        ItemCarrinho.produto_id == produto_id
    ).first()


def adicionar_item(db: Session, item: ItemCarrinho):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item