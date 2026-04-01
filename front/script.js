const API = "http://127.0.0.1:5000";


// LOGIN
function login(){
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    fetch(API+"/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({username:user,senha:pass})
    })
    .then(r=>r.json())
    .then(res=>{
        if(res.msg){
            localStorage.setItem("usuario",user);
            localStorage.setItem("tipo",res.tipo);

            if(res.tipo==="admin"){
                window.location="admin.html";
            }else{
                window.location="dashboard.html";
            }
        }else{
            alert(res.erro);
        }
    });
}


// REGISTER
function register(){
    const user = document.getElementById("newUser").value;
    const pass = document.getElementById("newPass").value;

    fetch(API+"/register",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({username:user,senha:pass})
    })
    .then(r=>r.json())
    .then(res=>{
        if(res.msg){
            alert("Conta criada");
        }else{
            alert(res.erro);
        }
    });
}


// LOGOUT
function logout(){
    localStorage.clear();
    window.location="index.html";
}


// TIMES
function criarTime(){
    const nome = document.getElementById("nome").value;
    const turma = document.getElementById("turma").value;
    const categoria = document.getElementById("categoria").value;
    const modalidade = document.getElementById("modalidade").value;
    const usuario = localStorage.getItem("usuario");

    fetch(API+"/times",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({nome,turma,categoria,modalidade,usuario})
    })
    .then(r=>r.json())
    .then(res=>{
        if(res.msg){
            carregarTimes();
        }else{
            alert(res.erro);
        }
    })
    .catch(()=>{
        alert("Erro ao criar time");
    });
}


function carregarTimes(){
    fetch(API+"/times")
    .then(r=>r.json())
    .then(data=>{
        const div = document.getElementById("times");
        if(!div) return;

        div.innerHTML="";

        data.forEach(t=>{
            div.innerHTML+=`
            <div>
                <b>${t.nome}</b><br>
                ${t.turma} - ${t.modalidade}
                <input id="a-${t.id}">
                <button onclick="addAluno(${t.id})">+</button>
                <div id="alunos-${t.id}"></div>
            </div>
            `;

            fetch(API+"/alunos/"+t.id)
            .then(r=>r.json())
            .then(alunos=>{
                document.getElementById("alunos-"+t.id).innerHTML=
                alunos.map(a=>a.nome).join("<br>");
            });
        });
    });
}


// ALUNOS
function addAluno(id){
    const input = document.getElementById("a-"+id) || document.getElementById("adm-"+id);

    if(!input){
        alert("input não encontrado");
        return;
    }

    const nome = input.value.trim();

    if(nome === ""){
        alert("Digite um nome");
        return;
    }

    const usuario = localStorage.getItem("usuario");
    const tipo = localStorage.getItem("tipo");

    console.log("USUARIO:", usuario);
    console.log("TIPO:", tipo);

    fetch(API + "/alunos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            time_id: id,
            usuario: usuario,
            tipo: tipo
        })
    })
    .then(r => r.json())
    .then(res => {
        if(res.erro){
            alert(res.erro);
        }else{
            carregarTimes();
        }
    })
    .catch(() => {
        alert("Erro ao adicionar aluno");
    });
}


function delAluno(id){
    const usuario = localStorage.getItem("usuario");
    const tipo = localStorage.getItem("tipo");

    fetch(API + "/alunos/" + id + "?usuario=" + usuario + "&tipo=" + tipo, {
        method: "DELETE"
    })
    .then(r => r.json())
    .then(res => {
        if(res.erro){
            alert(res.erro);
        }else{
            carregarAdmin();
        }
    });
}

// ADMIN LOGIN
function loginAdmin(){
    const user = prompt("login");
    const pass = prompt("senha");

    if(user==="admin" && pass==="1234"){
        localStorage.setItem("tipo","admin");
        window.location="admin.html";
    }else{
        alert("Acesso negado");
    }
}


// ADMIN PANEL
function carregarAdmin(){
    fetch(API+"/times")
    .then(r=>r.json())
    .then(data=>{
        const div = document.getElementById("listaAdmin");
        if(!div) return;

        div.innerHTML="";

        data.forEach(t=>{
            div.innerHTML+=`
            <div>
                <input id="n-${t.id}" value="${t.nome}">
                <button onclick="editar(${t.id})">Salvar</button>
                <button onclick="excluir(${t.id})">Excluir</button>

                <input id="adm-${t.id}">
                <button onclick="addAluno(${t.id})">+</button>

                <div id="adm-alunos-${t.id}"></div>
            </div>
            `;

            fetch(API+"/alunos/"+t.id)
            .then(r=>r.json())
            .then(alunos=>{
                document.getElementById("adm-alunos-"+t.id).innerHTML=
                alunos.map(a=>`${a.nome} <button onclick="delAluno(${a.id})">x</button>`).join("<br>");
            });
        });
    });
}


function editar(id){
    const nome = document.getElementById("n-"+id).value;

    fetch(API+"/times/"+id,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            nome:nome,
            usuario:localStorage.getItem("usuario"),
            tipo:localStorage.getItem("tipo")
        })
    })
    .then(r=>r.json())
    .then(res=>{
        if(res.erro){
            alert(res.erro);
        }else{
            carregarAdmin();
        }
    });
}

function excluir(id){
    fetch(API+"/times/"+id,{
        method:"DELETE",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            usuario:localStorage.getItem("usuario"),
            tipo:localStorage.getItem("tipo")
        })
    })
    .then(r=>r.json())
    .then(res=>{
        if(res.erro){
            alert(res.erro);
        }else{
            carregarAdmin();
        }
    });
}

function removerAluno(id){
    const usuario = localStorage.getItem("usuario");
    const tipo = localStorage.getItem("tipo");

    fetch(API + "/alunos/" + id + "?usuario=" + usuario + "&tipo=" + tipo, {
        method: "DELETE"
    })
    .then(r => r.json())
    .then(res => {
        if(res.erro){
            alert(res.erro);
        }else{
            carregarAdmin();
        }
    })
    .catch(() => {
        alert("Erro ao remover aluno");
    });
}


// INIT
window.onload = ()=>{
    carregarTimes();
    carregarAdmin();
};