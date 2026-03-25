import sqlite3
import flask 

conn = sqlite3.connect('interclasse.db')
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grupos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    turma TEXT NOT NULL,
    modalidade TEXT NOT NULL
)
""")

# Criar admin
cursor.execute("INSERT INTO usuarios (username, password) VALUES ('admin', '1234')")

conn.commit()
conn.close()

print("Banco criado com sucesso!")