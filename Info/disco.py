class bloco:

    pass

class disco:
    def __init__(self, tamanho_maximo: int, tamanho_blocos: int, tamanho_inodes: int):
        self.tamanho_maximo = tamanho_maximo
        self.tamanho_blocos = tamanho_blocos
        self.tamanho_inodes = tamanho_inodes
        self.blocos = []
        self.inodes = []
        self.bitmap_blocos_livres = []
        self.bitmap_blocos_ocupados = []
        self.bitmap_inodes_livres = []
        self.bitmap_inodes_ocupados = []