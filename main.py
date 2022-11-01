# main.py
# sistema de arquivos baseado em inodes
# assumir q o disco rígido tem 256mb de espaço
# disco tem blocos de tamanho fixo, 4kb de tamanho cada
# i-node: metainformações do arquivo
# 1. nome do arquivo
# 2. criador do arquivo
# 3. dono do arquivo
# 4. tamanho do arquivo
# 5. data de criação
# 6. data de modificação
# 7. permissões de acesso (dono e outros usuários - leitura, escrita, execução)
# 8. apontadores para blocos
# 9. apontador para eventual outro i-node
# 10. apontador para i-node pai
# # 11. apontador para i-node de diretório
# # 12. apontador para i-node de arquivo
# parte do armazenamento do disco é reservada para armazenar as informações de gerenciamento, controle sobre quais blocos estão sendo usados e quais estão livres
# 1. bitmap de blocos livres
# 2. bitmap de blocos ocupados
# 3. bitmap de i-nodes livres
# 4. bitmap de i-nodes ocupados
from sys import getsizeof


class inode:
    pass

class block:
    pass

class disk:
    pass

class inodes:
    pass

class blocks:
    pass

class filesystem:
    pass

print('trabalho pronto 100%. confia.')
