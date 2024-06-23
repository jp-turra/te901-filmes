from __future__ import print_function, unicode_literals

import re
import time
import sqlite3 as sql
import argparse

from enum import Enum
from classes import *
from PyInquirer import prompt, Validator, ValidationError
from populate_db import criar_tabelas, popular_tabelas

parser = argparse.ArgumentParser()
parser.add_argument("--create -c", action="store_true", dest="create_tables", default=False, help="Cria e popula todas as tabelas antes de iniciar a UI")

class Menu(Enum):
    SAIR=0
    CADASTRAR_FILME=1
    CADASTRAR_SESSAO=2
    LISTAR_FILMES_NOTA=3
    LISTAR_FILMES_TITULO=4
    LISTAR_SESSOES=6
    CONSULTAR_TODOS_FILMES=5
    CONSULTAR_SESSAO=7

    def get_main_choices():
        items = []
        for item in Menu:
            items.append({
                'key': item.name,
                'name': item.name.replace('_', ' ').title(),
                'value': str(item.value)
            })
        
        return items
    
class TextValidator(Validator):
    def validate(self, document):
        text = document.text

        if len(text) == 0:
            raise ValidationError(
                message="O campo não pode estar vazio.",
                cursor_position=len(text)
            )

        return True

class GradeValidator(Validator):
    def validate(self, document):
        try:
            number = int(document.text)
            if number < 0 or number > 5:
                raise ValueError

            return True
        except ValueError:
            raise ValidationError(
                message="A nota deve ser um número entre 0 e 5.",
                cursor_position=len(document.text)
            )

class DateValidator(Validator):
    def validate(self, document):
        try:
            date = str(document.text).strip()
            regexp_pattern = "^[0-9]{2}/[0-9]{2}/[0-9]{4}$"

            if len(date) == 0:
                raise ValueError
            
            res = re.match(regexp_pattern, date)
            if res is None:
                raise ValueError
            
            res_group = date.split('/')
            if int(res_group[0]) < 0 or int(res_group[0]) > 31:
                raise ValueError
            
            if int(res_group[1]) < 0 or int(res_group[1]) > 12:
                raise ValueError
            
            # Primeiro filme criado foi em 1895
            if int(res_group[2]) < 1895:
                raise ValueError
            
            struct_data = time.strptime(date, "%d/%m/%Y")
            if time.strftime("%Y/%m/%d", struct_data) > time.strftime("%Y/%m/%d", time.localtime()):
                raise ValidationError(
                    message="Data inválida. A data deve ser menor que a data atual.",
                    cursor_position=len(document.text)
                )
            
            return True
        except ValueError as error:
            raise ValidationError(
                message="Data inválida. dd/mm/aaaa. Verifique se o dia, mês e ano sao validos.",
                cursor_position=len(document.text)
            )
                

class Question(Enum):

    MAIN=[{
        'type': 'list',
        'name': 'menu',
        'message': 'Escolha uma opção',
        'choices': Menu.get_main_choices()
    }]

    ADD_MOVIE = [
        {
            'type': 'input',
            'name': 'title',
            'message': 'Insira o nome do filme:',
            'validate': TextValidator
        },
        {
            'type': 'input',
            'name': 'grade',
            'message': 'Insira a nota do filme:',
            'validate': GradeValidator
        },
        {
            'type': 'input',
            'name': 'comment',
            'message': 'Insira o comentário do filme:',
            'validate': TextValidator
        },
        {
            'type': 'list',
            'name': 'studio',
            'message': 'Insira o estúdio do filme:',
            'choices': ['Studio 1', 'Studio 2', 'Studio 3', 'Adicionar Novo Estúdio']
        },
        {
            'type': 'input',
            'name': 'studio_name',
            'message': 'Insira o nome do estúdio:',
            'when': lambda answers: answers['studio'] == 'Adicionar Novo Estúdio',
            'validate': TextValidator
        },
        {
            'type': 'checkbox',
            'name': 'diretor',
            'message': 'Selecione o(a) diretor(a) do filme:',
            'choices': ['Diretor 1', 'Diretor 2', 'Diretor 3'],
            'validate': lambda answers: len(answers['people']) > 0
        },
        {
            'type': 'checkbox',
            'name': 'actors',
            'message': 'Selecione os(as) atores(izes) do filme:',
            'choices': ['Ator 1', 'Ator 2', 'Ator 3'],
            'validate': lambda answers: len(answers['people']) > 0
        },
        {
            'type': 'checkbox',
            'name': 'genres',
            'message': 'Selecione os generos do filme:',
            'choices': ['Genero 1', 'Genero 2', 'Genero 3'],
            'validate': lambda answers: len(answers['people']) > 0
        }
    ]

    ADD_SESSION = [
        {
            'type': 'list',
            'name': 'movie',
            'message': 'Insira o filme da sessão:',
            'choices': ['Filme 1', 'Filme 2', 'Filme 3'],
        },
        {
            'type': 'input',
            'name': 'date',
            'message': 'Insira a data da sessão (dd/mm/aaaa):',
            'validate': DateValidator
        },
        {
            'type': 'list',
            'name': 'place',
            'message': 'Selecione o local da sessão:',
            'choices': ['Local 1', 'Local 2', 'Local 3', 'Adicionar Novo Local'],
        },
        {
            'type': 'checkbox',
            'name': 'people',
            'message': 'Selecione as pessoas que participaram da sessão:',
            'choices': ['Pessoa 1', 'Pessoa 2', 'Pessoa 3'],
            'validate': lambda answers: len(answers['people']) > 0
        },
        {
            'type': 'input',
            'name': 'comment',
            'message': 'Insira o comentário da sessão:',
            'validate': TextValidator
        }
    ]

    ADD_PLACE = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Insira o Nome do Local:',
            'validate': TextValidator,
        },
        {
            'type': 'input',
            'name': 'comment',
            'message': 'Insira o Comentário do Local:',
            'validate': TextValidator
        },
    ]

    ADD_PERSON = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Insira o Nome da Pessoa:',
            'validate': TextValidator
        },
        {
            'type': 'list',
            'name': 'sex',
            'message': 'Insira o Sexo da Pessoa:',
            'choices': [
                {
                    'name': 'Masculino',
                    'value': SexoPessoa.MASCULINO,
                    'short': 'Masc'
                },
                {
                    'name': 'Feminino',
                    'value': SexoPessoa.FEMININO,
                    'short': 'Fem'
                }
            ]
        }
    ]

    ADD_EXTRA_PERSON = [
        {
            'type': 'list',
            'name': 'add_extra_person',
            'message': 'Deseja adicionar mais uma pessoa?',
            'choices': ['Sim', 'Nao']
        }
    ]

    ADD_GENRE = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Insira o Nome do Genero:',
            'validate': TextValidator
        }
    ]

    ADD_EXTRA_GENRE = [
        {
            'type': 'list',
            'name': 'add_extra_genre',
            'message': 'Deseja adicionar mais um genero?',
            'choices': ['Sim', 'Nao']
        }
    ]

    LIST_SESSIONS_RESULT = [
        {
            'type': 'list',
            'name': 'session',
            'message': 'Lista de sessões encontradas:',
            'choices': ['Nenhum resultado encontrado', 'Voltar']
        }
    ]

class UserInterface():

    def __init__(self):
        pass

    def start(self, connection: sql.Connection):
        while(True):
            try:
                answare = prompt(Question.MAIN.value)
            
                if answare['menu'] == str(Menu.SAIR.value):
                    exit()
                elif answare['menu'] == str(Menu.CADASTRAR_FILME.value):
                    self.add_movie_menu(connection)
                elif answare['menu'] == str(Menu.CADASTRAR_SESSAO.value):
                    self.add_session_menu(connection)
                elif answare['menu'] == str(Menu.LISTAR_FILMES_NOTA.value):
                    self.list_movies_by_grade(connection)
                elif answare['menu'] == str(Menu.LISTAR_FILMES_TITULO.value):
                    self.list_movies_by_title(connection)
                elif answare['menu'] == str(Menu.LISTAR_SESSOES.value):
                    self.list_sessions_by_date(connection)
                elif answare['menu'] == str(Menu.CONSULTAR_TODOS_FILMES.value):
                    self.list_movies(connection)
                elif answare['menu'] == str(Menu.CONSULTAR_SESSAO.value):
                    self.list_sessions(connection)
            except KeyboardInterrupt:
                print("Interrupção do usuário!")
                break

    def add_genre_menu(self, connection: sql.Connection) -> int:
        genre_id = 0

        answares = prompt(Question.ADD_GENRE.value)

        genero = Genero(answares['name'])
        try:
            genero.inserir_genero(connection)
            genre_id = genero.get_id_genero(connection)

            return genre_id
        except sql.Error as e:
            print(f"Erro ao inserir genero: {e}")
            return 0



    def add_movie_menu(self, connection: sql.Connection) -> int:
        estudio_id = 0

        # Lista todos os estúdios
        Question.ADD_MOVIE.value[3]['choices'] = list(
            map(
                lambda x: {
                    'name': x.nome,
                    'value': x.id_estudio,
                    'short': x.nome
                }, 
                Estudio.listar_todos_estudios(connection)
            )
        )
        Question.ADD_MOVIE.value[3]['choices'].append({'name': 'Adicionar Novo Estúdio', 'value': 'Adicionar Novo Estúdio', 'short': 'Adicionar Novo Estúdio'})

        # Lista todos os diretores
        funcao_list = Funcao.procurar_funcao(connection, "Diretor")
        diretor = None if len(funcao_list) == 0 else funcao_list[0]
        funcao_diretor_id = diretor.id_funcao if diretor is not None else 0
        Question.ADD_MOVIE.value[5]['choices'] = list(
            map(
                lambda x: {
                    'name': x['name'],
                    'value': x['value'],
                    'short': x['name']
                }, 
                FuncionarioFilme.listar_todos_nomes(connection, funcao_diretor_id)
            )
        )
        Question.ADD_MOVIE.value[5]['choices'].append({'name': 'Adicionar Novo Diretor', 'value': 'Adicionar Novo Diretor', 'short': 'Adicionar Novo Diretor'})

        #Lista todos os atores
        funcao_list = Funcao.procurar_funcao(connection, "Ator")
        actor = None if len(funcao_list) == 0 else funcao_list[0]
        actor_function_id = actor.id_funcao if actor is not None else 0
        Question.ADD_MOVIE.value[6]['choices'] = list(
            map(
                lambda x: {
                    'name': x['name'],
                    'value': x['value'],
                    'short': x['name']
                }, 
                FuncionarioFilme.listar_todos_nomes(connection, actor_function_id)
            )
        )
        Question.ADD_MOVIE.value[6]['choices'].append({'name': 'Adicionar Novo Ator', 'value': 'Adicionar Novo Ator', 'short': 'Adicionar Novo Ator'})

        # Lista todos os generos
        Question.ADD_MOVIE.value[7]['choices'] = list(
            map(
                lambda x: {
                    'name': x.nome,
                    'value': x.id_genero,
                    'short': x.nome
                }, 
                Genero.procurar_genero(connection)
            )
        )
        Question.ADD_MOVIE.value[7]['choices'].append({'name': 'Adicionar Novo Genero', 'value': 'Adicionar Novo Genero', 'short': 'Adicionar Novo Genero'})

        answares = prompt(Question.ADD_MOVIE.value)
        
        if answares['studio'] == 'Adicionar Novo Estúdio':
            estudio = Estudio(answares["studio_name"])
            estudio.inserir_estudio(connection)
            estudio_id = estudio.get_id_estudio(connection)
        else:
            estudio_id = int(answares['studio'])
        
        filme = Filme(
            answares['title'],
            answares['comment'],
            answares['grade'],
            estudio_id
        )
        filme.inserir_filme(connection)

        id_filme = filme.get_id_filme(connection)

        for diretor in answares['diretor']:
            person_id = 0
            if diretor == 'Adicionar Novo Diretor':
                print("Adicionar Novo(a) Diretor(a)")
                person_id = self.add_people_menu(connection)
                film_function = FuncionarioFilme(person_id, id_filme, funcao_diretor_id)
                film_function.inserir_funcionario_filme(connection)

                # Mostra menu para adicionar pessoas extras
                new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)
                while new_person_answares['add_extra_person'] == "Sim":
                    print("Adicionar Novo(a) Diretor(a) Extra")
                    extra_person_id = self.add_people_menu(connection)
                    film_function = FuncionarioFilme(extra_person_id, id_filme, funcao_diretor_id)
                    film_function.inserir_funcionario_filme(connection)
                    new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)

            else:
                person_id = int(diretor)
                film_function = FuncionarioFilme(person_id, id_filme, funcao_diretor_id)
                film_function.inserir_funcionario_filme(connection)

        for actor in answares['actors']:
            person_id = 0
            if actor == 'Adicionar Novo Ator':
                print("Adicionar Novo(a) Ator(iz)")
                person_id = self.add_people_menu(connection)
                film_function = FuncionarioFilme(person_id, id_filme, actor_function_id)
                film_function.inserir_funcionario_filme(connection)

                # Mostra menu para adicionar pessoas extras
                new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)
                while new_person_answares['add_extra_person'] == "Sim":
                    print("Adicionar Novo(a) Ator(iz) Extra")
                    extra_person_id = self.add_people_menu(connection)
                    film_function = FuncionarioFilme(extra_person_id, id_filme, actor_function_id)
                    film_function.inserir_funcionario_filme(connection)
                    new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)

            else:
                person_id = int(actor)
                film_function = FuncionarioFilme(person_id, id_filme, actor_function_id)
                film_function.inserir_funcionario_filme(connection)

        for genre in answares['genres']:
            if genre == 'Adicionar Novo Genero':
                genre_id = self.add_genre_menu(connection)
                if genre_id != 0:
                    film_genre = GeneroFilme(id_filme, genre_id)
                    film_genre.inserir_genero_filme(connection)
                

                # Mostra menu para adicionar generos extras
                new_genre_answares = prompt(Question.ADD_EXTRA_GENRE.value)
                while new_genre_answares['add_extra_genre'] == "Sim":
                    extra_genre_id = self.add_genre_menu(connection)
                    if extra_genre_id != 0:
                        film_genre = GeneroFilme(id_filme, extra_genre_id)
                        film_genre.inserir_genero_filme(connection)
                    
                    new_genre_answares = prompt(Question.ADD_EXTRA_GENRE.value)
            else:
                genre_id = int(genre)
                film_genre = GeneroFilme(id_filme, genre_id)
                film_genre.inserir_genero_filme(connection)

        return id_filme

    def add_place_menu(self, connection: sql.Connection) -> int:
        answares = prompt(Question.ADD_PLACE.value)

        local = Local(answares['name'], answares['comment'])
        local.inserir_local(connection)

        id_local = local.get_id_local(connection)

        # print("Local {} foi inserido com ID={}!".format(local.nome, id_local))

        return id_local
    
    def add_people_menu(self, connection: sql.Connection) -> int:
        answares = prompt(Question.ADD_PERSON.value)

        people = Pessoa(answares['name'], answares['sex'])
        people.inserir_pessoa(connection)

        id_people = people.get_id_pessoa(connection)

        # print("Pessoa {} foi inserida com ID={}!".format(people.nome, id_people))

        return id_people

    def add_session_menu(self, connection: sql.Connection):
        add_movie_index = -1
        add_local_index = -1
        add_person_index = -1

        # Encontra o index da lista correspondente a cada menu
        for submenu in Question.ADD_SESSION.value:
            if submenu['name'] == 'movie':
                add_movie_index = Question.ADD_SESSION.value.index(submenu)
            elif submenu['name'] == 'place':
                add_local_index = Question.ADD_SESSION.value.index(submenu)
            elif submenu['name'] == 'people':
                add_person_index = Question.ADD_SESSION.value.index(submenu)
        
        # Retorna erro caso uma das opções de adição de sessão não forem encontradas
        if add_movie_index == -1 or add_local_index == -1 or add_person_index == -1:
            raise Exception('Erro ao encontrar as opções de adição de sessão!')


        # Atualiza menu de filmes com os listados no banco de dados + a opção de novos filmes.
        Question.ADD_SESSION.value[add_movie_index]['choices'] = list(
            map(
                lambda x: {
                    'name': x.titulo,
                    'value': x.id_filme,
                    'short': x.titulo
                }, 
                Filme.listar_todos_filmes(connection)
            )
        )
        Question.ADD_SESSION.value[add_movie_index]['choices'].append({'name': 'Adicionar Novo Filme', 'value': 'Adicionar Novo Filme', 'short': 'Adicionar Novo Filme'})

        # Atualiza menu de locais com os listados no banco de dados + a opção de novos locais.
        Question.ADD_SESSION.value[add_local_index]['choices'] = list(
            map(
                lambda x: {
                    'name': x.nome,
                    'value': x.id_local,
                    'short': x.nome
                }, 
                Local.listar_todos_locais(connection)
            )
        )
        Question.ADD_SESSION.value[add_local_index]['choices'].append({'name': 'Adicionar Novo Local', 'value': 'Adicionar Novo Local', 'short': 'Adicionar Novo Local'})

        # Atualiza menu de pessoas com os listados no banco de dados + a opção de novas pessoas.
        Question.ADD_SESSION.value[add_person_index]['choices'] = list(
            map(
                lambda x: {
                    'name': x.nome,
                    'value': x.id_pessoa,
                    'short': x.nome
                }, 
                Pessoa.listar_todas_pessoas(connection)
            )
        )
        Question.ADD_SESSION.value[add_person_index]['choices'].append({'name': 'Adicionar Nova Pessoa', 'value': 'Adicionar Nova Pessoa', 'short': 'Adicionar Nova Pessoa'})

        # Pergunta ao usuário as opções de adição de sessão.
        answares = prompt(Question.ADD_SESSION.value)
        id_local = answares['place']
        id_filme = answares['movie']

        # Adiciona o novo filme caso a opção de adição de novo filme tenha sido escolhida
        if answares['movie'] == 'Adicionar Novo Filme':
            id_filme = self.add_movie_menu(connection)

        # Adiciona o novo local caso a opção de adição de novo local tenha sido escolhida
        if answares['place'] == 'Adicionar Novo Local':
            id_local = self.add_place_menu(connection)
        
        # Cria a nova sessão
        sessao = Sessao(answares['date'], answares['comment'], id_filme, id_local)
        sessao.inserir_sessao(connection)

        # print("Sessão {} foi inserida com ID={}!".format(sessao.data_visto, sessao.get_id_sessao(connection)))

        # Passa por cada pessoa selecionada e adiciona na sessão
        for person in answares['people']:
            
            # Adiciona nova pessoa caso a opção de adição de nova pessoa tenha sido escolhida
            if person == 'Adicionar Nova Pessoa':
                person_id = self.add_people_menu(connection)
                sessao_pessoa = SessaoPessoa(person_id, sessao.get_id_sessao(connection))
                sessao_pessoa.inserir_sessao_pessoa(connection)

                # Mostra menu para adicionar pessoas extras
                new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)
                while new_person_answares['add_extra_person'] == "Sim":
                    extra_person_id = self.add_people_menu(connection)
                    sessao_pessoa = SessaoPessoa(extra_person_id, sessao.get_id_sessao(connection))
                    sessao_pessoa.inserir_sessao_pessoa(connection)
                    new_person_answares = prompt(Question.ADD_EXTRA_PERSON.value)

            else:
                # Adiciona pessoa existente a uma sessão
                sessao_pessoa = SessaoPessoa(int(person), sessao.get_id_sessao(connection))
                sessao_pessoa.inserir_sessao_pessoa(connection)
                # print("Pessoa {} inserida na sessão {}!".format(sessao_pessoa.id_pessoa, sessao.id_sessao))
    
    def list_movies_by_grade(self, connection: sql.Connection):
        filmes = Filme.listar_filmes_ordenado(connection, "titulo, nota", "nota DESC")
        for filme in filmes:
            print("Nota: {} - Filme: {}".format(filme.nota, filme.titulo))
        
        input("Pressione qualquer tecla para continuar...")
        
    
    def list_movies_by_title(self, connection: sql.Connection):
        filmes = Filme.listar_filmes_ordenado(connection, "titulo, nota", "titulo ASC")
        print("Nota\t\tFilme")
        for filme in filmes:
            print("Nota: {} - Filme: {}".format(filme.nota, filme.titulo))
        input("Pressione qualquer tecla para continuar...")
        
    
    def list_sessions_by_date(self, connection):
        sessoes = Sessao.listar_sessoes(connection, "data_visto, id_filme, id_sessao", "data_visto DESC", do_inner_join=True)

        Question.LIST_SESSIONS_RESULT.value[0]['choices'] = list(
            map(
                lambda x: {
                    'name': "Sessão {} - {}".format(Sessao.struct_time_to_str_date(x.data_visto), x.filme.titulo),
                    'value': x.id_sessao,
                    'short': "Sessão {} - {}".format(Sessao.struct_time_to_str_date(x.data_visto), x.filme.titulo)
                }, 
                sessoes
            )
        )
        Question.LIST_SESSIONS_RESULT.value[0]['choices'].append({'name': 'Voltar', 'value': 0, 'short': 'Voltar'})
        
        resposta = prompt(Question.LIST_SESSIONS_RESULT.value)

        return int(resposta['session'])

    
    def list_movies(self, connection: sql.Connection):
            filmes = Filme.listar_filmes_completo(connection)

            # Exibindo os resultados formatados
            for filme in filmes:
                print(f"\nFilme: {filme['ID Filme']}")
                print(f"Título: {filme['Título']}")
                print(f"Comentário do filme: {filme['Comentário']}")
                print(f"Nota: {filme['Nota']}")
                print(f"Estúdio: {filme['Estúdio']}")
                print(f"Gêneros: {filme['Gêneros']}")
                print(f"Funcionários: {filme['Funcionários']}")
                print()
                print("-" * 40)

            input("Pressione qualquer tecla para voltar")
    
    def list_sessions(self, connection):
        id_sessao = self.list_sessions_by_date(connection)
        
        if 0 == id_sessao:
            return

        sessoes = Sessao.listar_sessao_completo(connection, id_sessao)

        # sessoes = list(map(lambda x: {
        #     'ID Sessão': x[0],
        #     'Data Visto': x[1],
        #     'Comentario': x[2],
        #     'Título do Filme': x[3],
        #     'Comentario Filme': x[4],
        #     'Nota Filme': x[5],
        #     'Gêneros': x[6],
        #     'Local': x[7],
        #     'Comentario Local': x[8],
        #     'Pessoas': x[9],
        # }, rows))
            
        # Exibindo os resultados formatados
        for sessao in sessoes:
            data = Sessao.str_date_to_struct_time(sessao['Data Visto'], "%Y/%m/%d")
            print("\nSessão: {}".format(sessao['ID Sessão']))
            print("Data Visto: {}".format(Sessao.struct_time_to_str_date(data)))
            print("Comentário da sessão: {}".format(sessao['Comentario']))
            print("Título do Filme: {}".format(sessao['Título do Filme']))
            print("Comentário do filme: {}".format(sessao['Comentario Filme']))
            print("Nota do filme: {}".format(sessao['Nota Filme']))
            print("Gêneros: {}".format(sessao['Gêneros']))
            print("Local: {}".format(sessao['Local']))
            print("Comentário do local: {}".format(sessao['Comentario Local']))
            print("Pessoas: {}".format(sessao['Pessoas']))
            print()  # Linha em branco entre o conteúdo e a linha de separação
            print("-" * 40)

        input("Pressione qualquer tecla para voltar")


if __name__ == "__main__":
    connection = sql.connect("database/filmes.db")

    args = parser.parse_args()

    if args.create_tables:
        criar_tabelas(connection)
        popular_tabelas(connection)

    UserInterface().start(connection)