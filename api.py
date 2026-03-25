from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "interclasse.db"

# ---------------- CRIAR BANCO NA MÃO ----------------
def criar_banco():
    print("🔥 Criando banco...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS times (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        turma TEXT,
        categoria TEXT,
        modalidade TEXT,
        pontos INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        time_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Banco criado com sucesso!")

# 🔥 FORÇA CRIAÇÃO
criar_banco()

# ---------------- CONEXÃO ----------------
def get_db():
    return sqlite3.connect(DB_NAME)

# ---------------- ROOT ----------------
@app.route("/")
def home():
    return "API OK 🚀"

# ---------------- CREATE TIME ----------------
@app.route("/times", methods=["POST"])
def criar_time():
    try:
        data = request.json
        print("Recebido:", data)

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO times (nome, turma, categoria, modalidade)
        VALUES (?, ?, ?, ?)
        """, (
            data.get("nome"),
            data.get("turma"),
            data.get("categoria"),
            data.get("modalidade")
        ))

        conn.commit()
        conn.close()

        return jsonify({"msg": "Time criado"})

    except sqlite3.IntegrityError:
        return jsonify({"erro": "Já existe um time com esse nome!"}), 400

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": str(e)}), 500

# ---------------- LISTAR TIMES ----------------
@app.route("/times", methods=["GET"])
def listar_times():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM times")
    dados = cursor.fetchall()

    conn.close()

    lista = []
    for t in dados:
        lista.append({
            "id": t[0],
            "nome": t[1],
            "turma": t[2],
            "categoria": t[3],
            "modalidade": t[4],
            "pontos": t[5]
        })

    return jsonify(lista)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)