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

def excluir(db: Session, codigo_produto: int):
    """
    Busca o produto pelo CÓDIGO e o remove do banco de dados.
    """
    
    produto = db.query(Produto).filter(Produto.codigo == codigo_produto).first()
    
    if produto:
        db.delete(produto)
        db.commit()
        return True 
    
    return False