.open --new bib.db
  
CREATE TABLE estudantes (
  estID INTEGER PRIMARY KEY,
  estNome TEXT NOT NULL,
  estEmail TEXT NOT NULL);

INSERT INTO estudantes (estNome, estEmail) VALUES('Fulano de Tal','fulano@tal.com');
INSERT INTO estudantes (estNome, estEmail) VALUES('Xanderson de Tal','xandao@hotmail.com');
INSERT INTO estudantes (estNome, estEmail) VALUES('Beltrana de Tal','beltrana@msn.com');
INSERT INTO estudantes (estNome, estEmail) VALUES('Felizberto de Tal','feliz@gmail.com');
INSERT INTO estudantes (estNome, estEmail) VALUES('Cicrana de Tal','cicrana@tal.com.br');
INSERT INTO estudantes (estNome, estEmail) VALUES('Hedimberto de Tal','hed@empresa.com');
INSERT INTO estudantes (estNome, estEmail) VALUES('Cicrano de Tal','ciclano@hotmail.com.br');

CREATE TABLE livros(
livroID integer primary key,
livroNome text not null);

INSERT INTO livros (livroNome) VALUES('Lógica de Programação');
INSERT INTO livros (livroNome) VALUES('Cálculo');
INSERT INTO livros (livroNome) VALUES('Álgebra Linear');
INSERT INTO livros (livroNome) VALUES('Python para Engenheiros');
INSERT INTO livros (livroNome) VALUES('Geometria Analitica');
INSERT INTO livros (livroNome) VALUES('Fundamentos de Java');
INSERT INTO livros (livroNome) VALUES('C Completo e Total');
INSERT INTO livros (livroNome) VALUES('Métodos Numéricos');
INSERT INTO livros (livroNome) VALUES('Banco de Dados');
INSERT INTO livros (livroNome) VALUES('Engenharia de Software');
INSERT INTO livros (livroNome) VALUES('Circuitos Elétricos');
INSERT INTO livros (livroNome) VALUES('Instalções Prediais');
INSERT INTO livros (livroNome) VALUES('Mecânica');
INSERT INTO livros (livroNome) VALUES('Eletromagnetismo');
INSERT INTO livros (livroNome) VALUES('Sistemas Operacionais');

CREATE TABLE emprestimos (
  empID INTEGER PRIMARY KEY,
  estID INTEGER REFERENCES estudantes(estId),
  empData DATE NOT NULL);

INSERT INTO emprestimos (estId, empData) 
VALUES(1,'2024-03-11');
INSERT INTO emprestimos (estId, empData) 
VALUES(3,'2024-03-14');
INSERT INTO emprestimos (estId, empData) 
VALUES(6,'2024-03-15');
INSERT INTO emprestimos (estId, empData) 
VALUES(4,'2024-03-19');
INSERT INTO emprestimos (estId, empData) 
VALUES(2,'2024-03-20');

CREATE TABLE livroEmprestado (
  empID INTEGER REFERENCES emprestimos(empId),
  livroID INTEGER REFERENCES livros(livroID),
  empDataDev DATE DEFAULT NULL);

INSERT INTO livroEmprestado (empID, livroId) VALUES(1, 2);
INSERT INTO livroEmprestado (empID, livroId) VALUES(1, 3);
INSERT INTO livroEmprestado (empID, livroId) VALUES(2, 6);
INSERT INTO livroEmprestado (empID, livroId) VALUES(3, 4);
INSERT INTO livroEmprestado (empID, livroId) VALUES(4, 7);
INSERT INTO livroEmprestado (empID, livroId) VALUES(4, 9);
INSERT INTO livroEmprestado (empID, livroId) VALUES(4, 1);
INSERT INTO livroEmprestado (empID, livroId) VALUES(5, 5);