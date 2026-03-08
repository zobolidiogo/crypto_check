import requests

from datetime import datetime
from flask import render_template, session, redirect
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from functools import wraps

def crypto_name_format(nm_crypto):
    return nm_crypto.split("-")[1].capitalize()

def apology(mensagem):
    return render_template("apology.html", mensagem=mensagem)


def crypto_price_now(nm_crypto, moeda="usd"):
    
    url = f"https://api.coinpaprika.com/v1/tickers/{nm_crypto}?quotes={moeda}"
    try:
        
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        if not "quotes" in dados:
            return None

        preco = dados["quotes"][moeda.upper()]["price"]

        preco_formatado = Decimal(preco).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        return float(preco_formatado)
    
    except requests.RequestException as re:
        print(f"Erro de pedido: {re}")
    except (KeyError, ValueError) as kv:
        print(f"Erro de dados: {kv}")

    return None
    """
    exemplo de retorno:
    908900
    """

def crypto_history_format_day(nm_crypto, moeda="usd", dias=30):
    
    url = f"https://api.coingecko.com/api/v3/coins/{nm_crypto}/market_chart?vs_currency={moeda}&days={dias}"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        precos = dados.get("prices", [])
        if not precos:
            return []

        preco_diario = {}
        for ms, preco in precos:
            data = datetime.fromtimestamp(ms/1000).date()
            preco_diario[data] = preco

        datas_sortidas = sorted(preco_diario.keys())[-dias:]
        formatado = []
        for data in datas_sortidas:
            preco = Decimal(preco_diario[data]).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            formatado.append({
                "data": data.isoformat(),
                "preco": float(preco)
            })
        
        return formatado
    
    except requests.RequestException as re:
        print(f"Erro de pedido: {re}")
    except (KeyError, ValueError) as kv:
        print(f"Erro de dados: {kv}")

    return []
    # [{data: "2024-05-01", preco: 908900}, {data: "2024-05-02", preco: 912000}, ...]


def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id_usuario") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function

def usd(vl):
    try:
        formatacao = Decimal(vl)
    except(TypeError, ValueError, InvalidOperation):
        return "$ 0.00"
    return f"$ {formatacao:,.2f}"

def brl(vl):
    try:
        vl = Decimal(vl)
    except(TypeError, ValueError, InvalidOperation):
        return "R$ 0,00"
    formatacao = f"{vl:,.2f}"
    formatacao = formatacao.replace(",", "x").replace(".", ",").replace("x", ".")
    return f"R$ {formatacao}"

def val_nome(nome):
    if len(nome) < 3 or len(nome) > 20:
        return "o nome de usuário precisa ter entre 3-20 caracteres"

    if nome[0].isdigit():
        return "o nome de usuário não pode começar com um número"

    for caractere in nome:
        if not (caractere.isalnum() or caractere in "_"):
            return "o nome de usuário só pode conter letras, números e _"

    return None

def val_senha(senha):

    if len(senha) < 6 or len(senha) > 10:
        return "a senha precisa ter entre 6-10 caracteres"

    tem_minuscula = False
    tem_maiuscula = False
    tem_numero = False

    for caractere in senha:
        
        if caractere.islower():
            tem_minuscula = True

        elif caractere.isupper():
            tem_maiuscula = True

        elif caractere in "0123456789":
            tem_numero = True

        else:
            return "a senha não pode conter caracteres especiais"

    if not tem_minuscula:
        return "a senha precisa conter pelo menos uma letra minúscula"

    if not tem_maiuscula:
        return "a senha precisa conter pelo menos uma letra maiúscula"

    if not tem_numero:
        return "a senha deve conter pelo menos um número"

    return None