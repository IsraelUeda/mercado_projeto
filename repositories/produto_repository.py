from sqlalchemy.orm import Session
from models.produto_model import Produto

def listar(db: Session):
    return db.query(Produto).all()

def criar(db: Session, nome: str, preco: float):
    produto = Produto(nome=nome, preco=preco)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto