# Projeto de Filmes

## Uso:

1. `python -m venv env`
2. `env\Scripts\activate.bat` ou `.\env\Scripts\Activate.ps1`. Deve abrir um ambiente virtual, e os comandos a seguir devem ser usados dentro dele.
3. `pip install -r requirements.txt` para instalar as dependências.
4. `python src/main.py --create` para iniciar o projeto criando o banco de dados e populando as tabelas.

## Modelo Lógico
Filme (id_filme, titulo, comentário, nota, #id_estudio)

Estudio (id_estudio, nome) 

GeneroFilme (#id_genero, #id_filme) 

Genero (id_genero, nome) 

FuncionarioFilme (#id_funcao, #id_pessoa, #id_filme) 

Funcao (id_funcao, nome) 

Pessoa (id_pessoa, nome, sexo) 

SessaoPessoa (#id_pessoa, #id_sessao) 

Sessao (id_sessao, data_visto, comentário, #id_filme, #id_local) 

Local (id_local, nome, comentario) 

## Menu
OBS: A palavra associar remete a associação da tabela/menu sendo detalhado com uma tabela externa.

1. Cadastrar **filme**
   * Registrar um nome, comentário e nota
   * Associar um estúdio (ou criar um novo)
2. Cadastrar **sessão**
   * Associar um filme (ou cadastrar filme)
   * Registrar Data e hora da sessão
   * Associar Local da sessão (ou criar um novo)
   * Associar as pessoas que assitiram junto (ou cadastrar pessoa)
   * Registrar comentário da sessão
3. Listar filmes com nota (ordenar por nota)
4. Listar filmes pela ordem alfabética
5. Consultar dados de um filme (todos os dados) (não falar quando assistiu)
6. Listar sessões (ordenar por data descendente) (data + nome_filme)
7. Consultar dados de uma sessão (todos os dados)
