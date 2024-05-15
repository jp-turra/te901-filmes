import sqlite3
from datetime import date


# --------------------------------------------------------------------------------------------
# conectar ao banco de dados
def conectar_banco():
    con = sqlite3.connect('Bib.db')
    return con


# --------------------------------------------------------------------------------------------
# adastrar um novo livro
def cadastrar_livro(con, nome_livro):
    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO livros (livroNome) VALUES (?)", (nome_livro,))
        con.commit()
        print(f"\tLivro '{nome_livro}' cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"\tErro ao cadastrar livro: {e}")


# --------------------------------------------------------------------------------------------
# cadastrar um novo estudante
def cadastrar_estudante(con, nome, email):
    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO estudantes (estNome, estEmail) VALUES (?, ?)", (nome, email))
        con.commit()
        print(f"\tEstudante '{nome}' cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"\tErro ao cadastrar estudante: {e}")


# --------------------------------------------------------------------------------------------
# efetuar  empréstimo de livro para um estudante
def efetuar_emprestimo(con, est_id, livro_ids):
    try:
        cursor = con.cursor()
        data_emprestimo = date.today()
        for livro_id in livro_ids:
            cursor.execute("INSERT INTO emprestimos (estID, empData) VALUES (?, ?)", (est_id, data_emprestimo))
            emp_id = cursor.lastrowid
            cursor.execute("INSERT INTO livroEmprestado (empID, livroID) VALUES (?, ?)", (emp_id, livro_id))
        con.commit()
        print("\tEmpréstimo efetuado com sucesso!")
    except sqlite3.Error as e:
        print(f"\tErro ao efetuar empréstimo: {e}")


# --------------------------------------------------------------------------------------------
# efetuar a devolução de um livro
def efetuar_devolucao(con, livro_id):
    try:
        cursor = con.cursor()
        query = """
                UPDATE livroEmprestado SET empDataDev = ? 
                WHERE livroID = ? AND empDataDev IS NULL
                """
        cursor.execute(query, (date.today(), livro_id))
        con.commit()
        print("\tDevolução realizada com sucesso!")
    except sqlite3.Error as e:
        print(f"\tErro ao efetuar devolução: {e}")


# --------------------------------------------------------------------------------------------
# listar todos os empréstimos de um determinado aluno
def listar_emprestimos_estudante(con, est_id):
    try:
        cursor = con.cursor()
        query = """
        SELECT est.estNome, emp.empID, emp.empData, le.livroID, l.livroNome, empDataDev,
        CAST ((julianday('now') - julianday(emp.empData)) AS INTEGER)
        FROM  (((estudantes est 
        INNER JOIN emprestimos emp USING (estID))
        INNER JOIN livroEmprestado le USING (empID))
        INNER JOIN livros l USING (livroID))
        WHERE est.estID = ?"""

        cursor.execute(query, (est_id,))
        emprestimos = cursor.fetchall()
        if not emprestimos:  # estudantes sem DIVIDAS (sem emprestimo aberto)
            # nova query apenas para pegar o nome de quem não tem empréstimos pendentes
            try:
                cursor.execute("SELECT estNome FROM estudantes WHERE estID = ?;", (est_id,))
                nome = cursor.fetchone()
                if nome is not None:
                    print(f"\nEstudante de código: {est_id}\nNome: {nome[0]}\nNão possue empréstimos em aberto.")
                else:
                    print(f"\tCódigo {est_id} inexistente!")
            except sqlite3.Error as error:
                print(f"\tErro ao listar empréstimos de estudante: {error}")
        else:
            print(f"\nEstudante de código: {est_id}\nNome: {emprestimos[0][0]}")
            hoje = date.today()
            print("Relatório feito em:", hoje)
            print("Empréstimos: ")
            for linha in emprestimos:
                if linha[5] is None: # None na list equivale ao NULL do banco de dados
                    print(f"\t- empréstimo (cód {linha[1]}) feito há {linha[6]} dia(s) em {linha[2]} livro '{linha[4]}' (cód {linha[3]})")
                else:
                    print(f"\t- empréstimo (cód {linha[1]}) feito em {linha[2]}, devolvido em {linha[5]}, livro '{linha[4]}' (cód {linha[3]})")
    except sqlite3.Error as e:
        print(f"\tErro ao listar empréstimos de estudante: {e}")


# --------------------------------------------------------------------------------------------
# listar todos os devedores de livros
def listar_devedores(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * from devedores")
        devedores = cursor.fetchall()
        for devedor in devedores:
            print(f"\t- {devedor[1]} (cód {devedor[0]}), empréstimo (cód {devedor[2]}) feito em {devedor[3]},  livro '{devedor[6]}' (cód {devedor[5]})")
    except sqlite3.Error as e:
        print(f"Erro ao listar devedores: {e}")


# --------------------------------------------------------------------------------------------
# listar todo o acervo da biblioteca
def listar_acervo(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM livros")
        acervo = cursor.fetchall()
        print("\n>>> Listagem do acervo ")
        print("\n\tTotal de livros cadastrados: ", len(acervo))
        print(f"\n\tCódigo\tNome do Livro")
        print(f"\t------\t------------------------------")
        for livro in acervo:
            livro_id, livro_nome = livro
            print(f"\t{livro_id:4}\t{livro_nome}")
    except sqlite3.Error as e:
        print(f"Erro ao listar acervo da biblioteca: {e}")


# --------------------------------------------------------------------------------------------
# listar todos os estudantes em ordem alfabética
def listar_estudantes(con, ordem="cod"):
    try:
        cursor = con.cursor()
        query = "SELECT * FROM estudantes"
        if ordem == "alf":
            query += " ORDER BY estNome"
            print(query)
        cursor.execute(query)
        estudantes = cursor.fetchall()
        print("\n>>> Listagem dos estudantes ")
        print("\n\tTotal de estudantes cadastrados: ", len(estudantes))
        print("\n\tCódigo\tNome <Email>")
        print("\t------\t------------------------------------------------")
        for linha in estudantes:
            # acessando cada coluna da tabela como uma posição da tupla
            print(f"\t{linha[0]:4}\t{linha[1]} <{linha[2]}>")
    except sqlite3.Error as e:
        print(f"Erro ao listar acervo da biblioteca: {e}")


# --------------------------------------------------------------------------------------------
# listar todos os empréstimos de um determinado livro
def listar_emprestimos_livro(con, livro_id):
    try:
        cursor = con.cursor()
        query = """
                SELECT est.estNome, emp.empID, emp.empData, le.livroID, l.livroNome, empDataDev
                FROM  (((estudantes est 
                INNER JOIN emprestimos emp USING (estID))
                INNER JOIN livroEmprestado le USING (empID))
                INNER JOIN livros l USING (livroID))
                WHERE le.livroID = ?
                """
        cursor.execute(query, (livro_id,))
        emprestimos = cursor.fetchall()
        for emprestimo in emprestimos:
            print(f"\tEmprestimo cod: {emprestimo[1]}, estudante: {emprestimo[0]}, feito em {emprestimo[2]} ", end="")
            if emprestimo[5] is not None:
                print(f"devolvido em {emprestimo[5]}")
            else:
                print("em andamento.")
    except sqlite3.Error as e:
        print(f"\tErro ao listar empréstimos do livro: {e}")

# programa principal que exibe o menu e aciona as funções correspondentes
con = conectar_banco()
while True:
    print("\n----->  Menu  <----\n")
    print("\t0 - Sair")
    print("\t1 - Cadastrar livro")
    print("\t2 - Cadastrar estudante")
    print("\t3 - Efetuar empréstimo")
    print("\t4 - Efetuar devolução")
    print("\t5 - Listar todos os empréstimos de um estudante")
    print("\t6 - Listar todos os devedores de livros")
    print("\t7 - Listar todo o acervo da biblioteca")
    print("\t8 - Listar todos os empréstimos de um livro")
    print("\t9 - Listar todos os estudantes (código)")
    print("\t10 - Listar todos os estudantes (alfabético)")

    opcao = input("\n\tOpção: ")

    if opcao == '1':
        print("\n>>> Cadastro de livro ")
        nome_livro = input("\n\tTitulo do livro: ")
        cadastrar_livro(con, nome_livro)
    elif opcao == '2':
        print("\n>>> Cadastro de estudantes ")
        nome_estudante = input("\n\tNome do estudante: ")
        email_estudante = input("\tE-mail do estudante: ")
        cadastrar_estudante(con, nome_estudante, email_estudante)
    elif opcao == '3':
        print("\n>>> Efetuar empréstimo ")
        est_id = int(input("\n\tCódigo do estudante: "))
        livros_emprestimo = input("\tCódigos dos livros a emprestar (separados por vírgula): ").split(',')
        livros_emprestimo = [int(livro_id) for livro_id in livros_emprestimo]
        efetuar_emprestimo(con, est_id, livros_emprestimo)
    elif opcao == '4':
        print("\n>>> Efetuar devolução ")
        livro_id = int(input("\n\tCódigo do livro a ser devolvido: "))
        efetuar_devolucao(con, livro_id)
    elif opcao == '5':
        print("\n>>> Listar empréstimos de estudante")
        est_id = int(input("\n\tCódigo do estudante para listar empréstimos: "))
        listar_emprestimos_estudante(con, est_id)
    elif opcao == '6':
        print("\n>>> Listagem dos estueantes devedores\n")
        listar_devedores(con)
    elif opcao == '7':
        listar_acervo(con)
    elif opcao == '8':
        print("\n>>> Listar empréstimos de um livro")
        livro_id = int(input("\n\tCódigo do livro para listar empréstimos: "))
        listar_emprestimos_livro(con, livro_id)
    elif opcao == '9':
        listar_estudantes(con)
    elif opcao == '10':
        listar_estudantes(con, "alf")
    elif opcao == '0':
        print("Saindo do programa...")
        break
    else:
        print("\tOpção inválida.\n\tEscolha outra opção do menu.")

con.close()