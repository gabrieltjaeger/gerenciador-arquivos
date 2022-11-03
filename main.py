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
    def __init__(self):
        self.nome = ""
        self.criador = ""
        self.dono = ""
        self.tamanho = 0
        self.data_criacao = ""
        self.data_modificacao = ""
        self.permissoes = ""
        self.apontadores_blocos = []
        self.apontador_inode = None

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


class sistema_arquivos:
    def __init__(self, disco: disco):
        self.disco = disco
        self.diretorio_atual = "/"

    def criar_arquivo(self):
        pass

    def remover_arquivo(self):
        pass

    def escrever_arquivo(self):
        pass

    def ler_arquivo(self):
        pass

    def copiar_arquivo(self):
        pass

    def renomear_arquivo(self):
        pass

    def criar_diretorio(self):
        pass

    def listar_diretorio(self):
        pass

    def remover_diretorio(self):
        pass

    def trocar_diretorio(self):
        pass

    def renomear_diretorio(self):
        pass

class usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha


class sistema_operacional:
    def __init__(self):
        self.disco = disco(256, 4, 4)
        self.arquivos = sistema_arquivos(self.disco)
        self.usuarios = []


