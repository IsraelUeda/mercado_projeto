from sqlalchemy.orm import Session
from repositories import carrinho_repository, produto_repository
from models.carrinho_model import ItemCarrinho


def criar_carrinho(db: Session):
    return carrinho_repository.criar_carrinho(db)


def adicionar_item(db: Session, carrinho_id: int, produto_id: int, quantidade: int, valor_unitario: float):
    # 1. Verifica se o carrinho existe e está ativo
    carrinho = carrinho_repository.buscar_carrinho(db, carrinho_id)
    if not carrinho or carrinho.status != "ativo":
        raise Exception("Carrinho inválido ou já finalizado.")

    # 2. Busca o produto na prateleira da loja para saber o estoque atual
    produto = produto_repository.buscar_produto(db, produto_id)
    if not produto:
        raise Exception("Produto não encontrado no banco de dados.")

    # 3. [Inferência] Primeira trava de segurança: o cliente pediu mais do que tem na loja inteira?
    if produto.quantidade_estoque < quantidade:
        raise Exception(f"Estoque insuficiente. Temos apenas {produto.quantidade_estoque} unidades disponíveis.")

    # 4. Verifica se o produto já está no carrinho do cliente
    item_existente = carrinho_repository.buscar_item(db, carrinho_id, produto_id)

    if item_existente:
        # 5. [Inferência] Segunda trava de segurança: a soma do que já está no carrinho 
        # com o que o cliente quer adicionar agora ultrapassa o estoque da loja?
        nova_quantidade_total = item_existente.quantidade + quantidade
        
        if produto.quantidade_estoque < nova_quantidade_total:
            raise Exception(f"A soma excede o estoque. Você já tem {item_existente.quantidade} no carrinho e o estoque máximo é {produto.quantidade_estoque}.")
            
        item_existente.quantidade = nova_quantidade_total
        db.commit()
        return item_existente

    # 6. Se o item não estava no carrinho e passou na checagem de estoque, criamos um novo
    novo_item = ItemCarrinho(
        carrinho_id=carrinho_id,
        produto_id=produto_id,
        quantidade=quantidade,
        valor_unitario=valor_unitario
    )

    return carrinho_repository.adicionar_item(db, novo_item)

def buscar_carrinho(db: Session, carrinho_id: int):
    # Faz a ponte repassando o pedido para o repositório (que é quem fala com o banco)
    return carrinho_repository.buscar_carrinho(db, carrinho_id)