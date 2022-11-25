class usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return self.__str__()
