import sqlite3

conn = sqlite3.connect("interclasse.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS usuarios")
cursor.execute("DROP TABLE IF EXISTS times")
cursor.execute("DROP TABLE IF EXISTS alunos")

cursor.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    senha TEXT,
    tipo TEXT DEFAULT 'user'
)
""")

cursor.execute("""
CREATE TABLE times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    turma TEXT,
    categoria TEXT,
    modalidade TEXT,
    usuario TEXT,
    pontos INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    time_id INTEGER
)
""")

cursor.execute("""
INSERT INTO usuarios (username, senha, tipo)
VALUES ('admin', '1234', 'admin')
""")

conn.commit()
conn.close()

print("BANCO OK")