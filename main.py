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
# import datetime
from datetime import datetime
import os


class usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return self.__str__()


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
        self.criar_diretorio("root", "root", False)
        self.diretorio_atual = self.disco.inodes[0]

    def criar_arquivo(self, nome_arquivo: str, criador: str):
        if str(self.diretorio_atual.apontador_inodes).find(nome_arquivo) != -1: ## não deixa criar mais de um arquvio com o mesmo nome
            raise Exception
        novo_arquivo = open(nome_arquivo, "w")
        novo_arquivo.close()
        novo_inode = inode(nome_arquivo, criador, None, self.diretorio_atual)
        self.disco.inodes.append(novo_inode)
        self.diretorio_atual.apontador_inodes.append(novo_inode)

    def remover_arquivo(self, nome_arquivo: str):
        if str(self.diretorio_atual.apontador_inodes).find(nome_arquivo) != -1:
            os.remove(nome_arquivo) ##não sei se pode...
            for inode in self.diretorio_atual.apontador_inodes:
                if inode.nome == nome_arquivo:
                    self.diretorio_atual.apontador_inodes.remove(inode)
                    self.disco.inodes.remove(inode)
        else:
            raise Exception

    def escrever_arquivo(self, conteudo: str, arquivo: inode):
        if str(self.diretorio_atual.apontador_inodes).find(str(arquivo)) != -1: ## não deixa escrever em arquivos que não estão no diretório atual
          abrir_arquivo = open(arquivo, "a")
          abrir_arquivo.write(conteudo)
          abrir_arquivo.close()
        else:
          raise Exception
    def ler_arquivo(self):
        pass

    def copiar_arquivo(self):
        pass

    def renomear_arquivo(self):
        pass

    def criar_diretorio(self, nome: str, criador: str, apontador_inode_pai: bool):
        if apontador_inode_pai:
            apontador_inode_pai = self.diretorio_atual
        else:
            apontador_inode_pai = None

        novo_inode = inode(nome, criador, None, apontador_inode_pai)
        self.disco.inodes.append(novo_inode)

        if apontador_inode_pai:
            self.diretorio_atual.apontador_inodes.append(novo_inode)



    def listar_diretorio(self):
        for inode in self.diretorio_atual.apontador_inodes:
            print(inode.nome)
        

    def remover_diretorio(self):
        pass

    def trocar_diretorio(self, caminho: list, caminho_inicial: inode = None):
        destino = self.percorre_caminho_e_retorna_inode(caminho, caminho_inicial)
        if destino == False:
            return False
        if destino is not None:
          novodiretorio = [i for i in self.diretorio_atual.apontador_inodes if i.nome == destino] ## verifica se o destino é um diretório, se existe um inode com o nome do destino
          self.diretorio_atual = novodiretorio[0] ## o erro do cd é aqui
          return True
        return False

    def percorre_caminho_e_retorna_inode(self, caminho: list, caminho_inicial: inode = None) -> inode:
        return caminho[0]
        


    def renomear_diretorio(self):
        pass




class sistema_operacional:
    def __init__(self):
        self.disco = disco(256, 4, 4)
        self.arquivos = sistema_arquivos(self.disco)
        self.usuarios = []
        self.usuario_atual = None
    
    def criar_usuario(self, nome: str, senha: str):
        self.usuarios.append(usuario(nome, senha))

    def logar(self, nome: str, senha: str):
        for usuario in self.usuarios:
            if usuario.nome == nome and usuario.senha == senha:
                self.usuario_atual = usuario
                return True
        return False
    

def main():
    so = sistema_operacional()
    so.criar_usuario("admin", "admin")
    so.logar("admin", "admin")
    while (comando := input(f"{so.usuario_atual}:~{so.arquivos.diretorio_atual}$ ")) != "sair":
        comando = comando.split(" ")
        if comando[0] == "touch": ## cria um arquivo vazio (acho que tá funcionando direitinho)
            try:
                so.arquivos.criar_arquivo(comando[1], so.usuario_atual)
            except:
                print("erro ao criar arquivo\nuso: touch <nome>")
        elif comando[0] == "rm":
            try:
                so.arquivos.remover_arquivo(comando[1])
            except:
                print("erro ao remover arquivo\nuso: rm <nome>")
        elif comando[0] == "echo": ## tem que fazer funcionar para mais de uma palavra
            try:
                so.arquivos.escrever_arquivo(comando[1], comando[2])
            except:
                print("erro ao escrever no arquivo\nuso: echo \"<conteudo>\" >> <nome>")
        elif comando[0] == "cat":
            try:
                so.arquivos.ler_arquivo(comando[1])
            except:
                print("erro ao ler arquivo\nuso: cat <nome>")
        elif comando[0] == "cp":
            try:
                so.arquivos.copiar_arquivo(comando[1], comando[2])
            except:
                print("erro ao copiar arquivo\nuso: cp <nome> <destino>")
        elif comando[0] == "mv":
            try:
                so.arquivos.renomear_arquivo(comando[1], comando[2])
            except:
                print("erro ao renomear arquivo\nuso: mv <nome> <novo_nome>")
        elif comando[0] == "mkdir":
            try:
                so.arquivos.criar_diretorio(comando[1], so.usuario_atual, True)
                print(inode('teste', 'admin', None, None))
            except:
                print("erro ao criar diretório\nuso: mkdir <nome>")
        elif comando[0] == "ls":
            try:
                so.arquivos.listar_diretorio()
            except:
                print("erro ao listar diretório\nuso: ls")
        elif comando[0] == "rmdir":
            try:
                so.arquivos.remover_diretorio(comando[1]) # só funciona se o diretório estiver vazio
            except:
                print("erro ao remover diretório\nuso: rmdir <nome>")
        elif comando[0] == "cd":
            try:
                caminho = comando[1] if len(comando) > 1 else " " ### TO DO -- FAZER ISSO DE UMA FORMA MAIS ELEGANTE, FUNÇÃO QUE RETORNA O CAMINHO E QUE SERÁ 
                                                                  ### CHAMADA DENTRO DO SISTEMA DE ARQUIVOS E NÃO NA SELEÇÃO DE COMANDOS.

                if caminho[0] == "/":
                    print("Arquivo ou diretório inexistente")
                    raise Exception
                if "/" in caminho:
                    caminho = caminho.rstrip('/').split('/')
                else:
                    caminho = [caminho]
                so.arquivos.trocar_diretorio(caminho)
            except Exception as e:
                print(e,"\nerro ao trocar diretório\nuso: cd <nome>")
        elif comando[0] == "mvdir":
            try:
                so.arquivos.renomear_diretorio(comando[1], comando[2])
            except:
                print("erro ao renomear diretório\nuso: mvdir <nome> <novo_nome>")

        else:
            print("comando inválido")


    

    
if __name__ == "__main__":
    main()
