from .disco import disco
from .sistema_arquivos import sistema_arquivos
from .usuario import usuario

class sistema_operacional:
    def __init__(self):
        self.disco = disco(256, 4, 4)
        self.arquivos = sistema_arquivos(self.disco)
        self.usuarios = []
        self.usuario_atual = None

    def criar_usuario(self, nome: str, senha: str):
        for usuario in self.usuarios:
            if usuario.nome == nome:
                print("Já existe um usuário com esse nome. Tente novamente.")
                return False
        self.usuarios.append(usuario(nome, senha))
        return True

    def logar(self, nome: str, senha: str):
        for usuario in self.usuarios:
            if usuario.nome == nome and usuario.senha == senha:
                self.usuario_atual = usuario
                return True
        return False

    def converter_caminho_para_lista(self, comando: list) -> list:
        if len(comando) > 1:
            caminho = comando[1]
            if caminho[0] == "/":
                print("Arquivo ou diretório inexistente")
            if "/" in caminho:
                caminho = caminho.rstrip('/').split('/')
            else:
                caminho = [caminho]
            return caminho
        else:
            return ['']
