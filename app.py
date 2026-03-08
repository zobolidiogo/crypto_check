import os

from helpers import apology, crypto_history_format_day, crypto_price_now, login_required, usd, brl, val_nome, val_senha, crypto_name_format
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["brl"] = brl
app.jinja_env.filters["crypto_name_format"] = crypto_name_format

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///crypto.db")
db.execute("PRAGMA foreign_keys = ON")

cryptos = ["btc-bitcoin", "usdt-tether", "eth-ethereum", "sol-solana", "ada-cardano", "xrp-xrp", "doge-dogecoin"]

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    confirmacao = request.form.get("confirmacao")

    if not usuario:
        return apology("digite um usuário")
    
    if not senha:
        return apology("digite uma senha")
    
    erro_senha = val_senha(senha)
    if erro_senha:
        return apology(erro_senha)

    erro_usuario = val_nome(usuario)
    if erro_usuario:
        return apology(erro_usuario)

    if confirmacao != senha:
        return apology("as senhas não coincidem")

    rows = db.execute("select nm_usuario from T_USUARIO where nm_usuario = ?", usuario)
    if len(rows):
        return apology("o usuário já existe")
    
    hash = generate_password_hash(senha)
    db.execute("insert into T_USUARIO (nm_usuario, cd_hash) values (?, ?)", usuario, hash)

    rows = db.execute("select id_usuario, nm_usuario from T_USUARIO where nm_usuario = ?", usuario)
    session["id_usuario"] = rows[0]["id_usuario"]
    session["nm_usuario"] = rows[0]["nm_usuario"]

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if not usuario:
        return apology("precisa de um nome de usuário")
    
    if not senha:
        return apology("favor prover uma senha")
    
    rows = db.execute("select id_usuario, nm_usuario, cd_hash from T_USUARIO where nm_usuario = ?", usuario)

    if len(rows) != 1 or not check_password_hash(rows[0]["cd_hash"], senha):
        return apology("usuário e/ou senha inválido(s)")
    
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
    
    rows = db.execute("select nm_crypto, sum(qt_crypto) as qt_compras from T_TRANSACAO where id_usuario = ? group by nm_crypto having qt_compras > 0", session["id_usuario"])
    portfolio = []   
    total = 0

    for row in rows:
        preco = crypto_price_now(row["nm_crypto"])

        if preco is None:
            continue
        
        valor_total = preco * row["qt_compras"]
        total += valor_total

        portfolio.append(
            {
                "nm_crypto": row["nm_crypto"],
                "qt_compras": row["qt_compras"],
                "preco": preco,
                "valor_total": valor_total
            }
        )

    mensagem = ""
    if not portfolio:
        mensagem = "Você não possui nenhuma compra"
    
    row_dinheiro = db.execute("select qt_dinheiro from T_USUARIO where id_usuario = ?", session["id_usuario"])
    dinheiro = row_dinheiro[0]["qt_dinheiro"]
    total += dinheiro

    return render_template("index.html", portfolio=portfolio, total=total, dinheiro=dinheiro, mensagem=mensagem)

@app.route("/market")
@login_required
def market():
        
    estoques = []

    for crypto in cryptos:
        estoque = {
            "nome": crypto,
            "preco": crypto_price_now(crypto)
        }
        if estoque:
            estoques.append(estoque)
    
    return render_template("market.html", estoques=estoques)

@app.route("/market/<crypto>")
@login_required
def pagina_crypto(crypto):
    
    if crypto not in cryptos:
        return apology("cripto inválida")
    
    historico = crypto_history_format_day(crypto.split("-")[1])
    preco = crypto_price_now(crypto)
    
    precos = []

    for preco_historico in historico:
        precos.append((preco_historico["preco"], preco_historico["data"]))
    
    if len(precos) > 0:
        max_preco = max(precos, key=lambda x: x[0])[0]
        min_preco = min(precos, key=lambda x: x[0])[0]
    else:
        max_preco = None
        min_preco = None

    return render_template("crypto.html", crypto=crypto, preco=preco, historico=historico, max_preco=max_preco, min_preco=min_preco)

@app.route("/buy/<crypto>", methods=["GET", "POST"])
@login_required
def buy(crypto):

    if crypto not in cryptos:
        return apology("cripto inválida")
    
    preco = crypto_price_now(crypto)
    if preco is None:
        return apology("não foi possível obter o preço da criptomoeda")

    if request.method == "GET":
        return render_template("buy.html", crypto=crypto, preco=preco)
    
    quantidade = request.form.get("quantidade")
    if not quantidade:
        return apology("quantidade é obrigatória")

    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return apology("quantidade deve ser um número inteiro positivo")
    
    row_usuario = db.execute("select qt_dinheiro from T_USUARIO where id_usuario = ?", session["id_usuario"])
    dinheiro = row_usuario[0]["qt_dinheiro"]

    custo_total = preco * quantidade

    if custo_total > dinheiro:
        return apology("dinheiro insuficiente para esta compra")
    
    db.execute("update T_USUARIO set qt_dinheiro = qt_dinheiro - ? where id_usuario = ?", custo_total, session["id_usuario"])
    db.execute("insert into T_TRANSACAO (id_usuario, nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao) values (?, ?, ?, ?, ?)", session["id_usuario"], crypto, quantidade, preco, "BUY")

    return redirect("/")

@app.route("/sell/<crypto>", methods=["GET", "POST"])
@login_required
def sell(crypto):

    if crypto not in cryptos:
        return apology("cripto inválida")
    
    preco = crypto_price_now(crypto)
    if preco is None:
        return apology("não foi possível obter o preço da criptomoeda")
    
    row = db.execute("select sum(qt_crypto) as qt_total from T_TRANSACAO where id_usuario = ? and nm_crypto = ?", session["id_usuario"], crypto)
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
        quantidade_venda = int(quantidade_venda)
        if quantidade_venda <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return apology("quantidade de venda deve ser um número inteiro positivo")

    if quantidade_venda > quantidade_possui:
        return apology("você não possui esta quantidade da criptomoeda para vender")
    
    valor_total_venda = preco * quantidade_venda
    db.execute("insert into T_TRANSACAO (id_usuario, nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao) values (?, ?, ?, ?, ?)", session["id_usuario"], crypto, -quantidade_venda, preco, "SELL")
    db.execute("update T_USUARIO set qt_dinheiro = qt_dinheiro + ? where id_usuario = ?", valor_total_venda, session["id_usuario"])

    return redirect("/")

@app.route("/history")
@login_required
def history():
    transactions = db.execute("select nm_crypto, qt_crypto, vl_unitario_usd, tp_transacao, dt_transacao from T_TRANSACAO where id_usuario = ? order by dt_transacao desc", session["id_usuario"])
    return render_template("history.html", transactions=transactions)
