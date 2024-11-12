from urllib.parse import urlsplit

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from app import app, db
from app.forms import LoginForm, RegistrarNotasFiscaisForm, RegistrationForm
from app.models import DadosEmpenhos, DadosNfs, OrdenadorDespesas, User


@app.route("/")
@app.route("/index")
@login_required
def index():
    # user = {"username": "Miguel"}
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]
    return render_template("index.html", title="Home", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)

    # return redirect(url_for("index"))
    # flash(f'Login requested for user {form.username.data}. password={form.password.data}, remember_me={form.remember_me.data}')
    # return redirect(url_for('index'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register_user.html", title="Register", form=form)

@app.route("/registrar_nfs", methods=["GET", "POST"])
@login_required
def registrar_nfs():
    form = RegistrarNotasFiscaisForm()

    if form.validate_on_submit():
            
            # Converte Valor da NF para Float
            valor_nf = form.valor_nf.data 
            valor_nf = valor_nf.replace("R$", "").replace(",",".")
            valor_nf = float(valor_nf)

            nf = DadosNfs(
            processo_sei=form.processo_sei.data,
            doc_sei_nf=form.doc_sei_nf.data,
            doc_sei_ateste=form.doc_sei_ateste.data,
            doc_sei_conformidade=form.doc_sei_conformidade.data,
            numero_nf=form.numero_nf.data,
            data_emissao=form.data_emissao.data,
            data_entrada=form.data_entrada.data,
            data_vencimento=form.data_vencimento.data,
            data_inicio_competencia=form.data_inicio_competencia.data,
            data_fim_competencia=form.data_fim_competencia.data,
            masp=form.masp.data,
            # nome_ordenador=form.nome_ordenador.data,
            observacoes=form.observacoes.data,
            municipio=form.municipio.data,
            valor_nf=valor_nf,
            ue=form.ue.data,
            ano=form.ano.data,
            empenho=form.empenho.data,
            conformidade=form.conformidade.data,
            status=form.status.data,
            banco=form.banco.data,
            agencia=form.agencia.data,
            conta=form.conta.data
            )
            db.session.add(nf)
            db.session.commit()
            flash("Document successfully added!")
            return redirect(url_for("login"))
    
    return render_template("registrar_nfs.html", title="Registrar Notas Fiscais", form=form)

@app.route("/mostrar_nfs", methods=["GET"])
def mostrar_nfs():
    query = select(DadosNfs)
    dados_nfs = db.session.scalars(query).all()
    return render_template("mostrar_nfs.html", title="Mostrar Notas Fiscais", dados_nfs=dados_nfs)



@app.route("/get_ordenador_name", methods=["GET"])
def get_ordenador_name():
    masp = request.args.get("masp")  # Obtém o valor MASP passado na URL como parâmetro
    
    # Consulta o banco de dados buscando pelo MASP informado
    ordenador = db.session.scalar(select(OrdenadorDespesas).where(OrdenadorDespesas.masp == masp))

    if ordenador:  # Se o MASP existir, retorne o nome do funcionário
        return jsonify({"nome": ordenador.nome})  # Retorna uma resposta JSON com o nome
    else:  # Caso contrário, retorna um erro informando que o funcionário não foi encontrado
        return jsonify({"error": "Ordenador não encontrado"}), 404
    
@app.route("/get_emp_data", methods=["GET"])
def get_emp_data():
    ue = request.args.get("ue")  
    ano = request.args.get("ano") 
    empenho = request.args.get("empenho")  
    
    data_emp = db.session.scalar(select(DadosEmpenhos).where(DadosEmpenhos.ue == ue, DadosEmpenhos.ano == ano, DadosEmpenhos.empenho == empenho))

    if data_emp:  
        return jsonify({"gmi_fp": data_emp.gmi_fp, "nome_credor": data_emp.razao_social_credor, "cpnj_cpf_credor": data_emp.cnpj_cpf_credor}) 
    else:  
        return jsonify({"error": "Empenho não encontrado"}), 404


# from app import app


# @app.route("/")
# @app.route("/index")
# def index():
#     return "Hello, World!"

#next: fetch only when hits ok

# 6546546546546546565465465465

# 6672737

# 1090024	2022	1