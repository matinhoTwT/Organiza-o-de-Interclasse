const API = "http://127.0.0.1:5000";

// ---------------- LOGIN ----------------
function login() {
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    fetch(API + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: user,
            senha: pass
        })
    })
    .then(r => r.json())
    .then(res => {
        if(res.tipo){
            localStorage.setItem("tipo", res.tipo);
            localStorage.setItem("usuario", user); // 🔥 IMPORTANTE
            localStorage.setItem("logado", "true");

            if(res.tipo === "admin"){
                window.location.href = "admin.html";
            } else {
                window.location.href = "dashboard.html";
            }
        } else {
            alert("Login inválido");
        }
    });
}

// ---------------- LOGOUT ----------------
function logout(){
    localStorage.clear();
    window.location.href = "index.html";
}

// ---------------- CRIAR TIME ----------------
function criarTime() {
    const nome = document.getElementById("nome").value;
    const turma = document.getElementById("turma").value;
    const categoria = document.getElementById("categoria").value;
    const modalidade = document.getElementById("modalidade").value;

    const usuario = localStorage.getItem("usuario");

    if(!nome){
        alert("Digite o nome do time!");
        return;
    }

    fetch(API + "/times")
    .then(r => r.json())
    .then(times => {

        // 🔒 BLOQUEIA 1 TIME POR USUÁRIO
        const jaTem = times.find(t => t.usuario === usuario);

        if(jaTem){
            alert("Você já criou um time!");
            return;
        }

        fetch(API + "/times", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nome,
                turma,
                categoria,
                modalidade,
                usuario // 🔥 salva dono do time
            })
        })
        .then(() => {
            alert("Time criado!");
            carregarTimes();
        });

    });
}

// ---------------- ADD ALUNO ----------------
function addAluno(id){
    const input = document.getElementById("a-"+id) || document.getElementById("adm-a-"+id);

    if(!input){
        alert("Erro no input");
        return;
    }

    const nome = input.value;

    if(!nome){
        alert("Digite o nome do aluno");
        return;
    }

    fetch(API + "/alunos", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome,
            time_id: id
        })
    })
    .then(r => r.json())
    .then(res => {
        if(res.erro){
            alert(res.erro);
        } else {
            input.value = "";
            carregarTimes();
            carregarAdmin();
        }
    });
}

// ---------------- REMOVE ALUNO ----------------
function delAluno(id){
    fetch(API + "/alunos/" + id, {
        method: "DELETE"
    })
    .then(() => {
        carregarTimes();
        carregarAdmin();
    });
}

// ---------------- LISTAR DASHBOARD ----------------
function carregarTimes() {
    fetch(API + "/times")
    .then(r => r.json())
    .then(data => {
        const lista = document.getElementById("lista");
        if (!lista) return;

        lista.innerHTML = "";

        data.forEach(t => {
            lista.innerHTML += `
                <div class="item">
                    <b>${t.nome}</b><br>
                    ${t.turma} - ${t.modalidade}<br>

                    <input placeholder="Aluno" id="a-${t.id}">
                    <button onclick="addAluno(${t.id})">+</button>

                    <div>
                        ${t.alunos.map(a => a.nome).join("<br>")}
                    </div>
                </div>
            `;
        });
    });
}

// ---------------- ADMIN ----------------
function carregarAdmin() {
    fetch(API + "/times")
    .then(r => r.json())
    .then(data => {
        const div = document.getElementById("listaAdmin");
        if (!div) return;

        div.innerHTML = "";

        if(data.length === 0){
            div.innerHTML = "<p>Nenhum time cadastrado</p>";
            return;
        }

        data.forEach(t => {
            div.innerHTML += `
                <div class="item">

                    <input id="nome-${t.id}" value="${t.nome}">

                    <button onclick="editar(${t.id})">Salvar</button>
                    <button onclick="excluir(${t.id})">Excluir</button>

                    <hr>

                    <input placeholder="Novo aluno" id="adm-a-${t.id}">
                    <button onclick="addAluno(${t.id})">Adicionar</button>

                    <div>
                        ${t.alunos.map(a => `
                            ${a.nome}
                            <button onclick="delAluno(${a.id})">x</button>
                        `).join("<br>")}
                    </div>

                </div>
            `;
        });
    });
}

// ---------------- EDITAR ----------------
function editar(id){
    const nome = document.getElementById("nome-"+id).value;

    fetch(API + "/times/" + id, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ nome })
    })
    .then(() => carregarAdmin());
}

// ---------------- EXCLUIR ----------------
function excluir(id){
    fetch(API + "/times/" + id, {
        method: "DELETE"
    })
    .then(() => carregarAdmin());
}

// ---------------- INIT ----------------
window.onload = () => {
    carregarTimes();
    carregarAdmin();
};