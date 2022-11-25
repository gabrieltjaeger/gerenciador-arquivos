from Info.disco import disco
from Info.inode import inode
from Info.usuario import usuario
import os
from datetime import datetime

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
          ## atualizando o tempo de modificação do arquivo
          for inode in self.diretorio_atual.apontador_inodes:
            if inode.nome == arquivo:
                inode.data_modificacao = datetime.now()
          abrir_arquivo.write(conteudo)
          abrir_arquivo.close()
        else:
          raise Exception
   
    def ler_arquivo(self, arquivo: inode):
        if str(self.diretorio_atual.apontador_inodes).find(str(arquivo)) != -1:
            abrir_arquivo = open(arquivo, "r")
            conteudo = abrir_arquivo.read()
            print(conteudo)
            abrir_arquivo.close()
        else:
            raise Exception
    
    def copiar_arquivo(self, arquivo: inode, copia_arquivo: str, criador: str):
        if str(self.diretorio_atual.apontador_inodes).find(str(arquivo)) != -1:
            novo_arquivo = open(copia_arquivo, "w")
            conteudo_arquivo_original = open(arquivo, "r")
            novo_arquivo.write(conteudo_arquivo_original.read())
            novo_arquivo.close()
            conteudo_arquivo_original.close()
            novo_inode = inode(copia_arquivo, criador, None, self.diretorio_atual)
            self.disco.inodes.append(novo_inode)
            self.diretorio_atual.apontador_inodes.append(novo_inode)


    def renomear_arquivo(self, nome_antigo: str, nome_novo: str):
        if str(self.diretorio_atual.apontador_inodes).find(nome_antigo) != -1:
            for inode in self.diretorio_atual.apontador_inodes:
                if inode.nome == nome_antigo:
                    ##atualizando o tempo de modificação do arquivo
                    inode.data_modificacao = datetime.now()
                    inode.nome = nome_novo
                    os.rename(nome_antigo, nome_novo)
        else:
            raise Exception

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
        

    def remover_diretorio(self, nome_diretorio: str):
        for inode in self.diretorio_atual.apontador_inodes: ## github copilot, talvez vale a pena usar
            if inode.nome == nome_diretorio and len(inode.apontador_inodes) != 0: ## não deixa remover diretórios que não estão vazios
                self.diretorio_atual.apontador_inodes.remove(inode)
                self.disco.inodes.remove(inode)
                break
        else:
            raise Exception

    def trocar_diretorio(self, caminho: list, caminho_inicial: inode = None):
        destino = self.percorre_caminho_e_retorna_inode(caminho, caminho_inicial)
        if destino == False:
            return False
        if destino == '..':
            if self.diretorio_atual.apontador_inode_pai is not None: ## aqui ele vê se não é o root
                self.diretorio_atual = self.diretorio_atual.apontador_inode_pai
                return True
            else:
                return False
        if destino is not None:
          novodiretorio = [i for i in self.diretorio_atual.apontador_inodes if i.nome == destino] ## verifica se o destino é um diretório, se existe um inode com o nome do destino
          self.diretorio_atual = novodiretorio[0] ## o erro do cd é aqui
          return True
        return False

    def percorre_caminho_e_retorna_inode(self, caminho: list, caminho_inicial: inode = None) -> inode:
        return caminho[0]
        


    def renomear_diretorio(self, nome_antigo: str, nome_novo: str):
        for inode in self.diretorio_atual.apontador_inodes:
            if inode.nome == nome_antigo:
                ##atualizando o tempo de modificação do arquivo
                inode.data_modificacao = datetime.now()
                inode.nome = nome_novo
                break
                
        else:
            raise Exception