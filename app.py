import streamlit as st
import requests

API = "http://127.0.0.1:5000"

# ---------------- ESTADO ----------------
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

# ---------------- FUNÇÕES SEGURAS ----------------
def safe_post(url, data):
    try:
        return requests.post(url, json=data)
    except:
        st.error("API não está rodando 😢")
        return None

def safe_get(url):
    try:
        return requests.get(url)
    except:
        st.error("API não está rodando 😢")
        return None

# ---------------- LOGIN ----------------
def tela_login():
    st.title("🏫 Interclasse")

    opcao = st.radio("Escolha", ["Login", "Registrar"])

    if opcao == "Registrar":
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar conta"):
            r = safe_post(f"{API}/register", {
                "username": user,
                "senha": senha
            })

            if r and r.status_code == 200:
                st.success("Conta criada!")
            elif r:
                st.error(r.json().get("erro"))

    else:
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            r = safe_post(f"{API}/login", {
                "username": user,
                "senha": senha
            })

            if r and r.status_code == 200:
                st.session_state["pagina"] = "usuario"
                st.rerun()
            else:
                st.error("Login inválido")

    if st.button("Admin"):
        st.session_state["pagina"] = "admin"

# ---------------- AREA USUARIO ----------------
def area_usuario():
    st.title("👤 Área do Usuário")

    nome = st.text_input("Nome do Time")

    turma = st.selectbox("Turma", [
        "1º ano A","1º ano B","1º ano C",
        "2º ano A","2º ano B","2º ano C",
        "3º ano A","3º ano B","3º ano C"
    ])

    categoria = st.selectbox("Categoria", ["Masculino", "Feminino"])
    modalidade = st.selectbox("Modalidade", ["Futebol", "Vôlei", "Basquete"])

    if st.button("Criar Time"):
        if not nome:
            st.warning("Digite um nome")
            return

        r = safe_post(f"{API}/times", {
            "nome": nome.strip(),
            "turma": turma,
            "categoria": categoria,
            "modalidade": modalidade
        })

        if r and r.status_code == 200:
            st.success("Time criado!")
            st.rerun()
        elif r:
            st.error(r.json().get("erro"))

# ---------------- ADMIN ----------------
def area_admin():
    st.title("👨‍💼 Admin")

    user = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if user == "admin" and senha == "admin":

        r = safe_get(f"{API}/times")

        if not r:
            return

        times = r.json()

        for t in times:
            with st.expander(f"{t['nome']} ({t['modalidade']})"):

                novo_nome = st.text_input("Nome", t["nome"], key=f"n{t['id']}")

                if st.button("Salvar", key=f"s{t['id']}"):
                    requests.put(f"{API}/times/{t['id']}", json={
                        "nome": novo_nome,
                        "turma": t["turma"],
                        "categoria": t["categoria"],
                        "modalidade": t["modalidade"],
                        "pontos": t["pontos"]
                    })
                    st.rerun()

                alunos = requests.get(f"{API}/alunos/{t['id']}").json()

                for a in alunos:
                    col1, col2 = st.columns([3,1])
                    col1.write(a["nome"])

                    if col2.button("❌", key=f"d{a['id']}"):
                        requests.delete(f"{API}/alunos/{a['id']}")
                        st.rerun()

# ---------------- CONTROLE ----------------
if st.session_state["pagina"] == "login":
    tela_login()

elif st.session_state["pagina"] == "usuario":
    area_usuario()

elif st.session_state["pagina"] == "admin":
    area_admin()