class bloco:
    def __init__(self, conteudo: str = '', tamanho_limite: int = 0):
        self.conteudo = conteudo
        self.tamanho_limite = tamanho_limite

    def __str__(self) -> str:
        return self.conteudo
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def cheio(self):
        return len(self.conteudo) == self.tamanho_limite
    
    def escrever(self, conteudo: str):
        if self.cheio():
            raise Exception('Bloco cheio')
        if not self.comporta(conteudo):
            raise Exception('Tamanho do conteúdo maior que o limite do bloco')
        self.conteudo += conteudo
    
    def quantidade_que_comporta(self):
        return self.tamanho_limite - len(self.conteudo)

    def comporta(self, conteudo: str):
        return len(conteudo) <= self.quantidade_que_comporta()

    def limpar(self):
        self.conteudo = ''



