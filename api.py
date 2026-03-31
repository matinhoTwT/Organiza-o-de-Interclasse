# ===================== IMPORTS =====================
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB = "interclasse.db"

def conectar():
    return sqlite3.connect(DB)


# ===================== ROOT =====================

@app.route("/")
def home():
    return "API OK"


# ===================== AUTH =====================

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (?, ?)",
            (data["username"], data["senha"])
        )
        conn.commit()
    except:
        conn.close()
        return jsonify({"erro": "Usuário já existe"}), 400

    conn.close()
    return jsonify({"msg": "ok"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT tipo FROM usuarios WHERE username=? AND senha=?",
        (data["username"], data["senha"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"msg": "ok", "tipo": str(user[0]).lower()})

    return jsonify({"erro": "Login inválido"}), 401


# ===================== TIMES =====================

@app.route("/times", methods=["POST"])
def criar_time():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    usuario = (data.get("usuario") or "").strip().lower()

    cursor.execute("SELECT * FROM times WHERE usuario=?", (usuario,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Você já criou um time"}), 400

    cursor.execute("""
        INSERT INTO times (nome, turma, categoria, modalidade, usuario)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["nome"],
        data["turma"],
        data["categoria"],
        data["modalidade"],
        usuario
    ))

    conn.commit()
    conn.close()

    return jsonify({"msg": "ok"})


@app.route("/times", methods=["GET"])
def listar_times():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM times")
    dados = cursor.fetchall()

    conn.close()

    return jsonify([
        {
            "id": t[0],
            "nome": t[1],
            "turma": t[2],
            "categoria": t[3],
            "modalidade": t[4],
            "usuario": t[5],
            "pontos": t[6]
        }
        for t in dados
    ])


@app.route("/times/<int:id>", methods=["PUT"])
def editar_time(id):
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT usuario FROM times WHERE id=?", (id,))
    dono = cursor.fetchone()

    if not dono:
        conn.close()
        return jsonify({"erro": "Time não encontrado"}), 404

    usuario = (data.get("usuario") or "").strip().lower()
    tipo = (data.get("tipo") or "").strip().lower()
    dono_db = (dono[0] or "").strip().lower()

    if tipo != "admin" and usuario != dono_db:
        conn.close()
        return jsonify({"erro": "Sem permissão"}), 403

    cursor.execute("UPDATE times SET nome=? WHERE id=?", (data["nome"], id))

    conn.commit()
    conn.close()

    return jsonify({"msg": "ok"})


@app.route("/times/<int:id>", methods=["DELETE"])
def excluir_time(id):
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT usuario FROM times WHERE id=?", (id,))
    dono = cursor.fetchone()

    if not dono:
        conn.close()
        return jsonify({"erro": "Time não encontrado"}), 404

    usuario = (data.get("usuario") or "").strip().lower()
    tipo = (data.get("tipo") or "").strip().lower()
    dono_db = (dono[0] or "").strip().lower()

    if tipo != "admin" and usuario != dono_db:
        conn.close()
        return jsonify({"erro": "Sem permissão"}), 403

    cursor.execute("DELETE FROM alunos WHERE time_id=?", (id,))
    cursor.execute("DELETE FROM times WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"msg": "ok"})


# ===================== ALUNOS =====================

@app.route("/alunos", methods=["POST"])
def add_aluno():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT usuario FROM times WHERE id=?", (data["time_id"],))
    dono = cursor.fetchone()

    if not dono:
        conn.close()
        return jsonify({"erro": "Time não encontrado"}), 404

    usuario = (data.get("usuario") or "").strip().lower()
    tipo = (data.get("tipo") or "").strip().lower()
    dono_db = (dono[0] or "").strip().lower()

    if tipo != "admin" and usuario != dono_db:
        conn.close()
        return jsonify({"erro": "Sem permissão"}), 403

    cursor.execute("SELECT COUNT(*) FROM alunos WHERE time_id=?", (data["time_id"],))
    if cursor.fetchone()[0] >= 12:
        conn.close()
        return jsonify({"erro": "Limite atingido"}), 400

    cursor.execute(
        "INSERT INTO alunos (nome, time_id) VALUES (?, ?)",
        (data["nome"], data["time_id"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "ok"})


@app.route("/alunos/<int:time_id>", methods=["GET"])
def listar_alunos(time_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE time_id=?", (time_id,))
    dados = cursor.fetchall()

    conn.close()

    return jsonify([
        {"id": a[0], "nome": a[1]}
        for a in dados
    ])


@app.route("/alunos/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    usuario = request.args.get("usuario")
    tipo = request.args.get("tipo")

    conn = conectar()
    cursor = conn.cursor()

    # pega o dono do time do aluno
    cursor.execute("""
        SELECT t.usuario FROM alunos a
        JOIN times t ON a.time_id = t.id
        WHERE a.id=?
    """, (id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"erro":"Aluno não encontrado"}), 404

    dono = result[0]

    # 🔥 REGRA FINAL
    if tipo != "admin" and dono != usuario:
        conn.close()
        return jsonify({"erro":"Sem permissão"}), 403

    cursor.execute("DELETE FROM alunos WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"msg":"Aluno removido"})

# ===================== RUN =====================

if __name__ == "__main__":
    app.run(debug=True)     