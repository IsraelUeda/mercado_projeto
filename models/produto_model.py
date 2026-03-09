from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    codigo = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, default=0)