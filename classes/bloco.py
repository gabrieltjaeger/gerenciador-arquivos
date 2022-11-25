class bloco:
    def __init__(self, tamanho_bloco: int):
        self.tamanho = tamanho_bloco
        self.dados = ''

    def escrever(self, dados: str) -> None:
        self.dados = dados
        
    def __str__(self) -> str:
        return self.dados
    
    def __repr__(self) -> str:
        return self.__str__()