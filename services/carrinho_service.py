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

def atualizar_quantidade(db: Session, carrinho_id: int, produto_id: int, nova_quantidade: int):
    # 1. Verifica se o carrinho é válido
    carrinho = carrinho_repository.buscar_carrinho(db, carrinho_id)
    if not carrinho or carrinho.status != "ativo":
        raise Exception("Carrinho inválido ou já finalizado.")

    # 2. Verifica se o item realmente está no carrinho do cliente
    item_existente = carrinho_repository.buscar_item(db, carrinho_id, produto_id)
    if not item_existente:
        raise Exception("Item não encontrado no carrinho.")

    # 3.Regra de exclusão: se o cliente diminuir a quantidade para 0, removemos o item
    if nova_quantidade <= 0:
        # Precisaremos garantir que esta função exista no repositório
        carrinho_repository.remover_item(db, item_existente)
        return {"mensagem": "Item removido com sucesso."}

    # 4. Busca o produto na prateleira para checar o estoque
    produto = produto_repository.buscar_produto(db, produto_id)
    if not produto:
        raise Exception("Produto não encontrado no banco de dados.")

    # 5. Trava de segurança: a nova quantidade ultrapassa o estoque?
    if produto.quantidade_estoque < nova_quantidade:
        raise Exception(f"Estoque insuficiente. O limite máximo é de {produto.quantidade_estoque} unidades.")

    # 6. Se passou em todas as checagens, atualiza o valor no banco
    item_existente.quantidade = nova_quantidade
    db.commit()
    db.refresh(item_existente)
    
    return item_existente

def finalizar_carrinho(db: Session, carrinho_id: int):
    # Busca o carrinho atual
    carrinho = carrinho_repository.buscar_carrinho(db, carrinho_id)
    if not carrinho or carrinho.status != "ativo":
        raise Exception("Carrinho não encontrado ou já finalizado.")

    # [Especulação] Garante que o cliente não tente finalizar um carrinho vazio
    if not carrinho.itens:
        raise Exception("Não é possível finalizar um carrinho vazio.")

    # [Inferência] Itera sobre cada item do carrinho para dar a baixa no estoque da loja
    for item in carrinho.itens:
        produto = produto_repository.buscar_produto(db, item.produto_id)
        
        if not produto:
            raise Exception(f"Produto ID {item.produto_id} não encontrado no banco.")
            
        # Última trava de segurança antes de fechar a compra
        if produto.quantidade_estoque < item.quantidade:
            raise Exception(f"Estoque insuficiente para o produto ID {produto.codigo}.")
            
        # [Inferência] A matemática real acontece aqui: subtrai o que foi comprado do estoque
        produto.quantidade_estoque -= item.quantidade

    # Muda o status para que este carrinho não possa mais ser alterado
    carrinho.status = "concluido"
    
    db.commit()
    db.refresh(carrinho)
    
    return carrinho