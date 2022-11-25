from datetime import datetime

from .bloco import bloco
from .usuario import usuario


class inode:
    def __init__(self, nome: str, criador: usuario, apontador_inode_pai, apontador_inodes: list = [], apontador_blocos: list = []):
        self.nome = nome
        self.criador = criador
        self.dono = criador
        self.tamanho = 0
        self.data_criacao = datetime.now()
        self.data_modificacao = datetime.now()
        self.apontador_blocos = apontador_blocos
        self.apontador_inodes = apontador_inodes
        self.apontador_inode_pai = apontador_inode_pai

    def __str__(self) -> str:
        caminho = []
        inode_atual = self
        while inode_atual.apontador_inode_pai is not None:
            caminho.append(inode_atual.nome)
            inode_atual = inode_atual.apontador_inode_pai
        caminho.append(inode_atual.nome)
        caminho.reverse()
        saida = '/'.join(caminho)
        if saida[0:2] == '//':
            saida = saida[1:]
        return saida

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def tipo(self):
        if self.apontador_blocos is None:
            # É um diretório
            return 'd'
        if self.apontador_inodes is None:
            # É um arquivo
            return 'a'
        raise Exception('Tipo de inode não identificado')
    
    def listar(self):
        if self.tipo == 'd':
            return self.apontador_inodes
        else:
            return False
        
    def adicionar_inode(self, inode):
        self.apontador_inodes.append(inode)
    
