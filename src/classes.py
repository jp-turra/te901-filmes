import sqlite3 as sql
import time

from pprint import pprint
from typing import List, Dict

class Estudio:
    id_estudio = 0
    nome = ""

    def __init__(self, nome: str, id: int = 0) -> None:
        self.nome = nome
        self.id_estudio = id

    def set_id_estudio(self, id: int):
        self.id_estudio = id

    def get_id_estudio(self, connection: sql.Connection):
        try:
            if self.id_estudio == 0:
                estudio = self.procurar_estudio(connection, self.nome)
                if len(estudio) > 0:
                    self.id_estudio = int(estudio[0].id_estudio)
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
        estudios: List[Estudio] = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM estudio WHERE id_estudio = ? OR nome = ?", (id, nome))
            rows = cursor.fetchall()

            estudios = list(map(
                lambda x: Estudio(x[1], x[0]),
                rows
            ))

        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            cursor.close()
            return estudios
    
    @staticmethod
    def listar_todos_estudios(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM estudio")
            rows = cursor.fetchall()
           
            estudios = list(map(
                lambda x: Estudio(x[1], x[0]),
                rows
            ))

            return estudios
        except sql.Error as e:
            print(f"[listar_todos_estudios] Erro ao executar a consulta: {e}")
            return []
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

    def __init__(self, titulo: str, comentario: str, nota: int, id_estudio: int, id: int = 0) -> None:
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
                    self.id_filme = int(filme[0].id_filme)
                else:
                    raise sql.Error(f"Filme '{self.titulo}' não existe!")
        
            return self.id_filme
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
        
    def inserir_filme(self, connection: sql.Connection):
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
        filmes: List[Filme] = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM filme WHERE id_filme = ? OR titulo = ?", (id, nome))
            rows = cursor.fetchall()

            filmes = list(map(
                lambda x: Filme(x[1], x[2], x[3], x[4], x[0]),
                rows
            ))
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
        finally:
            cursor.close()
            return filmes
    
    @staticmethod
    def listar_todos_filmes(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM filme")
            rows = cursor.fetchall()

            filmes = list(map(
                lambda x: Filme(x[1], x[2], x[3], x[4], x[0]),
                rows
            ))

            return filmes
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def listar_filmes_completo(connection: sql.Connection):
        query = """
            SELECT
                Filme.id_filme,
                Filme.titulo,
                Filme.comentario,
                Filme.nota,
                Estudio.nome AS nome_estudio,
                GROUP_CONCAT(DISTINCT ' ' || Genero.nome || ' ') AS generos,
                GROUP_CONCAT(DISTINCT ' ' || Pessoa.nome || ' (' || Funcao.nome || ') ') AS funcionarios
            FROM
                Filme
            LEFT JOIN Estudio ON Filme.id_estudio = Estudio.id_estudio
            LEFT JOIN GeneroFilme ON Filme.id_filme = GeneroFilme.id_filme
            LEFT JOIN Genero ON GeneroFilme.id_genero = Genero.id_genero
            LEFT JOIN FuncionarioFilme ON Filme.id_filme = FuncionarioFilme.id_filme
            LEFT JOIN Pessoa ON FuncionarioFilme.id_pessoa = Pessoa.id_pessoa
            LEFT JOIN Funcao ON FuncionarioFilme.id_funcao = Funcao.id_funcao
            GROUP BY
                Filme.id_filme, Estudio.nome;
        """
        
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            

            # Formatando o output
            filmes = list(map(lambda x: {
                'ID Filme': x[0],
                'Título': x[1],
                'Comentário': x[2],
                'Nota': x[3],
                'Estúdio': x[4],
                'Gêneros': x[5],
                'Funcionários': x[6] 
            }, rows))
            
            return filmes
        
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def listar_filmes_ordenado(connection: sql.Connection, column: str = "*", order: str = "id ASC"):
        filmes: List[Filme] = []
        id_filme_pos = -1
        titulo_pos = -1
        comentario_pos = -1
        nota_pos = -1
        id_estudio_pos = -1
        try:
            if column == "*":
                id_filme_pos = 0
                titulo_pos = 1
                comentario_pos = 2
                nota_pos = 3
                id_estudio_pos = 4
            else:
                column_list = column.split(", ")

                for i in range(len(column_list)):
                    if column_list[i] == "id_filme":
                        id_filme_pos = i
                    elif column_list[i] == "titulo":
                        titulo_pos = i
                    elif column_list[i] == "comentario":
                        comentario_pos = i
                    elif column_list[i] == "nota":
                        nota_pos = i
                    elif column_list[i] == "id_estudio":
                        id_estudio_pos = i
                    

            cursor = connection.cursor()
            cursor.execute(f"SELECT {column} FROM Filme ORDER BY {order}")
            rows = cursor.fetchall()

            for row in rows:
                filmes.append(
                    Filme(
                        row[titulo_pos] if titulo_pos >= 0 else "",
                        row[comentario_pos] if comentario_pos >= 0 else "",
                        int(row[nota_pos]) if nota_pos >= 0 else 0,
                        row[id_estudio_pos] if id_estudio_pos >= 0 else "",
                        row[id_filme_pos] if id_filme_pos >= 0 else 0
                    )
                )
            
            return filmes
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
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
            genero = self.procurar_genero(connection, nome=self.nome)
            if len(genero) > 0:
                self.id_genero = genero[0].id_genero
            else:
                print(f"Genero '{self.nome}' não existe!")
                return 0
    
        return self.id_genero

    def inserir_genero(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            generos = self.procurar_genero(connection, self.nome)
            if len(generos) > 0:
                raise sql.Error(f"Genero '{self.nome}' ja existe!")
            cursor.execute("INSERT INTO genero (nome) VALUES (?)", (self.nome))
            connection.commit()
            print(f"Genero '{self.nome}' inserido com sucesso!")
        except sql.Error as e:
            print(f"Erro ao inserir genero: {e}")
        finally:
            cursor.close()

    @staticmethod
    def procurar_genero(connection: sql.Connection, nome: str = "", id_genero: int = 0):
        generos: List[Genero] = []
        try:
            cursor = connection.cursor()
            if id_genero != 0:
                cursor.execute("SELECT * FROM genero WHERE id_genero = ?", (id_genero))
            elif nome != "":
                cursor.execute("SELECT * FROM genero WHERE nome LIKE ?", (nome))
            else:
                cursor.execute("SELECT * FROM genero ORDER BY nome")

            rows = cursor.fetchall()

            generos = list(map(
                lambda x: Genero(x[1], x[0]),
                rows
            ))
            return generos

        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
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
            return
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
                self.id_pessoa = pessoa[0].id_pessoa
            else:
                raise sql.Error(f"Pessoa '{self.nome}' nao existe!")
            
            return self.id_pessoa
        except sql.Error as e:
            print(f"[get_id_pessoa] Erro ao recuperar id_pessoa: {e}")
            return 0

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
            print(f"[inseririr_pessoa] Erro ao inserir pessoa: {e}")
        finally:
            cursor.close()

    @staticmethod
    def procurar_pessoa(connection: sql.Connection, nome: str, id_pessoa: int = 0):
        pessoa: List[Pessoa] = []
        try:
            cursor = connection.cursor()

            if id_pessoa > 0:
                cursor.execute("SELECT * FROM Pessoa WHERE id_pessoa = ?", (id_pessoa,))
            elif len(nome) > 0:
                cursor.execute("SELECT * FROM Pessoa WHERE nome LIKE ?", (nome,))
            else:
                cursor.execute("SELECT * FROM Pessoa")

            rows = cursor.fetchall()

            pessoa = list(map(
                lambda x: Pessoa(x[1], x[2], x[0]), rows
            ))

            return pessoa

        except sql.Error as e:
            print(f"[procurar_pessoa] Erro ao executar a consulta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def listar_todas_pessoas(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Pessoa")
            rows = cursor.fetchall()

            pessoas = list(map(
                lambda x: Pessoa(x[1], x[2], x[0]), rows
            ))

            return pessoas
        except sql.Error as e:
            print(f"[listar_todas_pessoas] Erro ao executar a consulta: {e}")
            return []
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
            print(f"[print_tabela] Erro ao executar a consulta Pessoa: {e}")
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
                funcao_list = self.procurar_funcao(connection, self.nome)
                funcao = None if len(funcao_list) == 0 else funcao_list
                if funcao is not None and len(funcao) > 0:
                    self.id_funcao = funcao[0].id_funcao
                else:
                    raise sql.Error(f"Função '{self.nome}' nao existe")

            return self.id_funcao
        except sql.Error as e:
            print(f"[get_id_funcao] Erro ao recuperar id_funcao: {e}")

    def inserir_funcao(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            funcao_list = self.procurar_funcao(connection, self.nome)
            funcao = None if len(funcao_list) == 0 else funcao_list
            if funcao is not None and len(funcao) > 0:
                raise sql.Error(f"Função '{self.nome}' ja existe")
            
            cursor.execute("INSERT INTO Funcao (nome) VALUES (?)", (self.nome,))
            connection.commit()
        except sql.Error as e:
            print(f"[inserir_funcao] Erro ao inserir funcao: {e}")
        finally:
            cursor.close()

    @staticmethod
    def procurar_funcao(connection: sql.Connection, nome: str, id_funcao: int = 0):
        jobs: List[Funcao] = []
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM Funcao"
            if id_funcao > 0:
                cursor.execute(query + " WHERE id_funcao = ?", (id_funcao,))
            elif len(nome) > 0:
                cursor.execute(query + " WHERE nome = ?", (nome,))
            else:
                cursor.execute(query)

            rows = cursor.fetchall()

            jobs = list(map(
                lambda x: Funcao(x[1], x[0]), rows
            ))

            return jobs

        except sql.Error as e:
            print(f"[procurar_funcao]: Erro ao executar a consulta: {e}")
            return []
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
            if funcionario_filme is not None:
                raise sql.Error(f"FuncionarioFilme id_pessoa='{self.id_pessoa}' id_filme='{self.id_filme}' id_funcao='{self.id_funcao}' ja existe")

            cursor.execute("INSERT INTO FuncionarioFilme (id_pessoa, id_filme, id_funcao) VALUES (?, ?, ?)", (self.id_pessoa, self.id_filme, self.id_funcao))
            connection.commit()
        except sql.Error as e:
            print(f"Erro ao inserir FuncionarioFilme: {e}")
        finally:
            cursor.close()

    def procurar_funcionario_filme(self, connection: sql.Connection, id_pessoa: int, id_filme: int, id_funcao: int):
        workers: List[FuncionarioFilme] = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM FuncionarioFilme WHERE id_pessoa = ? AND id_filme = ? AND id_funcao = ?", (id_pessoa, id_filme, id_funcao))
            rows = cursor.fetchall()

            workers = list(map(
                lambda x: FuncionarioFilme(x[0], x[1], x[2]), rows
            ))

            return None if len(workers) == 0 else workers[0]
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            cursor.close()
       
    @staticmethod
    def listar_todos_nomes(connection: sql.Connection, funcao_id: int = 0) -> List[Dict[str, str]]:
        try:
            cursor = connection.cursor()
            if funcao_id == 0:
                cursor.execute("""SELECT Pessoa.nome, FuncionarioFilme.id_pessoa FROM FuncionarioFilme 
                                INNER JOIN Pessoa USING (id_pessoa) 
                                ORDER BY Pessoa.nome""")
            else:
                cursor.execute("""SELECT Pessoa.nome, FuncionarioFilme.id_pessoa FROM FuncionarioFilme 
                                INNER JOIN Pessoa ON (
                                    FuncionarioFilme.id_pessoa = Pessoa.id_pessoa AND FuncionarioFilme.id_funcao = ?)
                                ORDER BY Pessoa.nome""", (funcao_id,))

            rows = cursor.fetchall()

            workers = list(map(
                lambda x: {"name": x[0], "value": x[1]}, rows
            ))

            return workers
        except sql.Error as e:
            print(f"[listar_todos_nomes] Erro ao executar a consulta: {e}")
            return []
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
            print(f"[print_tabela] Erro ao executar a consulta FuncionarioFilme: {e}")
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
                    self.id_local = local[0].id_local
                else:
                    raise sql.Error(f"Local '{self.nome}' não existe")
                
            return self.id_local
        
        except sql.Error as e:
            print(f"[get_id_local] Erro ao executar a consulta: {e}")

    def inserir_local(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            local = self.procurar_local(connection, self.nome)
            if len(local) > 0:
                raise sql.Error(f"Local '{self.nome}' ja existe")
            
            cursor.execute("INSERT INTO Local (nome, comentario) VALUES (?, ?)", (self.nome, self.comentario))
            connection.commit()
        except sql.Error as e:
            print(f"[inserir_local] Erro ao inserir Local: {e}")
        finally:
            cursor.close()

    @staticmethod
    def procurar_local(connection: sql.Connection, nome: str, id_local: int = 0):
        locais: List[Local] = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Local WHERE id_local = ? OR nome = ?", (id_local, nome))
            rows = cursor.fetchall()

            locais = list(map(
                lambda x: Local(x[1], x[2], x[0]), rows
            ))

        except sql.Error as e:
            print(f"[procurar_local] Erro ao executar a consulta: {e}")
        finally:
            cursor.close()
            return locais

    @staticmethod
    def listar_todos_locais(connection: sql.Connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Local")
            rows = cursor.fetchall()

            locais = list(map(
                lambda x: Local(x[1], x[2], x[0]), rows
            ))

            return locais
        except sql.Error as e:
            print(f"[listar_todos_locais] Erro ao executar a consulta Local: {e}")
            return []
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
            print(f"[print_tabela] Erro ao executar a consulta Local: {e}")
        finally:
            cursor.close()

class Sessao:
    id_sessao = 0
    data_visto = None
    comentario = ""
    id_filme = 0
    id_local = 0

    def __init__(self, data: str, comentario: str, id_filme: int, id_local: Local, id: int = 0) -> None:
        self.id_sessao = id
        try:
            self.data_visto = self.str_date_to_struct_time(data, '%Y/%m/%d')
        except:
            if data != "":
                self.data_visto = self.str_date_to_struct_time(data)
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
                    self.id_sessao = sessao[0].id_sessao
                else:
                    raise sql.Error(f"Sessão '{self.data_visto}' não existe")
                
            return self.id_sessao
        
        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return 0

    def inserir_sessao(self, connection: sql.Connection):
        try:
            cursor = connection.cursor()
            sessao = self.procurar_sessao(connection, self.data_visto, self.id_filme, self.id_local)
            if len(sessao) > 0:
                raise sql.Error(f"Sessão '{self.struct_time_to_str_date(self.data_visto)}' ja existe")
            
            data_visto_str = Sessao.struct_time_to_str_date(self.data_visto, '%Y/%m/%d')
            cursor.execute("INSERT INTO Sessao (data_visto, comentario, id_filme, id_local) VALUES (?, ?, ?, ?)", (data_visto_str, self.comentario, self.id_filme, self.id_local))
            connection.commit()
            print(f"Sessão data '{self.struct_time_to_str_date(self.data_visto)}' id_filme '{self.id_filme}' id_local '{self.id_local}' inserida com sucesso")	
        except sql.Error as e:
            print(f"[inserir_sessao] Erro ao inserir Sessão: {e}")
        finally:
            cursor.close()

    @staticmethod
    def listar_sessoes(connection: sql.Connection, columns: str, order_by: str = "", limit: str = "", do_inner_join: bool = False):
        sessoes: List[Sessao] = []
        filme: Filme
        local: Local

        try:
            cursor = connection.cursor()

            data_pos = -1
            comentario_pos = -1
            id_filme_pos = -1
            id_local_pos = -1
            id_sessao_pos = -1

            query = f"SELECT {columns} FROM Sessao"

            split_columns = columns.split(",")
            for i in range(len(split_columns)):
                if split_columns[i].replace(" ", "") == "data_visto":
                    data_pos = i
                elif split_columns[i].replace(" ", "") == "comentario":
                    comentario_pos = i
                elif split_columns[i].replace(" ", "") == "id_filme":
                    id_filme_pos = i
                    if do_inner_join:
                        query += " INNER JOIN Filme USING (id_filme)"
                elif split_columns[i].replace(" ", "") == "id_local":
                    id_local_pos = i
                elif split_columns[i].replace(" ", "") == "id_sessao":
                    id_sessao_pos = i

            if order_by != "":
                query += f" ORDER BY {order_by}"
            
            if limit != "":
                query += f" LIMIT {limit}"

            cursor.execute(query)
            rows = cursor.fetchall()

            sessoes = list(map(
                lambda x: Sessao(
                    x[data_pos] if data_pos >= 0 else "", 
                    x[comentario_pos] if comentario_pos >= 0 else "", 
                    x[id_filme_pos] if id_filme_pos >= 0 else 0, 
                    x[id_local_pos] if id_local_pos >= 0 else 0,
                    x[id_sessao_pos] if id_sessao_pos >= 0 else 0
                ), rows
            ))

            if do_inner_join:
                for sessao in sessoes:
                    if id_filme_pos >= 0:
                        sessao.filme = Filme.procurar_filme(connection, "", sessao.id_filme)[0]
                    if id_local_pos >= 0:
                        sessao.local = Local.procurar_local(connection, "", sessao.id_local)[0]

            return sessoes
        except sql.Error as e:
            print(f"[listar_sessoes] Erro ao executar a consulta Sessão: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def listar_sessao_completo(connection: sql.Connection, id_sessao: int = 0):
        id_sessao_query = ""
        if id_sessao > 0:
            id_sessao_query = f"AND Sessao.id_sessao = {id_sessao}"

        query = f"""
        SELECT
            Sessao.id_sessao,
            Sessao.data_visto,
            Sessao.comentario AS comentario_sessao,
            Filme.titulo,
            Filme.comentario AS comentario_filme,
            Filme.nota,
            GROUP_CONCAT(DISTINCT ' ' || Genero.nome) AS generos,
            Local.nome AS nome_local,
            Local.comentario AS comentario_local,
            GROUP_CONCAT(DISTINCT ' ' || Pessoa.nome || ' ') AS pessoas
        FROM
            Sessao
        INNER JOIN Filme ON Sessao.id_filme = Filme.id_filme {id_sessao_query}
        INNER JOIN Local ON Sessao.id_local = Local.id_local
        INNER JOIN SessaoPessoa ON (Sessao.id_sessao = SessaoPessoa.id_sessao)
        INNER JOIN Pessoa ON SessaoPessoa.id_pessoa = Pessoa.id_pessoa
        INNER JOIN GeneroFilme ON Filme.id_filme = GeneroFilme.id_filme
        INNER JOIN Genero ON GeneroFilme.id_genero = Genero.id_genero
        GROUP BY
            Sessao.id_sessao;
        """
        
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Formatando o output
            sessoes = list(map(lambda x: {
                'ID Sessão': x[0],
                'Data Visto': x[1],
                'Comentario': x[2],
                'Título do Filme': x[3],
                'Comentario Filme': x[4],
                'Nota Filme': x[5],
                'Gêneros': x[6],
                'Local': x[7],
                'Comentario Local': x[8],
                'Pessoas': x[9],
            }, rows))

            return sessoes

        except sql.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def str_date_to_struct_time(date: str, format: str = '%d/%m/%Y') -> time.struct_time:
        return time.strptime(date, format)
    
    @staticmethod
    def struct_time_to_str_date(date: time.struct_time, format: str = '%d/%m/%Y') -> str:
        return time.strftime(format, date)

    @staticmethod
    def procurar_sessao(connection: sql.Connection, data_visto: time.struct_time, id_filme: int, id_local: int, id_sessao: int = 0):
        sessoes: List[Sessao] = []
        try:
            cursor = connection.cursor()
            if id_sessao > 0:
                cursor.execute(""" SELECT * FROM Sessao WHERE id_sessao = ?""", (id_sessao,))
            else:
                data_visto_str = Sessao.struct_time_to_str_date(data_visto, '%Y/%m/%d')
                cursor.execute(""" SELECT * FROM Sessao WHERE data_visto = ? AND id_filme = ? AND id_local = ?""", (data_visto_str, id_filme, id_local))

            rows = cursor.fetchall()
            
            sessoes = list(map(
                lambda x: Sessao(x[1], x[2], x[3], x[4], x[0]), rows
            ))
            
            return sessoes

        except sql.Error as e:
            print(f"[procurar_sessao] Erro ao executar a consulta: {e}")
            return []
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
            print(f"[print_tabela] Erro ao executar a consulta Sessao: {e}")
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
            print(f"[inserir_sessao_pessoa] Erro ao inserir SessãoPessoa: {e}")
        finally:
            cursor.close()

    def procurar_sessao_pessoa(self, connection: sql.Connection, id_pessoa: int = 0, id_sessao: int = 0):
        sessao_pessoas: List[SessaoPessoa] = []
        try:
            cursor = connection.cursor()
            if id_sessao > 0 and id_pessoa == 0:
                cursor.execute(" SELECT * FROM SessaoPessoa WHERE id_sessao = ?", (id_sessao,))
            elif id_pessoa > 0 and id_sessao == 0:
                cursor.execute(" SELECT * FROM SessaoPessoa WHERE id_pessoa = ?", (id_pessoa,))
            elif id_pessoa > 0 and id_sessao > 0:
                cursor.execute(" SELECT * FROM SessaoPessoa WHERE id_pessoa = ? AND id_sessao = ?", (id_pessoa, id_sessao))
            else:
                cursor.execute(" SELECT * FROM SessaoPessoa")

            rows = cursor.fetchall()

            sessao_pessoas = list(map(
                lambda x: SessaoPessoa(x[0], x[1]), rows
            ))

            return sessao_pessoas
        except sql.Error as e:
            print(f"[procurar_sessao_pessoa] Erro ao executar a consulta: {e}")
            return []
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
            print(f"[print_tabela] Erro ao executar a consulta SessaoPessoa: {e}")
        finally:
            cursor.close()
