from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo'

def conectar():
    return sqlite3.connect('interclasse.db')

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        senha = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (user, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['logado'] = True
            return redirect('/admin')
        else:
            return "Login inválido"

    return render_template('login.html')

# PAINEL ADMIN
@app.route('/admin')
def admin():
    if 'logado' not in session:
        return redirect('/login')

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grupos")
    grupos = cursor.fetchall()
    conn.close()

    return render_template('admin.html', grupos=grupos)

# CREATE
@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    turma = request.form['turma']
    modalidade = request.form['modalidade']

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO grupos (nome, turma, modalidade) VALUES (?, ?, ?)",
                   (nome, turma, modalidade))
    conn.commit()
    conn.close()

    return redirect('/admin')

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grupos WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/admin')

# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nome = request.form['nome']

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE grupos SET nome=? WHERE id=?", (nome, id))
    conn.commit()
    conn.close()

    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)