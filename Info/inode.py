from datetime import datetime
from Info.usuario import usuario

class inode:
    def __init__(self, nome: str, criador: usuario, apontador_bloco, apontador_inode_pai):
        self.nome = nome
        self.criador = criador
        self.dono = criador
        self.tamanho = 0
        self.data_criacao = datetime.now()
        self.data_modificacao = datetime.now()
        self.apontador_bloco = apontador_bloco
        self.apontador_inodes = []
        self.apontador_inode_pai = apontador_inode_pai

    def __str__(self) -> str:
        caminho = ''
        inode_atual = self
        while inode_atual.apontador_inode_pai is not None:
            caminho = '/' + inode_atual.nome + caminho
            inode_atual = inode_atual.apontador_inode_pai
        else:
          caminho = '/' + inode_atual.nome + caminho
        return caminho

    def __repr__(self) -> str:
        return self.__str__()