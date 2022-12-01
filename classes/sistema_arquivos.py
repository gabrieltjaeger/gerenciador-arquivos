from .disco import disco
from .inode import inode
from .usuario import usuario
from . import sistema_operacional


from colorama import Fore, Style


class sistema_arquivos:
    def __init__(self, disco: disco, so: sistema_operacional):
        self.disco = disco
        self.root = inode('/', 'root', None, self.disco, apontador_blocos=None)
        if len(self.disco.bitmap_inodes) > 0:
            for _inode, bit in self.disco.bitmap_inodes.items():
                self.root = _inode
                break
        else:
            self.disco.adicionar_inode(self.root)
        self.diretorio_atual = self.root
        self.so = so
        # print(self.diretorio_atual.apontador_inodes)


    def set_root(self, _inode: inode):
        self.root = _inode
        
    def alterar_diretorio_atual(self, _inode: inode):  # PRONTA
        if _inode is None:
            return False
        self.diretorio_atual = _inode

    def procurar_inode(self, inode_destino: inode, nome: str) -> inode:  # PRONTA
        return inode_destino.get_inode(nome)

    def remover_diretorio(self, caminho: list):
        if len(caminho) == 0:
            print("rmdir: caminho vazio ou inválido")
            return False
        diretorio_a_remover = caminho[-1]
        caminho = caminho[:-1]
        diretorio_onde_remover = self.encontrar_inode(caminho)
        if diretorio_onde_remover is False:
            print("bash: rmdir: " + '/'.join(caminho) +
                  ": Diretório inexistente")
            return False
        if (filho := self.procurar_inode(diretorio_onde_remover, diretorio_a_remover)) is not None:
            if filho is not False:
                if filho.apontador_inode_pai is diretorio_onde_remover:
                    if filho.tipo != 'd':
                        print("bash: rmdir: " + '/'.join(caminho) +
                              ": Diretório inexistente")
                        return False
                    if not filho.dir_vazio():
                        print("bash: rmdir: " + '/'.join(caminho) +
                              ": Diretório não vazio")
                        return False
                    diretorio_onde_remover.remover_inode(filho)
                    return True
        print("bash: rmdir: " + '/'.join(caminho) + ": Diretório inexistente")
        return False

    def criar_inode(self, caminho: list, criador: str, tipo: str) -> inode:  # PRONTA
        if len(caminho) == 0:
            print("mkdir: caminho vazio ou inválido")
            return False
        inode_a_criar = caminho[-1]
        caminho = caminho[:-1]
        diretorio_onde_criar = self.encontrar_inode(caminho)
        if diretorio_onde_criar is False:
            print("bash: mkdir: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if (filho := self.procurar_inode(diretorio_onde_criar, inode_a_criar)) is not None:
            if filho is not False:
                if filho.apontador_inode_pai is diretorio_onde_criar:
                    print("bash: mkdir: " + '/'.join(caminho) +
                          ": Arquivo ou diretório já existente")
                    return False
        novo_inode = None
        if tipo == 'd':
            novo_inode = inode(inode_a_criar, criador, diretorio_onde_criar, self.disco, apontador_blocos=None)
        elif tipo == 'a':
            novo_inode = inode(inode_a_criar, criador, diretorio_onde_criar, self.disco, apontador_inodes=None)
        else:
            print("bash: mkdir: " + '/'.join(caminho) +
                  ": Tipo de inode inválido")
            return False
        diretorio_onde_criar.adicionar_inode(novo_inode)
        self.disco.adicionar_inode(novo_inode)
        return novo_inode

    def encontrar_inode(self, caminho: list) -> inode:  # PRONTA
        diretorio_inicial = self.diretorio_atual
        for diretorio in caminho:
            if diretorio == '.':
                continue
            if diretorio == '/':
                diretorio = self.root
            elif diretorio == '..':
                if self.diretorio_atual.apontador_inode_pai is None:
                    self.alterar_diretorio_atual(diretorio_inicial)
                    return False
                diretorio = self.diretorio_atual.apontador_inode_pai
            else:
                diretorio = self.procurar_inode(
                    self.diretorio_atual, diretorio)
                if diretorio is False or diretorio is None:
                    self.alterar_diretorio_atual(diretorio_inicial)
                    return False
                if diretorio.apontador_inode_pai is not self.diretorio_atual:
                    self.alterar_diretorio_atual(diretorio_inicial)
                    return False
            self.alterar_diretorio_atual(diretorio)
        inode_encontrado = self.diretorio_atual
        self.alterar_diretorio_atual(diretorio_inicial)
        return inode_encontrado

    def trocar_diretorio(self, caminho: list):  # PRONTA
        diretorio_destino = self.encontrar_inode(caminho)
        if diretorio_destino is False:
            print("bash: cd: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if diretorio_destino.tipo != 'd':
            print("bash: cd: " + '/'.join(caminho) + ": Não é um diretório")
            return False
        self.alterar_diretorio_atual(diretorio_destino)
        return True

    def listar_diretorio(self, caminho: list = None) -> bool:  # PRONTA
        if caminho is None:
            caminho = ['.']
        diretorio_a_listar = self.encontrar_inode(caminho)
        if diretorio_a_listar is False:
            print("bash: ls: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        filhos = diretorio_a_listar.listar()
        filho: inode
        for filho in filhos:
            if filho.apontador_inode_pai is not diretorio_a_listar:
                continue
            if filho.tipo == 'd':
                print(f"{Fore.BLUE}{filho.nome}{Style.RESET_ALL}")
            else:
                print(filho.nome)
        return True

    def renomear_arquivo_ou_diretorio(self, caminho: list, novo_caminho: str): # ACREDITO QUE ESTEJA PRONTA, MAS NÃO TESTEI MUITO
        inode_a_renomear = self.encontrar_inode(caminho)
        if inode_a_renomear is False:
            print("bash: mv: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if inode_a_renomear.apontador_inode_pai is None:
            print("bash: mv: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        pai_novo_nome = self.encontrar_inode(novo_caminho[:-1])
        if pai_novo_nome is False:
            print("bash: mv: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        filho_novo_nome = self.procurar_inode(pai_novo_nome, novo_caminho[-1])
        if filho_novo_nome is not None and filho_novo_nome is not False:
            # Filho com mesmo nome já existe
            # Se filho estiver vazio, remover, senão, retornar erro
            if inode_a_renomear.apontador_inode_pai is pai_novo_nome:
                # Se o pai for o mesmo, colocar o filho_novo_nome dentro do inode_a_renomear
                inode_a_renomear.mover(filho_novo_nome, inode_a_renomear.nome)
                return True
            if filho_novo_nome.apontador_inode_pai is pai_novo_nome:
                if not filho_novo_nome.dir_vazio():
                    print("bash: mv: " + '/'.join(caminho) +
                          ": Diretório já existente")
                    return False
                else:
                    pai_novo_nome.remover_inode(filho_novo_nome)
                    self.disco.remover_inode(filho_novo_nome)
        inode_a_renomear.mover(pai_novo_nome, novo_caminho[-1])
        return True

    def remover_arquivo(self, caminho: list): ## PRONTO?? DA UMA OLHADA JAEGER
        inode_a_remover = self.encontrar_inode(caminho)
        if inode_a_remover is False:
            print("bash: rm: " + '/'.join(caminho) +
                  ": Arquivo inexistente")
            return False
        if inode_a_remover.apontador_inode_pai is None:
            print("bash: rm: " + '/'.join(caminho) +
                  ": Arquivo inexistente")
            return False
        if inode_a_remover.tipo == 'd':
            print("bash: rm: " + '/'.join(caminho) +
                  ": Não é um arquivo")
            return False
        else:
            inode_a_remover.apontador_inode_pai.remover_inode(inode_a_remover)
            self.disco.remover_inode(inode_a_remover)
            return True


    def escrever_arquivo(self, caminho: list, conteudo: str):
        inode_a_escrever = self.encontrar_inode(caminho)
        if inode_a_escrever is False:
            print("bash: echo: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if inode_a_escrever.tipo != 'a':
            print("bash: echo: " + '/'.join(caminho) +
                  ": Não é um arquivo")
            return False
        return inode_a_escrever.escrever(conteudo)
    
    def ler_arquivo(self, caminho: list):
        inode_a_ler = self.encontrar_inode(caminho)
        if inode_a_ler is False:
            print("bash: cat: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if inode_a_ler.tipo != 'a':
            print("bash: cat: " + '/'.join(caminho) +
                  ": Não é um arquivo")
            return False
        conteudo_arquivo = inode_a_ler.ler()
        if conteudo_arquivo is False or conteudo_arquivo is None:
            return False
        print(conteudo_arquivo)
        return True

    def copiar_arquivo(self, caminho: list, novo_caminho: list): ## está duplicando o conteúdo do arquivo... pq?
        inode_a_copiar = self.encontrar_inode(caminho)
        if inode_a_copiar is False:
            print("bash: cp: " + '/'.join(caminho) +
                  ": Arquivo ou diretório inexistente")
            return False
        if inode_a_copiar.tipo != 'a':
            print("bash: cp: " + '/'.join(caminho) +
                  ": Não é um arquivo")
            return False
        inode_copia = self.criar_inode(novo_caminho, self.so.usuario_atual, 'a')
        inode_copia.escrever(inode_a_copiar.ler())
        return True