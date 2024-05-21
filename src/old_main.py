import sqlite3 as sql
import time

from datetime import date
from classes import *
from ui import TerminalUI

db_path = "filmes.db"
# Conectar com o banco de dados
def conectar_banco():
    connection = sql.connect(db_path)
    return connection

def printar_linhas(rows: list):
    for row in rows:
        print(row)

# Lista todas as tabelas presentes no banco de dados
def listar_tabelas_existentes(conn: sql.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    printar_linhas(rows)
    cursor.close()

# Lista uma tabela de um banco de dados
def listar_tabela(conn: sql.Connection, table_name: str):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
    except sql.Error as e:
        print(f"Erro ao executar a consulta: {e}")

# Cria uma nova tabela no banco de dados
def criar_tabela(conn: sql.Connection, table_name: str, columns_str: str):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        conn.commit()
        print(f"tabela {table_name} OK")
        cursor.close()
    except sql.Error as e:
        print(f"Erro ao criar tabela: {e}")

# Cria tabelas necessarias para o projeto do Filme
def criar_tabelas(connection: sql.Connection):
    # Criar tabela Estudio
    criar_tabela(connection, "Estudio", "id_estudio INTEGER PRIMARY KEY, nome TEXT")

    # Criar tabela Filme
    criar_tabela(connection, "Filme", 
        """id_filme INTEGER PRIMARY KEY, 
            titulo TEXT, 
            comentario TEXT, 
            nota REAL, 
            id_estudio INTEGER,
            FOREIGN KEY(id_estudio) REFERENCES Estudio(id_estudio)"""
    )

    # Criar tabela Genero
    criar_tabela(connection, "Genero", "id_genero INTEGER PRIMARY KEY, nome TEXT")
    time.sleep(1)

    # Criar tabela GeneroFilme
    criar_tabela(connection, "GeneroFilme", "id_filme INTEGER, id_genero INTEGER, FOREIGN KEY(id_genero) REFERENCES Genero(id_genero), FOREIGN KEY(id_filme) REFERENCES Filme(id_filme)")
    time.sleep(1)

    # Criar tabela Pessoa
    criar_tabela(connection, "Pessoa", "id_pessoa INTEGER PRIMARY KEY, nome TEXT, sexo INTEGER")
    time.sleep(1)

    # Criar tabela Funcao
    criar_tabela(connection, "Funcao", "id_funcao INTEGER PRIMARY KEY, nome TEXT")
    time.sleep(1)

    # Criar tabela FuncionarioFilme
    criar_tabela(connection, "FuncionarioFilme", "id_pessoa INTEGER, id_filme INTEGER, id_funcao INTEGER, FOREIGN KEY(id_funcao) REFERENCES Funcao(id_funcao), FOREIGN KEY(id_pessoa) REFERENCES Pessoa(id_pessoa), FOREIGN KEY(id_filme) REFERENCES Filme(id_filme)")
    time.sleep(1)

    # Criar tabela Local
    criar_tabela(connection, "Local", "id_local INTEGER PRIMARY KEY, nome TEXT, comentario TEXT")
    time.sleep(1)

    # Criar tabela Sessao
    criar_tabela(connection, "Sessao", "id_sessao INTEGER PRIMARY KEY, data_visto DATE, comentario TEXT, id_filme INTEGER, id_local INTEGER, FOREIGN KEY(id_filme) REFERENCES Filme(id_filme), FOREIGN KEY(id_local) REFERENCES Local(id_local)")
    time.sleep(1)

    # Criar tabela SessaoPessoa
    criar_tabela(connection, "SessaoPessoa", "id_pessoa INTEGER, id_sessao INTEGER, FOREIGN KEY(id_sessao) REFERENCES Sessao(id_sessao), FOREIGN KEY(id_pessoa) REFERENCES Pessoa(id_pessoa)")
    time.sleep(1)

def popular_tabelas(connection: sql.Connection):
    # -------------------------------------------------
    # ----------------- Estúdios ----------------------
    # -------------------------------------------------
    universal = Estudio("Universal")
    universal.inserir_estudio(connection)

    warner_bros = Estudio("Warner Bros")
    warner_bros.inserir_estudio(connection)

    marvel = Estudio("Marvel")
    marvel.inserir_estudio(connection)

    century_studios = Estudio("20th Century Studios")
    century_studios.inserir_estudio(connection)


    # -------------------------------------------------
    # ----------------- Filmes ------------------------
    # -------------------------------------------------
    oppenheimer = Filme("Opennheimer", "Filme da bomba atômica. Muito bom", 5, universal.get_id_estudio(connection))
    oppenheimer.interir_filme(connection)

    barbie = Filme("Barbie", "Live-Action da barbie", 4, warner_bros.get_id_estudio(connection))
    barbie.interir_filme(connection)

    # elvis = Filme("Elvis", "Ainda não assisti", 1, ACHAR_ESTUDIO)
    # elvis.interir_filme(connection)

    doutor_estranho_2 = Filme("Doutor Estranho no Multiverso da Loucura", "Filme que explorou ainda mais o multiverso.", 4, marvel.get_id_estudio(connection))
    doutor_estranho_2.interir_filme(connection)

    # orfa_2 = Filme("Órfã 2: A Origem", "Não assisti", 1, ACHAR_ESTUDIO)
    # orfa_2.interir_filme(connection)

    # duna = Filme("Duna", "Filme muito bom", 5, ACHAR_ESTUDIO)
    # duna.interir_filme(connection)

    # homem_aranha_3 = Filme("Homem-Aranha: Sem volta para casa", "Filme muito bom", 5, ACHAR_ESTUDIO)
    # homem_aranha_3.interir_filme(connection)

    # interstellar = Filme("Interstellar", "Filme muito bom", 5, ACHAR_ESTUDIO)
    # interstellar.interir_filme(connection)

    # matrix = Filme("Matrix: Resurreição", "Deixou a desejar", 2, ACHAR_ESTUDIO)
    # matrix.interir_filme(connection)

    deadpool = Filme("Deadpool 2", "Filme muito bom", 5, century_studios.get_id_estudio(connection))
    deadpool.interir_filme(connection)

    # -------------------------------------------------
    # ----------------- Generos -----------------------
    # -------------------------------------------------
    ficcao = Genero("Ficção Cientifica")
    ficcao.inserir_genero(connection)

    drama = Genero("Drama")
    drama.inserir_genero(connection)

    cinebiografica = Genero("Cinebiografica")
    cinebiografica.inserir_genero(connection)

    comedia = Genero("Comédia")
    comedia.inserir_genero(connection)

    acao = Genero("Ação")
    acao.inserir_genero(connection)

    fantasia = Genero("Fantasia")
    fantasia.inserir_genero(connection)

    aventura = Genero("Aventura")
    aventura.inserir_genero(connection)

    super_heroi = Genero("Super-Heroi")
    super_heroi.inserir_genero(connection)

    terror = Genero("Terror")
    terror.inserir_genero(connection)

    # -------------------------------------------------
    # --------------- GeneroFilme ---------------------
    # -------------------------------------------------

    genero_oppenheimer = [
        GeneroFilme(oppenheimer.get_id_filme(connection), ficcao.get_id_genero(connection)),
        GeneroFilme(oppenheimer.get_id_filme(connection), drama.get_id_genero(connection)),
        GeneroFilme(oppenheimer.get_id_filme(connection), cinebiografica.get_id_genero(connection)),
    ]
    for genero in genero_oppenheimer:
        genero.inserir_genero_filme(connection)

    genero_barbie = GeneroFilme(barbie.get_id_filme(connection), comedia.get_id_genero(connection))
    genero_barbie.inserir_genero_filme(connection)

    genero_doutor_estranho_2 = [
        GeneroFilme(doutor_estranho_2.get_id_filme(connection), acao.get_id_genero(connection)),
        GeneroFilme(doutor_estranho_2.get_id_filme(connection), fantasia.get_id_genero(connection)),
        GeneroFilme(doutor_estranho_2.get_id_filme(connection), aventura.get_id_genero(connection)),
        GeneroFilme(doutor_estranho_2.get_id_filme(connection), super_heroi.get_id_genero(connection)),
        GeneroFilme(doutor_estranho_2.get_id_filme(connection), terror.get_id_genero(connection))
    ]
    for genero in genero_doutor_estranho_2:
        genero.inserir_genero_filme(connection)

    genero_deadpool = [
        GeneroFilme(deadpool.get_id_filme(connection), acao.get_id_genero(connection)),
        GeneroFilme(deadpool.get_id_filme(connection), comedia.get_id_genero(connection))
    ]
    for genero in genero_deadpool:
        genero.inserir_genero_filme(connection)

    # -------------------------------------------------
    # ----------------- Função -----------------------
    # -------------------------------------------------
    diretor = Funcao("Diretor")
    diretor.inserir_funcao(connection)

    ator = Funcao("Ator")
    ator.inserir_funcao(connection)

    # -------------------------------------------------
    # ----------------- Pessoas -----------------------
    # -------------------------------------------------
    nolan = Pessoa("Christopher Nolan", SexoPessoa.MASCULINO)
    nolan.inserir_pessoa(connection)

    cillian_murphy = Pessoa("Cillian Murphy", SexoPessoa.MASCULINO)
    cillian_murphy.inserir_pessoa(connection)

    emily_blunt = Pessoa("Emily Blunt", SexoPessoa.FEMININO)
    emily_blunt.inserir_pessoa(connection)

    rober_downeyjr = Pessoa("Robert Downey Jr.", SexoPessoa.MASCULINO)
    rober_downeyjr.inserir_pessoa(connection)

    margot_robbie = Pessoa("Margot Robbie", SexoPessoa.FEMININO)
    margot_robbie.inserir_pessoa(connection)

    ryan_gosling = Pessoa("Ryan Gosling", SexoPessoa.MASCULINO)
    ryan_gosling.inserir_pessoa(connection)

    america_ferreira = Pessoa("America Ferreira", SexoPessoa.FEMININO)
    america_ferreira.inserir_pessoa(connection)

    greta_gerwig = Pessoa("Greta Gerwig", SexoPessoa.FEMININO)
    greta_gerwig.inserir_pessoa(connection)

    benedict_cumberbatch = Pessoa("Benedict Cumberbatch", SexoPessoa.MASCULINO)
    benedict_cumberbatch.inserir_pessoa(connection)

    elizabeth_olsen = Pessoa("Elizabeth Olsen", SexoPessoa.FEMININO)
    elizabeth_olsen.inserir_pessoa(connection)

    xochitl_gomez = Pessoa("Xochitl Gomez", SexoPessoa.FEMININO)
    xochitl_gomez.inserir_pessoa(connection)

    benedic_wong = Pessoa("Benedict Wong", SexoPessoa.MASCULINO)
    benedic_wong.inserir_pessoa(connection)

    sam_raimi = Pessoa("Sam Raimi", SexoPessoa.MASCULINO)
    sam_raimi.inserir_pessoa(connection)

    david_leitch = Pessoa("David Leitch", SexoPessoa.MASCULINO)
    david_leitch.inserir_pessoa(connection)

    rayn_reynolds = Pessoa("Rayn Reynolds", SexoPessoa.MASCULINO)
    rayn_reynolds.inserir_pessoa(connection)

    josh_brolin = Pessoa("Josh Brolin", SexoPessoa.MASCULINO)
    josh_brolin.inserir_pessoa(connection)

    zazie_beetz = Pessoa("Zazie Beetz", SexoPessoa.FEMININO)
    zazie_beetz.inserir_pessoa(connection)

    joao_pedro = Pessoa("João Pedro", SexoPessoa.MASCULINO)
    joao_pedro.inserir_pessoa(connection)

    jhessica = Pessoa("Jhessica", SexoPessoa.FEMININO)
    jhessica.inserir_pessoa(connection)

    # -------------------------------------------------
    # --------------- Funcionarios --------------------
    # -------------------------------------------------
    oppenheimer_funcionarios = [
        FuncionarioFilme(nolan.get_id_pessoa(connection), oppenheimer.get_id_filme(connection), diretor.get_id_funcao(connection)),
        FuncionarioFilme(cillian_murphy.get_id_pessoa(connection), oppenheimer.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(emily_blunt.get_id_pessoa(connection), oppenheimer.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(rober_downeyjr.get_id_pessoa(connection), oppenheimer.get_id_filme(connection), ator.get_id_funcao(connection)),
    ]

    for funcionario in oppenheimer_funcionarios:
        funcionario.inserir_funcionario_filme(connection)

    barbie_funcionarios = [
        FuncionarioFilme(greta_gerwig.get_id_pessoa(connection), barbie.get_id_filme(connection), diretor.get_id_funcao(connection)),
        FuncionarioFilme(margot_robbie.get_id_pessoa(connection), barbie.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(ryan_gosling.get_id_pessoa(connection), barbie.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(america_ferreira.get_id_pessoa(connection), barbie.get_id_filme(connection), ator.get_id_funcao(connection)),
    ]

    for funcionario in barbie_funcionarios:
        funcionario.inserir_funcionario_filme(connection)

    doutor_estranho_2_funcionarios = [
        FuncionarioFilme(sam_raimi.get_id_pessoa(connection), doutor_estranho_2.get_id_filme(connection), diretor.get_id_funcao(connection)),
        FuncionarioFilme(benedict_cumberbatch.get_id_pessoa(connection), doutor_estranho_2.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(elizabeth_olsen.get_id_pessoa(connection), doutor_estranho_2.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(xochitl_gomez.get_id_pessoa(connection), doutor_estranho_2.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(benedic_wong.get_id_pessoa(connection), doutor_estranho_2.get_id_filme(connection), ator.get_id_funcao(connection)),
    ]

    for funcionario in doutor_estranho_2_funcionarios:
        funcionario.inserir_funcionario_filme(connection)

    deadpool_funcionarios = [
        FuncionarioFilme(david_leitch.get_id_pessoa(connection), deadpool.get_id_filme(connection), diretor.get_id_funcao(connection)),
        FuncionarioFilme(rayn_reynolds.get_id_pessoa(connection), deadpool.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(josh_brolin.get_id_pessoa(connection), deadpool.get_id_filme(connection), ator.get_id_funcao(connection)),
        FuncionarioFilme(zazie_beetz.get_id_pessoa(connection), deadpool.get_id_filme(connection), ator.get_id_funcao(connection)),
    ]
    for funcionario in deadpool_funcionarios:
        funcionario.inserir_funcionario_filme(connection)

    # -------------------------------------------------
    # --------------- Locais --------------------------
    # -------------------------------------------------
    cinema_sjda = Local("Cinema Shopping Jardim das Americas", "")
    cinema_sjda.inserir_local(connection)

    casa_da_mae = Local("Casa da Mae", "")
    casa_da_mae.inserir_local(connection)

    em_casa = Local("Em casa", "")
    em_casa.inserir_local(connection)

    casa_do_amigo = Local("Casa do Amigo", "")
    casa_do_amigo.inserir_local(connection)

    # -------------------------------------------------
    # ------------------ Sessao -----------------------
    # -------------------------------------------------

    sessao_deadpool_1 = Sessao(date(2023, 12, 27), "", deadpool.get_id_filme(connection), cinema_sjda.get_id_local(connection))
    sessao_deadpool_1.inserir_sessao(connection)

    # -------------------------------------------------
    # --------------- SessaoPessoa --------------------
    # -------------------------------------------------
    sessao_pessoa_deadpool_1 = [
        SessaoPessoa(joao_pedro.get_id_pessoa(connection), sessao_deadpool_1.get_id_sessao(connection)),
        SessaoPessoa(jhessica.get_id_pessoa(connection), sessao_deadpool_1.get_id_sessao(connection)),
    ]
    for sessao_pessoa in sessao_pessoa_deadpool_1:
        sessao_pessoa.inserir_sessao_pessoa(connection)

# Programa
connection = conectar_banco()

# criar_tabelas(connection)

# popular_tabelas(connection)

console = TerminalUI()

while console.main_menu != 99 and console.auxiliar_menu != 99:
    try:
        console.run_interface()
    except KeyboardInterrupt:
        break
    except sql.Error as e:
        print(f"Erro ao executar a consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    except:
        print("Erro inesperado!!")

connection.close()