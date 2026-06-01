import requests
import time
import os

from dotenv import load_dotenv
from datetime import datetime
from flask import render_template, session, redirect
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from functools import wraps

load_dotenv()

keys = {
    "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
}

BASE_COINGECKO_URL = "https://api.coingecko.com/api/v3"

CACHE_TEMPO = 60

cache_precos = {}
cache_historico = {}

session_requests = requests.Session()
session_requests.headers.update(keys)

def db_query(db, query, *params):
    try:
        return db.execute(query, *params)
    except Exception as e:
        print(e)
        return None

def apology(mensagem):
    return render_template("apology.html", mensagem=mensagem)

def index_crypto_func(linha, moeda="usd"):

    linha = ",".join(sorted(linha.split(",")))

    chave_cache = f"{linha}:{moeda}"

    if chave_cache in cache_precos:
        tempo_cache = cache_precos[chave_cache]["tempo"]

        if time.time() - tempo_cache < CACHE_TEMPO:
            print("Usando cache para preços")
            return cache_precos[chave_cache]["dados"]

    url = f"{BASE_COINGECKO_URL}/simple/price?ids={linha}&vs_currencies={moeda}"
    try:
        resposta = session_requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        cache_precos[chave_cache] = {
            "dados": dados,
            "tempo": time.time()
        }
        print("Cache atualizado para preços")
        return dados
    
    except requests.RequestException as re:
        print(f"Erro de pedido: {re}")
    return None

def crypto_history_format_day(nm_crypto, moeda="usd", dias=30):
    
    chave_cache = f"{nm_crypto}:{moeda}:{dias}"

    if chave_cache in cache_historico:

        tempo_cache = cache_historico[chave_cache]["tempo"]

        if time.time() - tempo_cache < CACHE_TEMPO:
            print("usando cache de histórico")
            return cache_historico[chave_cache]["dados"]
    
    url = f"{BASE_COINGECKO_URL}/coins/{nm_crypto}/market_chart?vs_currency={moeda}&days={dias}"
    
    try:
        resposta = session_requests.get(url)
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
        
        cache_historico[chave_cache] = {
            "dados": formatado,
            "tempo": time.time()
        }
        print("cache atualizado para histórico")
        
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
            return redirect("/market")
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

def primeira_letra_maiuscula(texto):
    if not texto:
        return ""
    return texto.capitalize()

def val_display(nome):
    if len(nome) < 1 or len(nome) > 20:
        return "o nome precisa ter entre 1-20 caracteres"

    if nome[0].isdigit():
        return "o nome não pode começar com um número"

    if "__" in nome:
        return "o nome não pode conter dois _ seguidos"

    if "  " in nome:
        return "o nome não pode conter espaços consecutivos"

    for caractere in nome:
        if not (caractere.isalnum() or caractere in "_ "):
            return "o nome só pode conter espaços, letras, números e _"
        
    return None

def val_nome(nome):
    if len(nome) < 3 or len(nome) > 20:
        return "o nome de usuário precisa ter entre 3-20 caracteres"

    if nome[0].isdigit():
        return "o nome de usuário não pode começar com um número"
    
    permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

    for caractere in nome:
        if not caractere in permitidos:
            return "o nome de usuário só pode conter letras (a-z), números (0-9) e underline (_)"

    return None

def val_senha(senha):

    if len(senha) < 6 or len(senha) > 20:
        return "a senha precisa ter entre 6-20 caracteres"

    tem_letra = False
    tem_numero = False

    for caractere in senha:
        
        if caractere.isalpha():
            tem_letra = True

        elif caractere in "0123456789":
            tem_numero = True

    if not tem_letra:
        return "a senha precisa conter pelo menos uma letra"

    if not tem_numero:
        return "a senha precisa conter pelo menos um número"

    return None