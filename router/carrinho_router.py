from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services import carrinho_service
from schemas.carrinho_schema import ItemCreate, CarrinhoResponse
from pydantic import BaseModel


router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

class ItemUpdate(BaseModel):
    quantidade: int

@router.post("/")
def criar(db: Session = Depends(get_db)):
    return carrinho_service.criar_carrinho(db)

@router.post("/{carrinho_id}/item")
def adicionar(carrinho_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    try:
        # [Inferência] Tenta adicionar. Se o service barrar por falta de estoque, cai no except
        return carrinho_service.adicionar_item(
            db,
            carrinho_id,
            item.produto_id,
            item.quantidade,
            item.valor_unitario
        )
    except Exception as e:
        # [Inferência] Repassa a mensagem de erro exata para o JavaScript ler
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{carrinho_id}", response_model=CarrinhoResponse)
def listar_carrinho(carrinho_id: int, db: Session = Depends(get_db)):
    # Busca no banco
    carrinho = carrinho_service.buscar_carrinho(db, carrinho_id)
    
    if not carrinho:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        
    return carrinho

@router.put("/{carrinho_id}/item/{produto_id}")
def atualizar_quantidade_item(
    carrinho_id: int, 
    produto_id: int, 
    item_update: ItemUpdate, 
    db: Session = Depends(get_db)
):
    try:
        # [Especulação] Esta função precisará ser construída no carrinho_service.py a seguir
        item_atualizado = carrinho_service.atualizar_quantidade(
            db=db, 
            carrinho_id=carrinho_id, 
            produto_id=produto_id, 
            nova_quantidade=item_update.quantidade
        )
        return item_atualizado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/{carrinho_id}/finalizar")
def finalizar_compra(carrinho_id: int, db: Session = Depends(get_db)):
    try:
        # Chama a função que criamos no passo anterior
        carrinho_finalizado = carrinho_service.finalizar_carrinho(db, carrinho_id)
        return {"mensagem": "Compra finalizada com sucesso!", "status": carrinho_finalizado.status}
    except Exception as e:
        # Devolve o erro para a tela caso o estoque tenha acabado no meio tempo
        raise HTTPException(status_code=400, detail=str(e))