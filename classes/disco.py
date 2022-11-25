from .bloco import bloco
from .inode import inode

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
    
    def criar_bloco(self, inode: inode) -> bloco:
        _bloco = bloco(self.tamanho_blocos)
        self.blocos.append(_bloco)
        self.bitmap_blocos_ocupados.append(_bloco)
        return _bloco
    
    def criar_arquivo(self, inode: inode) -> inode:
        self.inodes.append(inode)
        self.bitmap_inodes_ocupados.append(inode)
        bloco = self.criar_bloco(self.tamanho_blocos)
        inode.adicionar_bloco(bloco)
    
    def escrever_bloco(self, bloco: bloco, dados: str) -> None:
        bloco.escrever(dados)
    

