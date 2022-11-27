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
        self.qtd_inodes = 0

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

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, inode):
            return self is __o
        return False

    def get_inode(self, nome):
        for _inode in self.apontador_inodes:
            if _inode.nome == nome:
                if _inode is self:
                    continue
                return _inode

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

    def adicionar_inode(self, _inode):
        self.apontador_inodes.append(_inode)
        self.qtd_inodes += 1

    def remover_inode(self, inode):
        self.apontador_inodes.remove(inode)
        self.qtd_inodes -= 1

    def dir_vazio(self):
        if self.tipo == 'd':
            return self.qtd_inodes == 0
        raise Exception(f'{self} não é um diretório.')

    def mover(self, inode_pai, nome):
        self.apontador_inode_pai.remover_inode(self)
        self.apontador_inode_pai = inode_pai
        self.nome = nome
        self.apontador_inode_pai.adicionar_inode(self)

    def escrever(self, conteudo: str):
        if self.tipo == 'a':
            if len(self.apontador_blocos) == 0:
                self.apontador_blocos.append(bloco())
            bloco_atual: bloco = self.apontador_blocos[-1]
            if bloco_atual.comporta(conteudo):
                bloco_atual.escrever(conteudo)
            else:
                # Quantidade de caracteres que o bloco comporta
                qtd_comporta = bloco_atual.quantidade_que_comporta()
                bloco_atual.escrever(conteudo[:qtd_comporta])
                self.apontador_blocos.append(bloco())
                self.escrever(conteudo[qtd_comporta:])
            self.tamanho += len(conteudo)
            self.data_modificacao = datetime.now()
        else:
            raise Exception(f'{self} não é um arquivo.')

    def ler(self):
        if self.tipo == 'a':
            conteudo = ''
            for bloco in self.apontador_blocos:
                conteudo += bloco.conteudo
            return conteudo
        else:
            raise Exception(f'{self} não é um arquivo.')
