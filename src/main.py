from __future__ import print_function, unicode_literals

import re
import datetime

from PyInquirer import prompt, Validator, ValidationError
from enum import Enum
from typing import List, Dict

class Menu(Enum):
    SAIR=0
    CADASTRAR_FILME=1
    CADASTRAR_SESSAO=2
    LISTAR_FILMES_NOTA=3
    LISTAR_FILMES_TITULO=4
    LISTAR_SESSOES=6
    CONSULTAR_TODOS_FILMES=5
    CONSULTAR_TODAS_SESSOES=7

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
            if int(res_group[2]) < 1895 or int(res_group[2]) > datetime.date.today().year:
                raise ValueError
            
            return True
        except ValueError:
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
            'message': 'Insira o estuário do filme:',
            # TODO: Criar opções relacionando os estúdios cadastrados no BD
            'choices': ['Studio 1', 'Studio 2', 'Studio 3', 'Adicionar Novo Estúdio']
        },
        {
            'type': 'input',
            'name': 'studio_name',
            'message': 'Insira o nome do estuário:',
            'when': lambda answers: answers['studio'] == 'Adicionar Novo Estúdio',
            'validate': TextValidator
        }
    ]

    ADD_SESSION = [
        {
            'type': 'list',
            'name': 'movie',
            'message': 'Insira o filme da sessão:',
            # TODO: Criar opções relacionando os filmes cadastrados no BD
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
            # TODO: Criar opções relacionando os locais cadastrados no BD
            'choices': ['Local 1', 'Local 2', 'Local 3', 'Adicionar Novo Local'],
        },
        {
            'type': 'input',
            'name': 'place_name',
            'message': 'Insira o nome do local:',
            'when': lambda answers: answers['place'] == 'Adicionar Novo Local',
            'validate': TextValidator,
            'when': lambda answers: answers['place'] == 'Adicionar Novo Local',
        },
        {
            'type': 'input',
            'name': 'place_comment',
            'message': 'Insira o comentário do local:',
            'when': lambda answers: answers['place'] == 'Adicionar Novo Local',
            'validate': TextValidator
        },
        {
            'type': 'checkbox',
            'name': 'people',
            'message': 'Selecione as pessoas que participaram da sessão:',
            # TODO: Criar opções relacionando as pessoas cadastradas no BD
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


class UserInterface():

    def __init__(self):
        pass

    def start(self):
        while(True):
            try:
                answare = prompt(Question.MAIN.value)
            
                if answare['menu'] == str(Menu.SAIR.value):
                    exit()
                elif answare['menu'] == str(Menu.CADASTRAR_FILME.value):
                    self.add_movie_menu()
                elif answare['menu'] == str(Menu.CADASTRAR_SESSAO.value):
                    self.add_session_menu()
                elif answare['menu'] == str(Menu.LISTAR_FILMES_NOTA.value):
                    self.list_movies_by_grade()
                elif answare['menu'] == str(Menu.LISTAR_FILMES_TITULO.value):
                    self.list_movies_by_title()
                elif answare['menu'] == str(Menu.LISTAR_SESSOES_CRONO_DESC.value):
                    self.list_sessions_by_date()
                elif answare['menu'] == str(Menu.CONSULTAR_TODOS_FILMES.value):
                    self.list_movies()
                elif answare['menu'] == str(Menu.CONSULTAR_TODAS_SESSOES.value):
                    self.list_sessions()
            except KeyboardInterrupt:
                print("Interrupção do usuário!")
                break

    
    def add_movie_menu(self):
        answares = prompt(Question.ADD_MOVIE.value)
        print("Você está criando um novo filme!")
        print("Nome: ", answares['title'])
        print("Nota: ", answares['grade'])
        print("Comentário: ", answares['comment'])
        if answares['studio'] == 'Adicionar Novo Estúdio':
            print("Estúdio: ", answares['studio_name'])
        else:
            print("Estúdio: ", answares['studio'])
        
        # TODO: Adicionar filme ao banco de dados


    def add_session_menu(self):
        answares = prompt(Question.ADD_SESSION.value)
        print("Você está criando uma nova sessão!")
        print("Filme: ", answares['movie'])
        print("Data: ", answares['date'])
        if answares['place'] == 'Adicionar Novo Local':
            print("Local: ", answares['place_name'])
            print("Comentário: ", answares['place_comment'])
        else:
            print("Local: ", answares['place'])
        print("Pessoas: ", answares['people'])
        print("Comentário: ", answares['comment'])
        
        # TODO: Adicionar sessão ao banco de dados
    
    def list_movies_by_grade(self):
        pass
    
    def list_movies_by_title(self):
        pass
    
    def list_sessions_by_date(self):
        pass
    
    def list_movies(self):
        pass
    
    def list_sessions(self):
        pass
        
if __name__ == "__main__":
    UserInterface().start()