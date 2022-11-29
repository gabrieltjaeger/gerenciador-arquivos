from .disco import disco

class bloco:
    def __init__(self, ref_disco: disco): ## 4KB, TÁ COMO TESTE
        self.conteudo = ''
        self.ref_disco = ref_disco
        self.tamanho_limite = self.ref_disco.tamanho_blocos * 1024
        self.ref_disco.adicionar_bloco(self)

    def __str__(self) -> str:
        return self.conteudo
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, bloco):
            return self is __o
        return False
        

    def __hash__(self) -> int:
        return id(self)

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

    def para_texto(self):
        texto = ''
        texto += str(self.conteudo)
        if not self.cheio():
            texto += '"' + '0' * (int(self.quantidade_que_comporta()) - 1)
        return texto



