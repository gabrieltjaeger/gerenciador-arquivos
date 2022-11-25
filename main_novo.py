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
from Info.sistema_operacional import sistema_operacional


def main():
    so = sistema_operacional()
    print("Bem vindo ao sistema de arquivos, por favor, digite se você deseja criar um usuário ou logar em um já existente.")

    while True:
        print("1 - Criar usuário")
        print("2 - Logar")
        print("3 - Sair")
        opcao = int(input("Digite a opção desejada: "))
        if opcao == 1:
            nome = input("Digite o nome do usuário: ")
            senha = input("Digite a senha do usuário: ")
            try:
                so.criar_usuario(nome, senha)
            except:
                print("Erro ao criar usuário, fechando...")
                exit()
            print("Usuário criado com sucesso! Deseja logar?")
            print("s")
            print("n")
            opcao = input("Digite a opção desejada: ")
            if opcao == "s":
                so.logar(nome, senha)
                print("Bem Vindo, " + so.usuario_atual.nome)
                break
            else:
                print("Usuário não logado. Voltando ao menu principal.")
        elif opcao == 2:
            nome = input("Digite o nome do usuário: ")
            senha = input("Digite a senha do usuário: ")
            if so.logar(nome, senha):
                print("Bem vindo, " + so.usuario_atual.nome)
                break
            else:
                print("Usuário ou senha incorretos. Voltando ao menu principal.")
        elif opcao == 3:
            print("Saindo...")
            exit()
        else:
            print("Opção inválida.")

        
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
                print("erro ao escrever no arquivo\nuso: echo <conteudo> <nome>")
        elif comando[0] == "cat":
            try:
                so.arquivos.ler_arquivo(comando[1])
            except:
                print("erro ao ler arquivo\nuso: cat <nome>")
        elif comando[0] == "cp":
                so.arquivos.copiar_arquivo(comando[1], comando[2], so.usuario_atual)
        elif comando[0] == "mv":
            try:
                so.arquivos.renomear_arquivo(comando[1], comando[2])
            except:
                print("erro ao renomear arquivo\nuso: mv <nome> <novo_nome>")
        elif comando[0] == "mkdir":
            try:
                so.arquivos.criar_diretorio(comando[1], so.usuario_atual, True)
                ## print(inode('teste', 'admin', None, None)) # ?
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
