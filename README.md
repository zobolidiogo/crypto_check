# crypto.check: Simulador de Investimentos em Criptomoedas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

Plataforma web para simulação de investimentos em criptomoedas com dados de mercado em tempo real, desenvolvida como projeto final do CS50 (Harvard University).

---

## Deploy Online

A aplicação está disponível online através do Render:

🔗 **Live Demo:** https://crypto-check-vgkv.onrender.com/

> Por utilizar o plano gratuito do Render, a aplicação pode levar alguns segundos para iniciar após períodos de inatividade.

---

## O Desafio

Criar uma aplicação web completa que permitisse aos usuários praticar investimentos em criptomoedas sem risco financeiro, integrando cotações reais de mercado, gerenciamento de portfólio, histórico de transações e visualização de dados através de uma interface intuitiva e responsiva.

---

## A Solução

Aplicação full-stack que simula uma exchange de criptomoedas, utilizando Flask no backend, PostgreSQL em nuvem via Supabase e integração com APIs externas para dados de mercado em tempo real.

Usuários iniciam com $10.000 virtuais e podem negociar 7 criptomoedas principais:

- Bitcoin
- Ethereum
- Tether
- Solana
- Cardano
- XRP
- Dogecoin

Os preços são atualizados em tempo real via APIs públicas.

---

## Funcionalidades Principais

### Sistema de Autenticação

- Registro com validação
- Login seguro com hashing de senhas
- Gerenciamento de sessões server-side
- Controle de autenticação

### Gestão de Portfolio

- Dashboard interativo mostrando ativos do usuário
- Cálculo automático do valor total da carteira
- Atualização de preços em tempo real
- Exibição de quantidade, preço unitário e valor total por ativo

### Sistema de Negociação

- Compra de criptomoedas com validação de saldo
- Venda de ativos com verificação de quantidade disponível
- Registro completo de transações
- Histórico detalhado de operações

### Análise de Mercado

- Lista de criptomoedas disponíveis com preços atuais
- Página individual para cada criptomoeda
- Gráfico histórico de preços dos últimos 30 dias
- Estatísticas de preço máximo e mínimo
- Visualização interativa utilizando Chart.js

### Integrações API

- CoinPaprika API para cotações em tempo real
- CoinGecko API para histórico de preços
- Tratamento de falhas e timeouts

---

## Arquitetura Técnica

### Backend (Flask + Python)

#### `app.py`

Responsável por:

- Rotas da aplicação
- Sistema de autenticação
- Sistema de portfolio
- Compra e venda de criptomoedas
- Histórico de transações
- Integração com PostgreSQL
- Controle de sessões

#### `helpers.py`

Contém:

- Busca de preços em tempo real
- Histórico de criptomoedas
- Validação de usuários e senhas
- Decorators de autenticação
- Funções auxiliares de formatação

---

## Banco de Dados (PostgreSQL + Supabase)

> Inicialmente o projeto utilizava SQLite durante o desenvolvimento local. Posteriormente, a aplicação foi migrada para PostgreSQL utilizando Supabase como infraestrutura de banco de dados em nuvem, aproximando o projeto de um ambiente mais próximo de produção.

### `T_USUARIO`

| Campo | Tipo |
|---|---|
| id_usuario | PK |
| nm_usuario | UNIQUE |
| cd_hash | TEXT |
| qt_dinheiro | NUMERIC |

### `T_TRANSACAO`

| Campo | Tipo |
|---|---|
| id_transacao | PK |
| id_usuario | FK |
| nm_crypto | TEXT |
| qt_crypto | NUMERIC |
| vl_unitario_usd | NUMERIC |
| tp_transacao | TEXT |
| dt_transacao | TIMESTAMP |

---

## Frontend (HTML/CSS/JavaScript)

### Templates Jinja2

- Dashboard
- Mercado
- Página da criptomoeda
- Histórico
- Login
- Registro

### Chart.js

Utilizado para:

- Histórico de preços
- Visualização temporal
- Estatísticas de mercado

---

## Estrutura de Arquivos

```txt
crypto_check/
├── app.py
├── helpers.py
├── requirements.txt
├── .env.example
├── static/
│   ├── chart.js
│   ├── styles.css
│   └── favicon.ico
└── templates/
    ├── layout.html
    ├── index.html
    ├── market.html
    ├── crypto.html
    ├── buy.html
    ├── sell.html
    ├── history.html
    ├── login.html
    ├── register.html
    └── apology.html
```

---

## Como Reproduzir o Projeto

### Pré-requisitos

- Python
- pip

---

### 1. Clone o repositório

```bash
git clone https://github.com/zobolidiogo/crypto-check.git
cd crypto-check
```

---

### 2. Crie um arquivo `.env`

Baseado no `.env.example`:

```env
DATABASE_URL=postgresql://postgres:your_password@host:5432/postgres
SECRET_KEY=your_secret_key_here
```

> O arquivo `.env` não deve ser enviado para o GitHub, pois contém credenciais sensíveis da aplicação.

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Execute a aplicação

```bash
flask run
```

---

### 5. Acesse no navegador

```txt
http://127.0.0.1:5000
```

---

## Deploy

A aplicação foi publicada utilizando:

- Render (Deploy)
- Supabase (PostgreSQL Cloud)

### Variáveis de ambiente utilizadas

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## Tecnologias Utilizadas

### Backend

- Python
- Flask
- Flask-Session
- Werkzeug
- CS50 Library

### Database

- PostgreSQL
- Supabase

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2
- Chart.js

### APIs Externas

- CoinPaprika API
- CoinGecko API

### Infraestrutura & Deploy

- Render
- GitHub

### Ferramentas

- VS Code
- Git

---

## Segurança

- Hashing de senhas
- Sessões server-side
- Proteção de rotas com `@login_required`
- Validação de inputs
- Variáveis sensíveis protegidas via `.env`
- Uso de environment variables no deploy

---

## Diferenciais do Projeto

### Integração de APIs

- Dados em tempo real
- Histórico de preços
- Tratamento de falhas externas

### Arquitetura Modular

- Separação entre lógica, templates e utilitários
- Código reutilizável
- Estrutura organizada

### Visualização de Dados

- Gráficos interativos
- Histórico temporal
- Estatísticas de mercado

### Estrutura Próxima de Produção

- PostgreSQL em nuvem
- Deploy cloud
- Variáveis de ambiente
- Configuração segura
- Estrutura preparada para produção

---

## Melhorias Futuras

- WebSockets para preços em tempo real
- Sistema de watchlist
- Mais criptomoedas
- Dockerização
- Testes automatizados
- Cache de preços
- API própria
- Responsividade aprimorada
- Sistema de ranking de usuários

---

## Aprendizados

Este projeto consolidou conhecimentos em:

- Desenvolvimento full-stack
- Integração de APIs
- Modelagem de banco de dados
- PostgreSQL
- Deploy cloud
- Segurança em aplicações web
- Visualização de dados
- Flask
- Organização de código
- Configuração de ambiente
- Arquitetura web

Projeto desenvolvido como Final Project do **CS50x: Introduction to Computer Science** da Harvard University.

---

## Contato

**Diogo Zoboli**

- GitHub: [github.com/zobolidiogo](https://github.com/zobolidiogo)
- LinkedIn: [linkedin.com/in/zobolidiogo](https://linkedin.com/in/zobolidiogo)

---

⭐ Se este projeto foi interessante para você, considere dar uma estrela no repositório.

*This was CS50!*