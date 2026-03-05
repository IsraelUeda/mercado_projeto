from sqlalchemy.orm import Session
from repositories import produto_repository

def listar_produtos(db: Session):
    return produto_repository.listar(db)

def criar_produto(db: Session, nome: str, preco: float):
    return produto_repository.criar(db, nome, preco)

def excluir_produto(db: Session, produto_id: int):
    return produto_repository.excluir(db, produto_id)