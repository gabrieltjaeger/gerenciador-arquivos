from datetime import datetime

from .bloco import bloco
from . import disco
from . import usuario


class inode:
    def __init__(self, nome: str, criador: usuario, apontador_inode_pai, ref_disco: disco, apontador_inodes: list = [], apontador_blocos: list = []):
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
        self.ref_disco = ref_disco
        self.ref_disco.adicionar_inode(self)
        self.limite_de_blocos = ((self.ref_disco.tamanho_inodes * 1024) - 300) // (len(str(self.ref_disco.quantidade_blocos)))
        self._tipo = self.get_tipo()

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

    def __hash__(self) -> int:
        return id(self)

    def get_inode(self, nome):
        for _inode in self.apontador_inodes:
            if _inode.nome == nome:
                if _inode is self:
                    continue
                return _inode

    def get_tipo(self):
        if self.apontador_blocos is None:
            # É um diretório
            return 'd'
        if self.apontador_inodes is None:
            # É um arquivo
            return 'a'
    
    def set_tipo(self, tipo):
        if tipo == 'd':
            self.apontador_blocos = None
        elif tipo == 'a':
            self.apontador_inodes = None
        else:
            raise Exception('Tipo de inode não identificado')
        self._tipo = tipo
            
    @property
    def tipo(self):
        return self._tipo

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
                if self.comporta_novo_bloco():
                    self.apontador_blocos.append(bloco(self.ref_disco))
                else:
                    raise Exception(f'{self} não comporta mais blocos.')
            bloco_atual: bloco = self.apontador_blocos[-1]
            if bloco_atual.comporta(conteudo):
                bloco_atual.escrever(conteudo)
            else:
                # Quantidade de caracteres que o bloco comporta
                qtd_comporta = bloco_atual.quantidade_que_comporta()
                bloco_atual.escrever(conteudo[:qtd_comporta])
                if self.comporta_novo_bloco():
                    self.apontador_blocos.append(bloco(self.ref_disco))
                else:
                    raise Exception(f'{self} não comporta mais blocos.')
                self.escrever(conteudo[qtd_comporta:])
            self.tamanho += 1
            self.data_modificacao = datetime.now()
        else:
            raise Exception(f'{self} não é um arquivo.')

    def comporta_novo_bloco(self):
        return len(self.apontador_blocos) < self.limite_de_blocos
        
    def ler(self):
        if self.tipo == 'a':
            conteudo = ''
            for bloco in self.apontador_blocos:
                conteudo += bloco.conteudo
            return conteudo
        else:
            raise Exception(f'{self} não é um arquivo.')
        
    def limpar(self):
        if self.tipo == 'a':
            self.apontador_blocos = []
            self.tamanho = 0
            self.data_modificacao = datetime.now()
        elif self.tipo == 'd':
            self.apontador_inodes = []
            self.qtd_inodes = 0
            self.data_modificacao = datetime.now()
        else:
            raise Exception(f'{self} não é um arquivo ou diretório.')

    def para_texto(self):
        texto = ''
        nome = str(self.nome)
        nome = nome[nome.rfind('/')+1:]
        if len(nome) < 260:
            nome += '"'
            if len(nome) < 260:
                nome += '0' * (260 - len(nome))
        texto += nome
        tamanho = str(self.tamanho)
        if len(tamanho) < 10:
            tamanho = '0' * (10 - len(tamanho)) + tamanho
        texto += tamanho
        data_criacao = ''
        dia = str(self.data_criacao.day)
        if len(dia) < 2:
            dia = '0' + dia
        mes = str(self.data_criacao.month)
        if len(mes) < 2:
            mes = '0' + mes
        ano = str(self.data_criacao.year)
        if len(ano) < 4:
            ano = '0' * (4 - len(ano)) + ano
        hora = str(self.data_criacao.hour)
        if len(hora) < 2:
            hora = '0' * (2 - len(hora)) + hora
        minuto = str(self.data_criacao.minute)
        if len(minuto) < 2:
            minuto = '0' * (2 - len(minuto)) + minuto
        data_criacao = dia + mes + ano + hora + minuto
        texto += data_criacao
        data_modificacao = ''
        dia = str(self.data_modificacao.day)
        if len(dia) < 2:
            dia = '0' + dia
        mes = str(self.data_modificacao.month)
        if len(mes) < 2:
            mes = '0' + mes
        ano = str(self.data_modificacao.year)
        if len(ano) < 4:
            ano = '0' * (4 - len(ano)) + ano
        hora = str(self.data_modificacao.hour)
        if len(hora) < 2:
            hora = '0' * (2 - len(hora)) + hora
        minuto = str(self.data_modificacao.minute)
        if len(minuto) < 2:
            minuto = '0' * (2 - len(minuto)) + minuto
        data_modificacao = dia + mes + ano + hora + minuto
        texto += data_modificacao
        # From self.ref_disco, find the inode's position
        posicao_pai = ''
        if self.apontador_inode_pai is None:
            posicao_pai = '0' * len(str(self.ref_disco.quantidade_inodes))
        else:
            pai = str(self.apontador_inode_pai)
            if pai == '/':
                pai = self.apontador_inode_pai.nome
            posicao_pai = list(map(str, list(self.ref_disco.bitmap_inodes.keys()))).index(pai)
            if len(str(posicao_pai)) < (x := len(str(self.ref_disco.quantidade_inodes))):
                posicao_pai = '0' * (x - len(str(posicao_pai))) + str(posicao_pai)
        texto += posicao_pai
        blocos = ''
        if self.apontador_blocos is None:
            blocos = '0' * len(str(self.ref_disco.quantidade_blocos)) * self.limite_de_blocos
        else:
            for bloco in self.apontador_blocos:
                posicao_bloco = list(self.ref_disco.bitmap_blocos.keys()).index(bloco)
                if len(str(posicao_bloco)) < (x := len(str(self.ref_disco.quantidade_blocos))):
                    posicao_bloco = '0' * (x - len(str(posicao_bloco))) + str(posicao_bloco)
                blocos += posicao_bloco
            if len(self.apontador_blocos) < self.limite_de_blocos:
                blocos += '0' * len(str(self.ref_disco.quantidade_blocos)) * (self.limite_de_blocos - len(self.apontador_blocos))
        texto += blocos
        if len(texto) < (x:=(self.ref_disco.tamanho_inodes*1024)):
            texto += '"'
            if len(texto) < x:
                texto += '0' * (x - len(texto))
            texto = texto[:-1] + self.tipo
        return texto
        



