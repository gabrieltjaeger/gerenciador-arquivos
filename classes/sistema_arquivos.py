from .disco import disco
from .inode import inode
from .usuario import usuario
from colorama import Fore, Style


class sistema_arquivos:
    def __init__(self, disco: disco):
        self.disco = disco
        self.disco.inodes.append(
            inode('/', "root", None, apontador_blocos=None))
        self.diretorio_atual = self.disco.inodes[0]

    def criar_diretorio(self, caminho: list, criador: str):
        diretorio_inicial = self.diretorio_atual
        if len(caminho) == 1:
            self.diretorio_atual.adicionar_inode(
                inode(caminho[0], criador, self.diretorio_atual, apontador_blocos=None))
            self.alterar_diretorio_atual(self.diretorio_atual.apontador_inodes[-1])
        elif len(caminho) > 1:
            for diretorio in caminho:
                if diretorio == '..':
                    self.alterar_diretorio_atual(self.diretorio_atual.apontador_inode_pai)
                elif diretorio == '.':
                    pass
                elif diretorio == '':
                    self.alterar_diretorio_atual(self.disco.inodes[0])
                else:
                    _inode = self.procurar_inode(self.diretorio_atual, diretorio)
                    if _inode is False:
                        _inode = inode(diretorio, criador, self.diretorio_atual, apontador_blocos=None)
                        self.diretorio_atual.adicionar_inode(_inode)        
                    self.alterar_diretorio_atual(_inode)
                if self.diretorio_atual is False:
                    return False
        self.alterar_diretorio_atual(diretorio_inicial)
        return True

    def listar_diretorio(self, caminho: list = None) -> None:
        # Encontra o inode de um diretório e imprime os seus filhos
        if len(caminho) == 1:
            if caminho[0] == '':
                filhos = self.diretorio_atual.listar()
                for filho in filhos:
                    if filho.apontador_inode_pai is not self.diretorio_atual:
                        continue
                    print(f"{Fore.BLUE}{filho.nome}{Style.RESET_ALL}")
        elif len(caminho) > 1:
            inode = self.encontrar_inode(caminho)
            if inode is False:
                return False
            filhos = inode.listar()
            for filho in filhos:
                if filho.apontador_inode_pai is not inode:
                    continue
                print(f"{Fore.BLUE}{filho.nome}{Style.RESET_ALL}")

    def listar_diretorio(self, caminho: list = None) -> None:
        # Encontra o inode de um diretório e imprime os seus filhos
        diretorio_a_listar = None

    def encontrar_inode(self, caminho: list) -> inode:
        diretorio_inicial = self.diretorio_atual
        for diretorio in caminho:
            if diretorio == '..':
                self.alterar_diretorio_atual(self.diretorio_atual.apontador_inode_pai)
            elif diretorio == '.':
                pass
            elif diretorio == '':
                self.alterar_diretorio_atual(self.disco.inodes[0])
            else:
                self.alterar_diretorio_atual(self.procurar_inode(self.diretorio_atual, diretorio))
            if self.diretorio_atual is False:
                self.alterar_diretorio_atual(diretorio_inicial)
                return False
        _inode = self.diretorio_atual
        self.alterar_diretorio_atual(diretorio_inicial)
        return _inode

    def alterar_diretorio_atual(self, _inode: inode):
        if _inode is None:
            return False
        self.diretorio_atual = _inode

    def trocar_diretorio(self, caminho: list):
        novo_diretorio = self.encontrar_inode(caminho)
        if novo_diretorio == False:
            print("bash: cd: " + '/'.join(caminho) + ": No such file or directory")
            return False
        if novo_diretorio.tipo != 'd':
            return False
        self.alterar_diretorio_atual(novo_diretorio)
        return True

    def procurar_inode(self, inode: inode, nome: str) -> inode:
        for _inode in inode.apontador_inodes:
            if _inode.nome == nome:
                return _inode
        return False

    def remover_diretorio(self):
        pass

    def renomear_diretorio(self):
        pass

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
