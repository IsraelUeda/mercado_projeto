from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal,engine
from services import produto_service, carrinho_service
from fastapi import HTTPException
from schemas.produto_schema import ProdutoCreate, ProdutoResponse
from models.produto_model import Base
from fastapi.staticfiles import StaticFiles
from router import carrinho_router
from repositories import produto_repository,carrinho_repository

app = FastAPI()

app.include_router(carrinho_router.router)
app.mount("/front", StaticFiles(directory="static", html=True), name="static")

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
    return produto_service.criar_produto(db, produto.nome, produto.preco, produto.quantidade_estoque)

@app.delete("/produtos/{codigo}")
def deletar_produto(codigo: int, db: Session = Depends(get_db)):
    """
    Recebe o pedido de exclusão, pega o código da URL e manda para o repositório.
    """
    # Chama a função excluir_produto (que você colocou no seu arquivo de serviços)
    # ou chama direto o produto_repository.excluir(db, codigo) dependendo de como você organizou
    sucesso = produto_repository.excluir(db, codigo)
    
    if sucesso:
        # Se deu certo, avisa o JavaScript que tudo correu bem (Status 200 OK padrão)
        return {"mensagem": f"Produto {codigo} excluído com sucesso!"}
    else:
        # Se a função retornou False, é porque esse código não existe no banco
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
