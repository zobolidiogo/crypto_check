import os

from helpers import db_query, index_crypto_func, apology, crypto_history_format_day, login_required, usd, brl, val_nome, val_senha
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["brl"] = brl

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL(os.getenv("DATABASE_URL"))
# db.execute("PRAGMA foreign_keys = ON")

cryptos = ["bitcoin", "tether", "ethereum", "solana", "cardano", "xrp", "dogecoin"]

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():

    if session.get("id_usuario"):
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")

    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    confirmacao = request.form.get("confirmacao")

    if not usuario:
        return render_template("register.html", mensagem="digite um nome de usuário", usuario=usuario)
    
    if not senha:
        return render_template("register.html", mensagem="digite uma senha", usuario=usuario)
    
    erro_senha = val_senha(senha)
    if erro_senha:
        return render_template("register.html", mensagem=erro_senha, usuario=usuario)

    erro_usuario = val_nome(usuario)
    if erro_usuario:
        return render_template("register.html", mensagem=erro_usuario, usuario=usuario)

    if confirmacao != senha:
        return render_template("register.html", mensagem="as senhas não conferem", usuario=usuario)

    rows = db_query(db, "select nm_usuario from T_USUARIO where nm_usuario = ?", usuario)
    if rows is None:
        return render_template("register.html", mensagem="erro ao acessar o banco de dados", usuario=usuario)
    
    if len(rows):
        return render_template("register.html", mensagem="o usuário já existe", usuario=usuario)
    
    hash = generate_password_hash(senha)

    try:
        db.execute("insert into T_USUARIO (nm_usuario, cd_hash) values (?, ?)", usuario, hash)
    except Exception as e:
        return render_template("register.html", mensagem="erro ao cadastrar usuário", usuario=usuario)
    
    rows = db_query(db, "select id_usuario, nm_usuario from T_USUARIO where nm_usuario = ?", usuario)
    if rows is None:
        return render_template("register.html", mensagem="erro ao acessar o banco de dados", usuario=usuario)

    session["id_usuario"] = rows[0]["id_usuario"]
    session["nm_usuario"] = rows[0]["nm_usuario"]

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("id_usuario"):
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")
    
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if not usuario:
        return render_template("login.html", mensagem="favor prover um usuário", usuario=usuario)
    
    if not senha:
        return render_template("login.html", mensagem="favor prover uma senha", usuario=usuario)
    
    rows = db_query(db, "select id_usuario, nm_usuario, cd_hash from T_USUARIO where nm_usuario = ?", usuario)
    if rows is None:
        return render_template("login.html", mensagem="erro ao acessar o banco de dados", usuario=usuario)

    if len(rows) != 1 or not check_password_hash(rows[0]["cd_hash"], senha):
        return render_template("login.html", mensagem="usuário e/ou senha inválido(s)", usuario=usuario)
    
    session["id_usuario"] = rows[0]["id_usuario"]
    session["nm_usuario"] = rows[0]["nm_usuario"]

    return redirect("/")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/")
@login_required
def index():

    rows = db_query(db, """
        select nm_crypto, sum(qt_crypto) as qt_compras
        from T_TRANSACAO
        where id_usuario = ?
        group by nm_crypto
        having sum(qt_crypto) > 0
    """, session["id_usuario"])

    if rows is None:
        return apology("erro ao acessar o banco de dados")

    portfolio = []
    total = 0
    linha = []
    moeda = "usd"

    for row in rows:
        crypto = row["nm_crypto"]
        linha.append(crypto)

    precos = index_crypto_func(linha=",".join(linha), moeda=moeda)

    # exemplo: {"bitcoin": {"usd": 78088}, "solana": {"usd": 86.19}}

    if precos is None:
        return apology("não foi possível obter preços")

    for row in rows:

        crypto = row["nm_crypto"]

        if crypto not in precos:
            continue

        preco = precos[crypto][moeda]

        valor_total = preco * row["qt_compras"]

        total += valor_total

        portfolio.append({
            "nm_crypto": row["nm_crypto"],
            "qt_compras": row["qt_compras"],
            "preco": preco,
            "valor_total": valor_total
        })

    mensagem = ""

    if not portfolio:
        mensagem = "Você não possui nenhuma compra"

    row_dinheiro = db_query(db, "select qt_dinheiro from T_USUARIO where id_usuario = ?", session["id_usuario"])
    if row_dinheiro is None:
        return apology("erro ao acessar o banco de dados")

    dinheiro = row_dinheiro[0]["qt_dinheiro"]

    total += dinheiro

    return render_template("index.html", portfolio=portfolio, total=total, dinheiro=dinheiro, mensagem=mensagem)

@app.route("/market")
def market():

    moeda = "usd"

    estoques = []

    cryptos_arrumado = []

    for crypto in cryptos:

        cryptos_arrumado.append(crypto)

    precos = index_crypto_func(linha=",".join(cryptos_arrumado), moeda=moeda)

    if precos is None:
        return apology("não foi possível obter preços")

    for crypto in cryptos:

        nome_api = crypto

        if nome_api not in precos:
            continue

        estoque = {
            "nome": crypto,
            "preco": precos[nome_api][moeda]
        }

        estoques.append(estoque)

    return render_template("market.html", estoques=estoques)

@app.route("/market/<crypto>")
def pagina_crypto(crypto):

    days = 31
    
    if crypto not in cryptos:
        return apology("cripto inválida")
    
    historico = crypto_history_format_day(crypto, dias=days)
    
    if not historico:
        return apology("não foi possível obter histórico da criptomoeda")
    
    preco = historico[-1]["preco"]

    precos = []

    for preco_historico in historico:
        precos.append((preco_historico["preco"], preco_historico["data"]))
    
    if len(precos) > 0:
        max_preco = max(precos, key=lambda x: x[0])[0]
        min_preco = min(precos, key=lambda x: x[0])[0]
    else:
        max_preco = None
        min_preco = None

    return render_template("crypto.html", days=days, crypto=crypto, preco=preco, historico=historico, max_preco=max_preco, min_preco=min_preco)

@app.route("/buy/<crypto>", methods=["GET", "POST"])
@login_required
def buy(crypto):

    row_usuario = db_query(db, "select qt_dinheiro from T_USUARIO where id_usuario = ?", session["id_usuario"])
    if row_usuario is None:
        return apology("erro ao acessar o banco de dados")

    dinheiro = row_usuario[0]["qt_dinheiro"]

    if crypto not in cryptos:
        return apology("cripto inválida")
    
    historico = crypto_history_format_day(crypto)
    
    if not historico:
        return apology("não foi possível obter o histórico da criptomoeda")

    preco = historico[-1]["preco"]

    if preco is None:
        return apology("não foi possível obter o preço da criptomoeda")

    if request.method == "GET":
        return render_template("buy.html", dinheiro=dinheiro, crypto=crypto, preco=preco)
    
    quantidade = request.form.get("quantidade")
    if not quantidade:
        return apology("quantidade é obrigatória")

    try:
        quantidade = float(quantidade)
        if quantidade <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return apology("quantidade deve ser um número positivo")

    custo_total = preco * quantidade

    if custo_total > dinheiro:
        return apology("dinheiro insuficiente para esta compra")
    
    try:
        db.execute("BEGIN TRANSACTION")
        db.execute("update T_USUARIO set qt_dinheiro = qt_dinheiro - ? where id_usuario = ?", custo_total, session["id_usuario"])
        db.execute("insert into T_TRANSACAO (id_usuario, nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao) values (?, ?, ?, ?, ?)", session["id_usuario"], crypto, quantidade, preco, "BUY")
        db.execute("COMMIT")
    except Exception as e:
        print(e)
        db.execute("ROLLBACK")
        return apology("erro ao acessar o banco de dados")

    return redirect("/")

@app.route("/sell/<crypto>", methods=["GET", "POST"])
@login_required
def sell(crypto):

    if crypto not in cryptos:
        return apology("cripto inválida")
    
    historico = crypto_history_format_day(crypto)
    
    if not historico:
        return apology("não foi possível obter o histórico da criptomoeda")

    preco = historico[-1]["preco"]

    if preco is None:
        return apology("não foi possível obter o preço da criptomoeda")
    
    row = db_query(db, "select sum(qt_crypto) as qt_total from T_TRANSACAO where id_usuario = ? and nm_crypto = ?", session["id_usuario"], crypto)
    if row is None:
        return apology("erro ao acessar o banco de dados")
    
    quantidade_possui = row[0]["qt_total"]
    if quantidade_possui is None:
        quantidade_possui = 0

    if quantidade_possui <= 0:
        return apology("você não possui esta criptomoeda para vender")

    if request.method == "GET":
        return render_template("sell.html", crypto=crypto, preco=preco, quantidade_possui=quantidade_possui)
    
    quantidade_venda = request.form.get("quantidade_venda")
    if not quantidade_venda:
        return apology("quantidade de venda é obrigatória")

    try:
        quantidade_venda = float(quantidade_venda)
        if quantidade_venda <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return apology("quantidade de venda deve ser um número positivo")

    if quantidade_venda > quantidade_possui:
        return apology("você não possui esta quantidade da criptomoeda para vender")
    
    valor_total_venda = preco * quantidade_venda
    try:
        db.execute("BEGIN TRANSACTION")
        db.execute("insert into T_TRANSACAO (id_usuario, nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao) values (?, ?, ?, ?, ?)", session["id_usuario"], crypto, -quantidade_venda, preco, "SELL")
        db.execute("update T_USUARIO set qt_dinheiro = qt_dinheiro + ? where id_usuario = ?", valor_total_venda, session["id_usuario"])
        db.execute("COMMIT")
    except Exception as e:
        print(e)
        db.execute("ROLLBACK")
        return apology("erro ao acessar o banco de dados")
    return redirect("/")

@app.route("/history")
@login_required
def history():
    transactions = db_query(db, "select nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao, dt_transacao from T_TRANSACAO where id_usuario = ? order by dt_transacao desc", session["id_usuario"])
    if transactions is None:
        return apology("erro ao acessar o banco de dados")
    
    return render_template("history.html", transactions=transactions)

@app.route("/about")
def about():
    return render_template("about.html")