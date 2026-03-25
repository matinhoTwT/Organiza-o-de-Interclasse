from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "interclasse.db"

def conectar():
    return sqlite3.connect(DB)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT tipo FROM usuarios WHERE username=? AND senha=?",
        (data["username"], data["senha"])
    )

    res = cursor.fetchone()
    conn.close()

    if res:
        return jsonify({"msg": "ok", "tipo": res[0]})
    else:
        return jsonify({"erro": "login inválido"}), 401

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (?, ?)",
            (data["username"], data["senha"])
        )

        conn.commit()
        conn.close()

        return jsonify({"msg": "criado"})
    except:
        return jsonify({"erro": "usuário já existe"}), 400

# ---------------- CREATE TIME ----------------
@app.route("/times", methods=["POST"])
def criar_time():
    data = request.json

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO times (nome, turma, categoria, modalidade, usuario)
        VALUES (?, ?, ?, ?, ?)
        """, (
            data["nome"],
            data["turma"],
            data["categoria"],
            data["modalidade"],
            data.get("usuario")  # 🔥 AQUI
        ))

        conn.commit()
        conn.close()

        return jsonify({"msg": "Time criado"})

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro ao criar time"}), 400

# ---------------- LISTAR TIMES + ALUNOS ----------------
@app.route("/times", methods=["GET"])
def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM times")
    times = cursor.fetchall()

    resultado = []

    for t in times:
        cursor.execute("SELECT id, nome FROM alunos WHERE time_id=?", (t[0],))
        alunos = cursor.fetchall()

        resultado.append({
            "id": t[0],
            "nome": t[1],
            "turma": t[2],
            "categoria": t[3],
            "modalidade": t[4],
            "pontos": t[5],
            "alunos": [{"id": a[0], "nome": a[1]} for a in alunos]
        })

    conn.close()
    return jsonify(resultado)

# ---------------- ADD ALUNO ----------------
@app.route("/alunos", methods=["POST"])
def add_aluno():
    data = request.json

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alunos WHERE time_id=?", (data["time_id"],))
    total = cursor.fetchone()[0]

    if total >= 12:
        return jsonify({"erro": "limite atingido"}), 400

    cursor.execute(
        "INSERT INTO alunos (nome, time_id) VALUES (?, ?)",
        (data["nome"], data["time_id"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "aluno adicionado"})

# ---------------- DELETE ALUNO ----------------
@app.route("/alunos/<int:id>", methods=["DELETE"])
def del_aluno(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alunos WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"msg": "removido"})

# ---------------- DELETE TIME ----------------
@app.route("/times/<int:id>", methods=["DELETE"])
def del_time(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alunos WHERE time_id=?", (id,))
    cursor.execute("DELETE FROM times WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"msg": "deletado"})

# ---------------- EDIT TIME ----------------
@app.route("/times/<int:id>", methods=["PUT"])
def edit_time(id):
    data = request.json

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE times SET nome=? WHERE id=?",
        (data["nome"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "editado"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)