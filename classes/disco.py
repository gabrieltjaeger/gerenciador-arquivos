from collections import OrderedDict
from datetime import datetime
import os

from .bloco import bloco
from .inode import inode
from . import sistema_operacional

class disco:
    def __init__(self, tamanho_maximo: int, tamanho_blocos: int, tamanho_inodes: int, so: sistema_operacional):
        self.tamanho_maximo = tamanho_maximo
        self.tamanho_blocos = tamanho_blocos
        self.tamanho_inodes = tamanho_inodes
        self.so = so

        self.bitmap_blocos = OrderedDict() # inode: 0 ou 1
        self.bitmap_inodes = OrderedDict() # bloco: 0 ou 1

        self.quantidade_blocos = self.quantidade_inodes = self.limite()
        
    def limite(self) -> int:
        '''
        Retorna a quantidade máxima de blocos e inodes que o disco comporta,
        baseado no tamanho máximo do disco e no tamanho dos blocos e inodes.

        Assume que haverá também um bit para cada bloco e inode no bitmap.

        Nessa implementação, quantidade de blocos e inodes é a mesma. Porém,
        isso não é uma regra.
        '''
        quantidade_de_bytes_disco = self.tamanho_maximo * 1024 * 1024
        quantidade_de_bytes_por_bloco = self.tamanho_blocos * 1024
        quantidade_de_bytes_por_inode = self.tamanho_inodes * 1024
        # x: quantidade de blocos
        # y: quantidade de inodes
        # b: quantidade_de_bytes_por_bloco
        # i: quantidade_de_bytes_por_inode
        # m: bitmap; m = x + y
        # d: disco; d = x * b + y * i + m
        # d = x * b + y * i + x + y
        # se x = y, então: 
        # d = b * x + i * x + x + x
        # d = b * x + i * x + 2 * x
        # d = (b + i + 2) * x
        # d / (b + i + 2) = x
        return quantidade_de_bytes_disco // (quantidade_de_bytes_por_bloco + quantidade_de_bytes_por_inode + 2)
    
    def adicionar_bloco(self, bloco):
        # Se há espaço no disco para adicionar um bloco
        if len(self.bitmap_blocos) < self.quantidade_blocos:
            if bloco in self.bitmap_blocos:
                if self.bitmap_blocos[bloco] == 1:
                    return False
            self.bitmap_blocos[bloco] = 1
            return True
        return False

    def adicionar_inode(self, _inode):
        # Se há espaço no disco para adicionar um inode
        if len(self.bitmap_inodes) < self.quantidade_inodes:
            if _inode in self.bitmap_inodes:
                if self.bitmap_inodes[_inode] == 1:
                    return False
            self.bitmap_inodes[_inode] = 1
            return True
        return False
    
    def remover_bloco(self, bloco):
        if bloco in self.bitmap_blocos:
            if self.bitmap_blocos[bloco] == 1:
                self.bitmap_blocos[bloco] = 0
                return True
        return False
    
    def remover_inode(self, inode):
        if inode in self.bitmap_inodes:
            if self.bitmap_inodes[inode] == 1:
                for bloco in inode.apontador_blocos:
                    self.remover_bloco(bloco)
                inode.limpar()
                self.bitmap_inodes[inode] = 0
                return True
        return False
    
    def para_texto(self):
        # Se disco não existe, criar disco
        with open('disco.txt', 'w') as disco:
            disco.write('')

        for _, bit in self.bitmap_blocos.items():
            with open('disco.txt', 'a') as disco:
                disco.write(str(bit))
        if len(self.bitmap_blocos) < self.quantidade_blocos:
            with open('disco.txt', 'a') as disco:
                disco.write(str('0' * (self.quantidade_blocos - len(self.bitmap_blocos))))
        for _, bit in self.bitmap_inodes.items():
            with open('disco.txt', 'a') as disco:
                disco.write(str(bit))
        if len(self.bitmap_inodes) < self.quantidade_inodes:
            with open('disco.txt', 'a') as disco:
                disco.write(str('0' * (self.quantidade_inodes - len(self.bitmap_inodes))))
        for bloco, _ in self.bitmap_blocos.items():
            with open('disco.txt', 'a') as disco:
                disco.write(str(bloco.para_texto()))
        if len(self.bitmap_blocos) < self.quantidade_blocos:
            with open('disco.txt', 'a') as disco:
                disco.write(str('0' * (self.quantidade_blocos - len(self.bitmap_blocos)) * self.tamanho_blocos * 1024))
        for inode, _ in self.bitmap_inodes.items():
            with open('disco.txt', 'a') as disco:
                disco.write(str(inode.para_texto()))
        if len(self.bitmap_inodes) < self.quantidade_inodes:
            with open('disco.txt', 'a') as disco:
                disco.write(str('0' * (self.quantidade_inodes - len(self.bitmap_inodes)) * self.tamanho_inodes * 1024))
                
       
    def carregar(self, arquivo):
        with open(arquivo, 'r') as disco:
            texto = disco.read()
        bits_blocos = []
        bits_inodes = []
        for i in range(self.quantidade_blocos):
            bits_blocos.append(int(texto[i]))

        for i in range(self.quantidade_inodes):
            bits_inodes.append(int(texto[self.quantidade_blocos + i]))
        
        blocos = []
        for i in range(self.quantidade_blocos):
            bloco_texto = texto[self.quantidade_blocos + self.quantidade_inodes + i * self.tamanho_blocos * 1024 : self.quantidade_blocos + self.quantidade_inodes + (i + 1) * self.tamanho_blocos * 1024]
            _bloco = None
            if bloco_texto[-1] == '0':
                fim_bloco = bloco_texto.rfind('"0')
                if fim_bloco != 0:
                    _bloco = bloco(self)
                    _bloco.escrever(bloco_texto[:fim_bloco])
            elif bloco_texto[-1] == '"':
                bloco_texto = bloco_texto[:-1]
                _bloco = bloco(self)
                _bloco.escrever(bloco_texto)
            else:
                _bloco = bloco(self)
                _bloco.escrever(bloco_texto)
            blocos.append(_bloco)

        for i in range(len(bits_blocos)):
            _bloco = blocos[i]
            if _bloco is None:
                _bloco = str(i)
            self.bitmap_blocos[_bloco] = bits_blocos[i]

        inodes = []
        for i in range(self.quantidade_inodes):
            inode_texto = texto[self.quantidade_blocos + self.quantidade_inodes + self.tamanho_blocos * 1024 * self.quantidade_blocos + i * self.tamanho_inodes * 1024 : self.quantidade_blocos + self.quantidade_inodes + self.tamanho_blocos * 1024 * self.quantidade_blocos + (i + 1) * self.tamanho_inodes * 1024]
            _inode = None
            nome = inode_texto[:260]
            if '"' in nome:
                nome = nome[:nome.rfind('"')]

            tamanho = int(inode_texto[260:270])
            data_criacao = inode_texto[270:282]

            dia = int(data_criacao[:2])
            mes = int(data_criacao[2:4])
            ano = int(data_criacao[4:8])
            hora = int(data_criacao[8:10])
            minuto = int(data_criacao[10:12])
            if nome == len(nome) * '0':
                if dia == 0 and mes == 0 and ano == 0 and hora == 0 and minuto == 0:
                    inodes.append(None)    
                    continue

            data_criacao = datetime(ano, mes, dia, hora, minuto)
            data_modificacao = inode_texto[282:294]
            dia = int(data_modificacao[:2])
            mes = int(data_modificacao[2:4])
            ano = int(data_modificacao[4:8])
            hora = int(data_modificacao[8:10])
            minuto = int(data_modificacao[10:12])
            data_modificacao = datetime(ano, mes, dia, hora, minuto)
            posicao_pai = int(inode_texto[294:294+len(str(self.quantidade_inodes))])

            if posicao_pai == 0 and nome == '':
                apontador_inode_pai = None
            else:
                apontador_inode_pai = inodes[posicao_pai]

            inode_blocos = []
            limite_blocos = ((self.tamanho_inodes * 1024) - 300) // (len(str(self.quantidade_blocos)))
            ultima_posicao = 294 + len(str(self.quantidade_inodes))
            for j in range(limite_blocos):
                pos_bloco_texto = inode_texto[ultima_posicao:ultima_posicao + len(str(self.quantidade_blocos))]
                ultima_posicao += len(str(self.quantidade_blocos))
                _bloco = int(pos_bloco_texto)
                if _bloco != 0 or j == 0:
                    inode_blocos.append(_bloco)
            if len(inode_blocos) == 0:
                inode_blocos = None
            else:
                for j in range(len(inode_blocos)):
                    inode_blocos[j] = blocos[inode_blocos[j]]
            
            criador = ''
            if i == 0:
                nome = '/'
                criador = 'root'
            tipo = inode_texto[-1]
            if tipo == 'd':
                inode_blocos = None
            _inode: inode = inode(nome, criador,  apontador_inode_pai, self)
            _inode.tamanho = tamanho
            _inode.data_criacao = data_criacao
            _inode.data_modificacao = data_modificacao
            _inode.apontador_blocos = inode_blocos
            
            inodes.append(_inode)

        cont = 0
        for _inode in inodes:
            if _inode is None and cont != 0:
                cont += 1
                continue
            cont += 1
            if _inode.apontador_inode_pai is not None:
                for i in range(len(inodes)):
                    if inodes[i] == _inode.apontador_inode_pai:
                        _inode.apontador_inode_pai.apontador_inodes.append(_inode)   
                        _inode.apontador_inode_pai.set_tipo('d')
                        break
        
        for _inode in inodes:
            if _inode is None:
                continue
            if _inode.tipo == 'd':
                continue
            _inode.set_tipo('a')

        for i in range(len(bits_inodes)):
            _inode = inodes[i]
            if _inode is None:
                _inode = str(i)
            self.bitmap_inodes[_inode] = bits_inodes[i]
        
        self.bitmap_blocos = OrderedDict((k, v) for k, v in self.bitmap_blocos.items() if v == 1)
        self.bitmap_inodes = OrderedDict((k, v) for k, v in self.bitmap_inodes.items() if v == 1)








def main():
    meu_disco = disco(256, 4, 1)

    quantidade_maxima_blocos = meu_disco.limite()
    print(f'Quantidade máxima de blocos: {quantidade_maxima_blocos}')
    bytes_blocos = meu_disco.tamanho_blocos * quantidade_maxima_blocos * 1024
    bytes_inodes = meu_disco.tamanho_inodes * quantidade_maxima_blocos * 1024
    bytes_total = bytes_blocos + bytes_inodes + quantidade_maxima_blocos * 2
    total_bytes = meu_disco.tamanho_maximo * 1024 * 1024
    sobra = total_bytes - bytes_total
    print(f'Bytes usados: {bytes_total}')
    print(f'Bytes livres: {sobra}')




    
    

if __name__ == '__main__':
    main()