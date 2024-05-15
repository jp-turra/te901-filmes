import sqlite3 as sql
from datetime import date
from pprint import pprint

class Estudio:
    id_estudio = 0
    nome = ""

    def __init__(self, nome: str) -> None:
        self.nome = nome

    def set_id_estudio(self, id: int):
        self.id_estudio = id

    def get_id_estudio(self, connection: sql.Connection):
        try:
            if self.id_estudio == 0:
                estudio = self.procurar_estudio(connection, self.nome)
                if len(estudio) > 0:
                    self.id_estudio = int(estudio[0][0])
                else:
                    raise sql.Error(f"Estudio '{self.nome}' nao existe!")
            
            return self.id_estudio
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")

    def inserir_estudio(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            estudios = self.procurar_estudio(connection, self.nome)
            if len(estudios) > 0:
                raise sql.Error(f"Estudio '{self.nome}' ja existe!")

            cursor.execute("INSERT INTO estudio (nome) VALUES (?)", (self.nome,))
            connection.commit()
            print(f"Estudio '{self.nome}' inserido com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir estudio: {e}")
        finally:
            cursor.close()
    
    @staticmethod
    def procurar_estudio(connection: sql.Connection, nome: str, id: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM estudio WHERE id_estudio = ? OR nome = ?", (id, nome))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Estudio")
            rows = cursor.fetchall()
            print("id_estudio\tnome")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

class Filme:
    id_filme = 0
    titulo = ""
    nota = 0
    id_estudio = 0

    def __init__(self, titulo: str, comentario: str, nota: int, id_estudio: Estudio, id: int = 0) -> None:
        self.titulo = titulo
        self.comentario = comentario
        self.nota = nota
        self.id_estudio = id_estudio
        self.id_filme = id


    def set_id_filme(self, id: int):
        self.id_filme = id

    def get_id_filme(self, connection: sql.Connection):
        try:
            if self.id_filme == 0:
                filme = self.procurar_filme(connection, self.titulo)
                if len(filme) > 0:
                    self.id_filme = filme[0][0]
                else:
                    raise sql.Error(f"Filme '{self.titulo}' não existe!")
        
            return self.id_filme
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        
    def interir_filme(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            filmes = self.procurar_filme(connection, self.titulo)
            if len(filmes) > 0:
                raise sql.Error(f"Filme '{self.titulo}' ja existe!")

            cursor.execute("INSERT INTO filme (titulo, comentario, nota, id_estudio) VALUES (?, ?, ?, ?)", (self.titulo, self.comentario, self.nota, self.id_estudio))
            connection.commit()
            print(f"Filme '{self.titulo}' inserido com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir filme: {e}")
        finally:
            cursor.close()
    
    @staticmethod
    def procurar_filme(connection: sql.Connection, nome: str, id: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM filme WHERE id_filme = ? OR titulo = ?", (id, nome))
            rows = cursor.fetchall()
            
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Filme")
            rows = cursor.fetchall()
            print("id_filme\ttitulo\tcomentario\tnota\tid_estudio")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

class Genero:
    id_genero = 0
    nome = ""

    def __init__(self, nome: str, id_genero: int = 0) -> None:
        self.nome = nome
        self.id_genero = id_genero

    def set_id_genero(self, id: int):
        self.id_genero = id

    def get_id_genero(self, connection: sql.Connection):
        if self.id_genero == 0:
            genero = self.procurar_genero(connection, self.nome)
            if len(genero) > 0:
                self.id_genero = genero[0][0]
            else:
                print(f"Genero '{self.nome}' não existe!")
                return None
    
        return self.id_genero

    def inserir_genero(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            generos = self.procurar_genero(connection, self.nome)
            if len(generos) > 0:
                raise sql.Error(f"Genero '{self.nome}' ja existe!")
            cursor.execute("INSERT INTO genero (nome) VALUES (?)", (self.nome,))
            connection.commit()
            print(f"Genero '{self.nome}' inserido com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir genero: {e}")
        finally:
            cursor.close()

    @staticmethod
    def procurar_genero(connection: sql.Connection, nome: str, id_genero: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM genero WHERE id_genero = ? OR nome LIKE ?", (id_genero, nome))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Genero")
            rows = cursor.fetchall()
            print("id_genero\tnome")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

class GeneroFilme:
    id_filme = 0
    id_genero = 0

    def __init__(self, id_filme: int, id_genero: int) -> None:
        self.id_filme = id_filme
        self.id_genero = id_genero

    def inserir_genero_filme(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            genero_filme = self.procurar_genero_filme(connection, self.id_filme, self.id_genero)
            if len(genero_filme) > 0:
                raise sql.Error(f"GeneroFilme '{self.id_filme}' '{self.id_genero}' ja existe!")
                
            cursor.execute("INSERT INTO GeneroFilme (id_filme, id_genero) VALUES (?, ?)", (self.id_filme, self.id_genero))
            connection.commit()
        except sql.Error as e:
            print(f"Erro ao inserir genero_filme: {e}")
        finally:
            cursor.close()

        
    def procurar_genero_filme(self, connection: sql.Connection, id_filme: int, id_genero: int):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM GeneroFilme WHERE id_filme = ? AND id_genero = ?", (id_filme, id_genero))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()


    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM GeneroFilme")
            rows = cursor.fetchall()
            print("id_filme\tid_genero")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta GeneroFilme: {e}")
        finally:
            cursor.close()

class SexoPessoa (enumerate):
    FEMININO = 0
    MASCULINO = 1

class Pessoa:
    id_pessoa = 0
    nome = ""
    sexo = 0

    def __init__(self, nome: str, sexo: SexoPessoa, id: int = 0) -> None:
        self.id_pessoa = id
        self.nome = nome
        self.sexo = sexo

    def set_id_pessoa(self, id: int):
        self.id_pessoa = id

    def get_id_pessoa(self, connection: sql.Connection):
        try:
            pessoa = self.procurar_pessoa(connection, self.nome)
            if len(pessoa) > 0:
                self.id_pessoa = pessoa[0][0]
            else:
                raise sql.Error(f"Pessoa '{self.nome}' nao existe!")
            
            return self.id_pessoa
        except sql.Error as e:
            print(f"Erro ao recuperar id_pessoa: {e}")

    def inserir_pessoa(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            pessoa = self.procurar_pessoa(connection, self.nome)
            if len(pessoa) > 0:
                raise sql.Error(f"Pessoa '{self.nome}' ja existe!")
            
            cursor.execute("INSERT INTO Pessoa (nome, sexo) VALUES (?, ?)", (self.nome, self.sexo))
            connection.commit()
            print(f"Pessoa '{self.nome}' inserida com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir pessoa: {e}")
        finally:
            cursor.close()

    def procurar_pessoa(self, connection: sql.Connection, nome: str, id_pessoa: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Pessoa WHERE id_pessoa = ? OR nome = ?", (id_pessoa, nome))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Pessoa")
            rows = cursor.fetchall()
            title = ["id_pessoa", "nome", "sexo"]
            rows = list(rows)
            rows.insert(0, title)
            pprint(rows)
                    
        except sql.Error as e:
            print(f"Erro ao executar a consulta Pessoa: {e}")
        finally:
            cursor.close()

class Funcao:
    id_funcao = 0
    nome = ""

    def __init__(self, nome: str,  id: int = 0) -> None:
        self.id_funcao = id
        self.nome = nome

    def set_id_funcao(self, id: int):
        self.id_funcao = id

    def get_id_funcao(self, connection: sql.Connection):
        try:
            if self.id_funcao == 0:
                funcao = self.procurar_funcao(connection, self.nome)
                if len(funcao) > 0:
                    self.id_funcao = funcao[0][0]
                else:
                    raise sql.Error(f"Função '{self.nome}' nao existe")

            return self.id_funcao
        except sql.Error as e:
            print(f"Erro ao recuperar id_funcao: {e}")

    def inserir_funcao(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            funcao = self.procurar_funcao(connection, self.nome)
            if len(funcao) > 0:
                raise sql.Error(f"Função '{self.nome}' ja existe")
            
            cursor.execute("INSERT INTO Funcao (nome) VALUES (?)", (self.nome,))
            connection.commit()
        except sql.Error as e:
            print(f"Erro ao inserir funcao: {e}")
        finally:
            cursor.close()

    def procurar_funcao(self, connection: sql.Connection, nome: str, id_funcao: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Funcao WHERE id_funcao = ? OR nome = ?", (id_funcao, nome))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Funcao")
            rows = cursor.fetchall()
            print("id_funcao\tnome")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta Funcao: {e}")
        finally:
            cursor.close()

class FuncionarioFilme:
    id_pessoa = 0
    id_filme = 0
    id_funcao = 0

    def __init__(self, id_pessoa: int, id_filme: int, id_funcao: Funcao) -> None:
        self.id_pessoa = id_pessoa
        self.id_filme = id_filme
        self.id_funcao = id_funcao

    def inserir_funcionario_filme(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            funcionario_filme = self.procurar_funcionario_filme(connection, self.id_pessoa, self.id_filme, self.id_funcao)
            if len(funcionario_filme) > 0:
                raise sql.Error(f"FuncionarioFilme id_pessoa='{self.id_pessoa}' id_filme='{self.id_filme}' id_funcao='{self.id_funcao}' ja existe")

            cursor.execute("INSERT INTO FuncionarioFilme (id_pessoa, id_filme, id_funcao) VALUES (?, ?, ?)", (self.id_pessoa, self.id_filme, self.id_funcao))
            connection.commit()
        except sql.Error as e:
            print(f"Erro ao inserir FuncionarioFilme: {e}")
        finally:
            cursor.close()

    def procurar_funcionario_filme(self, connection: sql.Connection, id_pessoa: int, id_filme: int, id_funcao: int):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM FuncionarioFilme WHERE id_pessoa = ? AND id_filme = ? AND id_funcao = ?", (id_pessoa, id_filme, id_funcao))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM FuncionarioFilme")
            rows = cursor.fetchall()
            print("id_pessoa\tid_filme\tid_funcao")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta FuncionarioFilme: {e}")
        finally:
            cursor.close()

class Local:
    id_local = 0
    nome = ""
    comentario = ""

    def __init__(self, nome: str, comentario: str, id: int = 0) -> None:
        self.id_local = id
        self.nome = nome
        self.comentario = comentario
    
    def set_id_local(self, id: int):
        self.id_local = id

    def get_id_local(self, connection: sql.Connection):
        try:
            if self.id_local == 0:
                local = self.procurar_local(connection, self.nome)
                if len(local) > 0:
                    self.id_local = local[0][0]
                else:
                    raise sql.Error(f"Local '{self.nome}' não existe")
                
            return self.id_local
        
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")

    def inserir_local(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            local = self.procurar_local(connection, self.nome)
            if len(local) > 0:
                raise sql.Error(f"Local '{self.nome}' ja existe")
            
            cursor.execute("INSERT INTO Local (nome, comentario) VALUES (?, ?)", (self.nome, self.comentario))
            connection.commit()
        except sql.Error as e:
            print(f"Erro ao inserir Local: {e}")
        finally:
            cursor.close()

    def procurar_local(self, connection: sql.Connection, nome: str, id_local: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Local WHERE id_local = ? OR nome = ?", (id_local, nome))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Local")
            rows = cursor.fetchall()
            print("id_local\tnome\tcomentario")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta Local: {e}")
        finally:
            cursor.close()

class Sessao:
    id_sessao = 0
    data_visto = None
    comentario = ""
    id_filme = 0
    id_local = 0

    def __init__(self, data: date, comentario: str, id_filme: int, id_local: Local, id: int = 0) -> None:
        self.id_sessao = id
        self.data_visto = data
        self.comentario = comentario
        self.id_filme = id_filme
        self.id_local = id_local

    def set_id_sessao(self, id: int):
        self.id_sessao = id
    
    def get_id_sessao(self, connection: sql.Connection):
        try:
            if self.id_sessao == 0:
                sessao = self.procurar_sessao(connection, self.data_visto, self.id_filme, self.id_local)
                if len(sessao) > 0:
                    self.id_sessao = sessao[0][0]
                else:
                    raise sql.Error(f"Sessão '{self.data_visto}' não existe")
                
            return self.id_sessao
        
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")

    def inserir_sessao(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            sessao = self.procurar_sessao(connection, self.data_visto, self.id_filme, self.id_local)
            if len(sessao) > 0:
                raise sql.Error(f"Sessão '{self.data_visto}' ja existe")
            
            cursor.execute("INSERT INTO Sessao (data_visto, comentario, id_filme, id_local) VALUES (?, ?, ?, ?)", (self.data_visto, self.comentario, self.id_filme, self.id_local))
            connection.commit()
            print(f"Sessão data '{self.data_visto}' id_filme '{self.id_filme}' id_local '{self.id_local}' inserida com sucesso")	
        except sql.Error as e:
            print(f"Erro ao inserir Sessão: {e}")
        finally:
            cursor.close()

    def procurar_sessao(self, connection: sql.Connection, data_visto: date, id_filme: int, id_local: int, id_sessao: int = 0):
        try:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * FROM Sessao WHERE id_sessao = ? OR (data_visto = ? AND id_filme = ? AND id_local = ?)""", (id_sessao, data_visto, id_filme, id_local))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()

    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Sessao")
            rows = cursor.fetchall()
            print("id_sessao\tdata_visto\tcomentario\tid_filme\tid_local")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta Sessao: {e}")
        finally:
            cursor.close()

class SessaoPessoa:
    id_pessoa = 0
    id_sessao = 0

    def __init__(self, id_pessoa: int, id_sessao: int) -> None:
        self.id_pessoa = id_pessoa
        self.id_sessao = id_sessao

    def inserir_sessao_pessoa(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            sessao_pessoa = self.procurar_sessao_pessoa(connection, self.id_pessoa, self.id_sessao)
            if len(sessao_pessoa) > 0:
                raise sql.Error(f"SessãoPessoa id_pessoa='{self.id_pessoa}' id_sessao='{self.id_sessao}' ja existe")
            
            cursor.execute("INSERT INTO SessaoPessoa (id_pessoa, id_sessao) VALUES (?, ?)", (self.id_pessoa, self.id_sessao))
            connection.commit()
            print(f"SessãoPessoa id_pessoa='{self.id_pessoa}' id_sessao='{self.id_sessao}' inserida com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir SessãoPessoa: {e}")
        finally:
            cursor.close()

    def procurar_sessao_pessoa(self, connection: sql.Connection, id_pessoa: int, id_sessao: int):
        try:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * FROM SessaoPessoa WHERE id_pessoa = ? AND id_sessao = ?""", (id_pessoa, id_sessao))
            rows = cursor.fetchall()
            return rows
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()
    
    @staticmethod
    def print_tabela(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SessaoPessoa")
            rows = cursor.fetchall()
            print("id_pessoa\tid_sessao")
            for row in rows:
                for i in row:
                    print(i, end="\t")
        except sql.Error as e:
            print(f"Erro ao executar a consulta SessaoPessoa: {e}")
        finally:
            cursor.close()
