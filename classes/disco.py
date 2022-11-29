from collections import OrderedDict
import os

class disco:
    def __init__(self, tamanho_maximo: int, tamanho_blocos: int, tamanho_inodes: int):
        self.tamanho_maximo = tamanho_maximo
        self.tamanho_blocos = tamanho_blocos
        self.tamanho_inodes = tamanho_inodes

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
        print(len(self.bitmap_blocos))
        print(self.quantidade_blocos, self.quantidade_inodes)
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
                
        

        # print(bitmap_blocos)
        # print(blocos)




def main():
    meu_disco = disco(256, 4, 1)
    # Se eu quiser criar um disco com 256MB, com blocos de 4KB e inodes de 1KB, qual é a configuração mais eficiente?

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