from colorama import Fore, Style

from classes.sistema_operacional import sistema_operacional

'''# main.py
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
# import datetime'''


def main():
    so = sistema_operacional()
    so.criar_usuario("admin", "admin")
    so.logar("admin", "admin")
    while (comando := input(f"{Fore.GREEN}{so.usuario_atual}{Style.RESET_ALL}:{Fore.BLUE}~{so.arquivos.diretorio_atual}{Style.RESET_ALL}$ ")) != "sair":
        comando = comando.split(" ")
        match comando[0]:
            case "touch":
                try:
                    caminho = so.converter_caminho_para_lista(comando)
                    nome = caminho.pop(-1)
                    so.arquivos.criar_arquivo(caminho, nome, so.usuario_atual)
                except Exception as e:
                    print(e)
                    print("erro ao criar arquivo")
                    print("uso: touch <nome>")
            case "rm":
                try:
                    so.arquivos.remover_arquivo(comando[1])
                except Exception as e:
                    print(e)
                    print("erro ao remover arquivo")
                    print("uso: rm <nome>")
            case "echo":
                try:
                    so.arquivos.escrever_arquivo(comando[1], comando[2])
                except Exception as e:
                    print(e)
                    print("erro ao escrever no arquivo")
                    print("uso: echo \"<conteudo>\" >> <nome>")
            case "cat":
                try:
                    so.arquivos.ler_arquivo(comando[1])
                except Exception as e:
                    print(e)
                    print("erro ao ler arquivo")
                    print("uso: cat <nome>")
            case "cp":
                try:
                    so.arquivos.copiar_arquivo(comando[1], comando[2])
                except Exception as e:
                    print(e)
                    print("erro ao copiar arquivo")
                    print("uso: cp <nome> <novo_nome>")
            case "mv":
                try:
                    so.arquivos.renomear_arquivo(comando[1], comando[2])
                except Exception as e:
                    print(e)
                    print("erro ao renomear arquivo")
                    print("uso: mv <nome> <novo_nome>")
            case "mkdir":
                try:
                    caminho = so.converter_caminho_para_lista(comando)
                    so.arquivos.criar_diretorio(caminho, so.usuario_atual)
                except Exception as e:
                    print(e)
                    print("erro ao criar diretório")
                    print("uso: mkdir <nome>")
            case "ls":
                # try:
                caminho = so.converter_caminho_para_lista(comando)
                so.arquivos.listar_diretorio(caminho)
                # except Exception as e:
                #     print(e)
                #     print("erro ao listar diretório")
                #     print("uso: ls")
            case "rmdir":
                try:
                    # só funciona se o diretório estiver vazio
                    so.arquivos.remover_diretorio(comando[1])
                except Exception as e:
                    print(e)
                    print("erro ao remover diretório")
                    print("uso: rmdir <nome>")
            case "cd":
                # try:
                caminho = so.converter_caminho_para_lista(comando)
                so.arquivos.trocar_diretorio(caminho)
                # except Exception as e:
                    # print("erro ao trocar diretório")
                    # print("uso: cd <nome>")
            case "mvdir":
                try:
                    so.arquivos.renomear_diretorio(comando[1], comando[2])
                except Exception as e:
                    print(e)
                    print("erro ao renomear diretório")
                    print("uso: mvdir <nome> <novo_nome>")
            case _:
                print("comando não encontrado")


if __name__ == "__main__":
    main()
