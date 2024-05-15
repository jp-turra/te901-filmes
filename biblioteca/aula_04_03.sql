
-- usando queries aninhadas
-- um select usando um where resultado de outro select

-- livros nunca emprestados
SELECT * FROM livros WHERE livroID NOT IN (
SELECT livroID FROM livroEmprestado);

-- livros já emprestados alguma vez
SELECT * FROM livros WHERE livroID IN (
SELECT livroID FROM livroEmprestado);

-- se fosse com INNER JOIN
SELECT * FROM  livros
INNER JOIN livroEmprestado le
USING  (livroID)
WHERE le.empDataDev IS NULL
ORDER BY livroNome;

-- nome dos livros emprestados pelo estudante de id 3
SELECT livroNome FROM livros WHERE livroID IN (
SELECT livroID FROM livroEmprestado WHERE empID IN(
SELECT empID FROM emprestimos WHERE estID = 3));

-- todos os empréstimos com JOIN
SELECT est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le  USING (empID))
INNER JOIN livros l USING (livroID));

-- todos os empréstimos NAO devolvidos com JOIN
SELECT est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le  USING (empID))
INNER JOIN livros l USING (livroID))
WHERE le.empDataDev IS NULL;

-- criando uma VIEW para a consulta de empréstimos não devolvido
-- devedores se comporta agora como uma tabela virtual contexto as colunas resultantes da query
-- servem  para encapsular joins complexos e criar uma camada de abstração
-- pode-se alterar as colunas de uma view sem alterar as tabelas reais\
-- são apenas para facilitar leitura
CREATE VIEW devedores
AS 
SELECT est.estID, est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le  USING (empID))
INNER JOIN livros l USING (livroID))
WHERE le.empDataDev IS NULL
ORDER BY estNome, l.livroNome;

-- view para todos os empréstimos já devolvidos
CREATE VIEW encerrados
AS 
SELECT est.estID, est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le  USING (empID))
INNER JOIN livros l USING (livroID))
WHERE le.empDataDev IS NOT NULL
ORDER BY estNome, l.livroNome;

-- select geral usando a view devedores
SELECT * from devedores;

-- select geral usando a view encerrados
SELECT * from encerrados;

-- devolvendo o livro 9 do emprestimo 4
-- para testar a view devedores e a view encerrados 
UPDATE livroEmprestado 
SET empDataDev = date('now', 'localtime') 
WHERE empID = 4 and livroID = 9;




