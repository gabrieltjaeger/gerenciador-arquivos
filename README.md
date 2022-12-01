# gerenciador-arquivos

Gerenciador de arquivos.

Feito por: André Maurell - 142365, Arthur Bubolz - 140548, Gabriel Jaeger - 140543, Gabriel Martins - 142356

Para rodar este código, é necessário que todas as pastas estejam localizadas junto com a main.py.

Após isso, é necessário apenas rodar em um terminal: 

'''
python3 main.py
'''

Ele simulará o funcionamento de um sistema de arquivos, como em um Sistema Operacional. Inicialmente, ele criará um usuário admin para que o usuário possa fazer as operações.

As operações disponíveis são:

mkdir (nome do diretório) - cria um diretório;

cd (nome do diretório) - troca o diretório sendo modificado atualmente pelo diretório desejado.

rmdir (nome do diretório) - remove o diretório;

ls - lista os arquivos e diretórios dentro do diretório atual;

touch (nome do arquivo) - cria um arquivo, inicialmente vazio;

rm (nome do arquivo) - remove aquele arquivo, o excluindo;

echo "(conteúdo)" >> (nome do arquivo) - escreve dentro do arquivo dado o conteúdo entre aspas;

cat (nome do arquivo) - lê o arquivo, retornando seu conteúdo.

cp (arquivo antigo) (arquivo novo) - copia o conteúdo do arquivo antigo para um arquivo novo;

mv (nome do arquivo/diretório) (novo nome do arquivo/diretório) - Renomeia o arquivo ou diretório dado;


Além disto, todos os arquvios e diretórios criados ficam de maneira persistente no sistema.
