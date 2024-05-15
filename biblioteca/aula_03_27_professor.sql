-- Queries úteis para teste da Biblioteca e uso de INNER JOIN
------------------------------------------------------------

-- select com condições diferentes

SELECT * FROM livros;

SELECT * FROM livros ORDER BY livroNome;

SELECT * FROM livros ORDER BY livroNome DESC;

SELECT * FROM livros LIMIT 5;

SELECT * FROM livros LIMIT 5 OFFSET 5;

SELECT * FROM livros WHERE livroNome LIKE 'Eng%';

SELECT * FROM livros WHERE livroNome LIKE '%Eng%';

SELECT COUNT(*) FROM estudantes;
SELECT COUNT(*) FROM emprestimos;
SELECT COUNT(DISTINCT empID) FROM livroEmprestado;

-- devolvendo um livro

UPDATE livroEmprestado 
SET empDataDev = '2024-03-25' WHERE livroId=3;

UPDATE livroEmprestado 
SET empDataDev = date('now', 'localtime') WHERE livroId=2;

-- DUAS tabelas usando where

-- livros que já foram ou estão emprestados
SELECT livros.livroID, livroNome
FROM  livros, livroEmprestado
WHERE livroEmprestado.livroID = livros.livroId;

-- livros que estão emprestados neste momento
SELECT livros.livroID, livroNome
FROM  livros, livroEmprestado
WHERE livroEmprestado.livroID = livros.livroId 
AND livroEmprestado.empDataDev IS NULL;

-- livros que já foram emprestados e devolvidos
SELECT livros.livroID, livroNome
FROM  livros, livroEmprestado
WHERE livroEmprestado.livroID = livros.livroId 
AND livroEmprestado.empDataDev IS NOT NULL;

-- emprestados com nome de quem emprestou
SELECT livros.livroID, livroNome, estNome
FROM  livros, livroEmprestado, estudantes, emprestimos
WHERE livroEmprestado.livroID = livros.livroId 
AND livroEmprestado.empID = emprestimos.empID
AND estudantes.estID = emprestimos.estID
AND livroEmprestado.empDataDev IS NULL;

-- idem mas ordenado por estudante e por livro
SELECT livros.livroID, livroNome, estNome
FROM  livros, livroEmprestado, estudantes, emprestimos
WHERE livroEmprestado.livroID = livros.livroId 
AND livroEmprestado.empID = emprestimos.empID
AND estudantes.estID = emprestimos.estID
AND livroEmprestado.empDataDev IS NULL
ORDER BY estNome, livroNome;

-- Duas ou mais tabelas usando INNER JOIN
----------------------------------------

-- mais infos sobre JOIN, conforme discutido em sala em:
-- https://www.w3schools.com/sql/sql_join.asp
-- https://www.tutorialspoint.com/sqlite/sqlite_using_joins.htm

-- equivalente ao select acima, porém usando INNER JOIN (opção preferencial em relação à query anterior)
SELECT livros.livroID, livroNome
FROM  livros
INNER JOIN livroEmprestado 
ON livroEmprestado.livroID = livros.livroID;

-- o mesmo usando alias para facilitar referencia as tabelas
SELECT l.livroID, l.livroNome
FROM  livros l
INNER JOIN livroEmprestado le
ON le.livroID = l.livroID;

-- o mesmo usando USING, viável apenas quando as chaves PK e FK tiverem o mesmo identificador
SELECT livros.livroID, livroNome
FROM  livros
INNER JOIN livroEmprestado 
USING  (livroID);

-- adicionando uma ordenação ascendente (pode colocar ASC também)
SELECT livros.livroID, livroNome
FROM  livros
INNER JOIN livroEmprestado 
USING  (livroID)
ORDER BY livroNome;

-- recuperando apenas os livros ainda emprestados, portanto como devolução = NULL
SELECT *
FROM  livros
INNER JOIN livroEmprestado le
USING  (livroID)
WHERE le.empDataDev IS NULL
ORDER BY livroNome;

-- descobrindo os estudantes com emprestimo efetuado
SELECT est.estNome, emp.empID
FROM  estudantes est
INNER JOIN emprestimos emp
USING  (estID);

-- adicionalmente, descobrindo que livros emprestou
-- usando um INNER JOIN encadeado, atenção aos parênteses
SELECT est.estNome, emp.empID, le.livroID
FROM  ((estudantes est 
INNER JOIN emprestimos emp ON est.estID = emp.estID)
INNER JOIN livroEmprestado le ON emp.empID = le.empID);

-- o mesmo com USING
SELECT est.estNome, emp.empID, le.livroID
FROM  ((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID));

COM AS 4 TABELAS
----------------

-- incluindo agora qual o título do livro
SELECT est.estNome, emp.empID, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp ON est.estID = emp.estID)
INNER JOIN livroEmprestado le ON emp.empID = le.empID)
INNER JOIN livros l ON le.livroID = l.livroID);

-- o mesmo com USING
SELECT est.estNome, emp.empID, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID))
INNER JOIN livros l USING (livroID));

-- removendo do resultado os livros já devolvidos
SELECT est.estNome, emp.empID, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID))
INNER JOIN livros l USING (livroID))
WHERE le.empDataDev IS NULL;

-- incluindo a ordenação
SELECT est.estNome, emp.empID, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID))
INNER JOIN livros l USING (livroID))
WHERE le.empDataDev IS NULL
ORDER BY estNome, livroNome;

-- todos emprestimos do estudante 4
SELECT est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID))
INNER JOIN livros l USING (livroID))
WHERE est.estID = 4
ORDER BY livroNome;

-- devolvendo o livro 7
UPDATE livroEmprestado 
SET empDataDev = date('now', 'localtime') WHERE livroId=7;

-- livros emprestados e não devolvidos pelo estudante de código 4
SELECT est.estNome, emp.empID, emp.empData, le.empDataDev, le.livroID, l.livroNome
FROM  (((estudantes est 
INNER JOIN emprestimos emp USING (estID))
INNER JOIN livroEmprestado le USING (empID))
INNER JOIN livros l USING (livroID))
WHERE est.estID = 4  AND le.empDataDev IS NULL
ORDER BY livroNome;