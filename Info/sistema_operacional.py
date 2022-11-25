from Info.disco import disco
from Info.sistema_arquivos import sistema_arquivos
from Info.usuario import usuario
import os

class sistema_operacional:
    def __init__(self):
        self.disco = disco(256, 4, 4)
        self.arquivos = sistema_arquivos(self.disco)
        self.usuarios = []
        ## se o arquivo users.txt não estiver vazio, carrega os usuários
        if os.stat("Info\\Usuarios\\users.txt")!= 0:
            arquivo_users = open("Info\\Usuarios\\users.txt", "r")
            for linha in arquivo_users:
                nome, senha = linha.split()
                self.usuarios.append(usuario(nome, senha))
            arquivo_users.close()
        self.usuario_atual = None
    
    def criar_usuario(self, nome: str, senha: str):
        ## verifica se o usuário já existe
        for usuario in self.usuarios:
            if usuario.nome == nome:
                print("Usuário já existe")
                raise Exception

        ##salvando usuario na pasta Users, no arquivo users.txt
        arquivo_users = open("Info\\Usuarios\\users.txt", "a")
        arquivo_users.write(nome + " " + senha + "\n")
        arquivo_users.close()
        self.usuarios.append(usuario(nome, senha))

    def logar(self, nome: str, senha: str):
        for usuario in self.usuarios:
            if usuario.nome == nome and usuario.senha == senha:
                self.usuario_atual = usuario
                return True
        return False