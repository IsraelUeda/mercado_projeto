from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal,engine
from services import produto_service
from schemas.produto_schema import ProdutoCreate, ProdutoResponse
from models.produto_model import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependência para abrir/fechar conexão automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return produto_service.listar_produtos(db)

@app.post("/produtos", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.criar_produto(db, produto.nome, produto.preco)