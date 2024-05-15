from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from pprint import pprint
from enum import Enum

class MenuOptions(Enum):
    MAIN=0x00,
    SEARCH=0x01,
    ADD=0x02,
    EXIT=0x99

class TableOptions(Enum):
    FILME=0x01,
    ESTUDIO=0x02,
    GENERO=0x03,
    PESSOA=0x04,
    FUNCAO=0x05,
    FUNCIONARIO=0x06,
    LOCAL=0x07,
    SESSAO=0x8,
    PARTICIPANTE_SESSAO=0x09,
    VOTAR=0x00,
    SAIR=0x99

class UserInterface():
    current_menu = 0


    main_menu = [
        {
            'type': 'list',
            'name': 'menu_choice',
            'message': 'Selecione sua opção:',
            'choices': [
                {
                    'name': 'Pesquisar',
                    'value': MenuOptions.SEARCH
                },
                {
                    'name': 'Cadastrar',
                    'value': MenuOptions.ADD
                },
                {
                    'name': 'Sair',
                    'value': MenuOptions.EXIT
                }
            ],
        }
    ]

    tables = [
        {
            'type': 'list',
            'name': 'table_choice',
            'message': 'Selecione sua opção:',
            'choices': [
                {
                    'name': 'Filme',
                    'value': TableOptions.FILME
                },
                {
                    'name': 'Estudio',
                    'value': TableOptions.ESTUDIO
                },
                {
                    'name': 'Genero',
                    'value': TableOptions.GENERO
                },
                {
                    'name': 'Pessoa',
                    'value': TableOptions.PESSOA
                },
                {
                    'name': 'Função',
                    'value': TableOptions.FUNCAO
                },
                {
                    'name': 'Funcionário',
                    'value': TableOptions.FUNCIONARIO
                },
                {
                    'name': 'Local',
                    'value': TableOptions.LOCAL
                },
                {
                    'name': 'Sessão',
                    'value': TableOptions.SESSAO
                },
                {
                    'name': 'Participante na Sessão',
                    'value': TableOptions.PARTICIPANTE_SESSAO
                },
                {
                    'name': 'Votar',
                    'value': TableOptions.VOTAR
                },
                {
                    'name': 'Sair',
                    'value': TableOptions.SAIR
                }
            ],
        }
    ]



    def __init__(self) -> None:
        pass

    def handle_main_menu_choice(self, answare) -> None:
        choice = answare['menu_choice']

        if choice == MenuOptions.EXIT:
            exit(0)
        
        self.current_menu = choice

    def handle_add_menu_choice(self, answare) -> None:
        choice = answare['add_menu']

        if choice == TableOptions.SAIR:
            exit(0)
        if choice == TableOptions.VOTAR:
            self.current_menu
                 
        
        self.current_menu = choice

    def run(self) -> None:
        if self.current_menu == 0x00:
            self.handle_main_menu_choice(prompt(self.main_menu))

        if self.current_menu == 0x01:
            self.tables["name"] = "add_menu"
            self.handle_add_menu_choice(prompt(self.tables))
        
        if self.current_menu == 0x02:
            self.tables["name"] = "search_menu"
            self.handle_add_menu_choice(prompt(self.tables))

if __name__ == '__main__':
    while True:
        try:
            UserInterface().run()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)