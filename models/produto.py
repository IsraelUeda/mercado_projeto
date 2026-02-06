from utils.helper import formata_float_str_moeda

class Produto:
    def __init__(self, codigo: int, nome: str, preco: float) -> None:
        self.__codigo = codigo
        self.__nome = nome
        self.__preco = preco

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def preco(self) -> float:
        return self.__preco

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "preco": self.preco
        }

    @staticmethod
    def from_dict(dados: dict):
        return Produto(
            dados["codigo"],
            dados["nome"],
            dados["preco"]
        )

    def __str__(self) -> str:
        return (
            f'Código: {self.codigo}\n'
            f'Nome: {self.nome}\n'
            f'Preço: {formata_float_str_moeda(self.preco)}'
        )
