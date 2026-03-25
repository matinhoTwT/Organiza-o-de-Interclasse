DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS times;
DROP TABLE IF EXISTS alunos;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    senha TEXT,
    tipo TEXT DEFAULT 'user'
);

CREATE TABLE times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    turma TEXT,
    categoria TEXT,
    modalidade TEXT,
    pontos INTEGER DEFAULT 0
);

CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    time_id INTEGER,
    FOREIGN KEY (time_id) REFERENCES times(id)
);

INSERT INTO usuarios (username, senha, tipo)
VALUES ('admin', '1234', 'admin');