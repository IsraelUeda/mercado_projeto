from sqlalchemy.orm import Session
from repositories import carrinho_repository
from models.carrinho_model import ItemCarrinho


def criar_carrinho(db: Session):
    return carrinho_repository.criar_carrinho(db)


def adicionar_item(db: Session, carrinho_id: int, produto_id: int, quantidade: int, valor_unitario: float):
    carrinho = carrinho_repository.buscar_carrinho(db, carrinho_id)

    if not carrinho or carrinho.status != "ativo":
        raise Exception("Carrinho inválido")

    item_existente = carrinho_repository.buscar_item(db, carrinho_id, produto_id)

    if item_existente:
        item_existente.quantidade += quantidade
        db.commit()
        return item_existente

    novo_item = ItemCarrinho(
        carrinho_id=carrinho_id,
        produto_id=produto_id,
        quantidade=quantidade,
        valor_unitario=valor_unitario
    )

    return carrinho_repository.adicionar_item(db, novo_item)