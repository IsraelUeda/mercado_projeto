from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base

class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="ativo")

    itens = relationship("ItemCarrinho", back_populates="carrinho")


class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"))
    produto_id = Column(Integer)
    quantidade = Column(Integer)
    valor_unitario = Column(Float)

    carrinho = relationship("Carrinho", back_populates="itens")