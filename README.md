# crypto.check: Simulador de Investimentos em Criptomoedas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

Plataforma web para simulação de investimentos em criptomoedas com dados de mercado em tempo real, desenvolvida como projeto final do CS50 (Harvard University).

---

## O Desafio

Criar uma aplicação web completa que permitisse aos usuários praticar investimentos em criptomoedas sem risco financeiro, integrando cotações reais de mercado, gerenciamento de portfólio, histórico de transações e visualização de dados através de uma interface intuitiva e responsiva.

---

## A Solução

Aplicação full-stack que simula uma exchange de criptomoedas, utilizando Flask no backend, PostgreSQL em nuvem via Supabase e integração com APIs externas para dados de mercado em tempo real.

Usuários iniciam com $10.000 virtuais e podem negociar 7 criptomoedas principais (Bitcoin, Ethereum, Tether, Solana, Cardano, XRP e Dogecoin) com preços atualizados em tempo real via APIs públicas.

### Funcionalidades Principais

### Sistema de Autenticação

- Registro com validação robusta
- Login seguro com hash de senha
- Gerenciamento de sessões server-side

### Gestão de Portfolio

- Dashboard interativo mostrando criptomoedas do usuário
- Cálculo automático de valor total
- Atualização de preços em tempo real
- Exibição de quantidade, preço unitário e valor total por ativo

### Sistema de Negociação

- Compra de criptomoedas com validação de saldo
- Venda de ativos com verificação de quantidade disponível
- Registro completo de transações com timestamp
- Histórico detalhado de operações

### Análise de Mercado

- Lista de criptomoedas disponíveis com preços atuais
- Página individual por cripto com gráfico de 30 dias
- Estatísticas de preço máximo e mínimo
- Visualização interativa utilizando Chart.js

### Integrações API

- CoinPaprika: cotações em tempo real
- CoinGecko: histórico de preços
- Tratamento robusto de falhas e timeouts

---

## Arquitetura Técnica

### Backend (Flask + Python)

#### `app.py`

- Rotas de autenticação
- Sistema de portfolio
- Sistema de compra e venda
- Histórico de transações
- Integração com PostgreSQL

#### `helpers.py`

- Busca de preços em tempo real
- Histórico de criptomoedas
- Validação de usuários e senhas
- Decorators de autenticação
- Funções auxiliares de formatação

### Banco de Dados (PostgreSQL + Supabase)

> **Atualização recente:** originalmente o projeto utilizava SQLite durante o desenvolvimento inicial. Posteriormente, a aplicação foi migrada para PostgreSQL utilizando Supabase como infraestrutura de banco de dados em nuvem, aproximando o projeto de um ambiente mais próximo de produção com persistência de dados em cloud.

#### `T_USUARIO`

- id_usuario (PK)
- nm_usuario (UNIQUE)
- cd_hash
- qt_dinheiro

#### `T_TRANSACAO`

- id_transacao (PK)
- id_usuario (FK)
- nm_crypto
- qt_crypto
- vl_unitario_usd
- tp_transacao
- dt_transacao

### Frontend (HTML/CSS/JavaScript)

#### Templates Jinja2

- Dashboard
- Mercado
- Página individual da criptomoeda
- Histórico
- Login e registro

#### Chart.js

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

### Instalação

#### 1. Clone o repositório

```bash
git clone https://github.com/zobolidiogo/crypto-check.git
cd crypto-check
```

#### 2. Crie um arquivo `.env` baseado no `.env.example`

```env
DATABASE_URL=postgresql://postgres:your_password@host:5432/postgres
SECRET_KEY=your_secret_key_here
```

> O arquivo `.env` não deve ser enviado para o GitHub, pois contém credenciais sensíveis da aplicação.

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Execute a aplicação

```bash
flask run
```

#### 5. Acesse no navegador

```txt
http://127.0.0.1:5000
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

### Ferramentas

- Git/GitHub
- VS Code

---

## Segurança

- Hashing de senhas
- Sessões server-side
- Proteção de rotas com `@login_required`
- Validação de inputs
- Variáveis sensíveis protegidas via `.env`

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
- Variáveis de ambiente
- Configuração segura
- Estrutura preparada para deploy

---

## Melhorias Futuras

- Deploy completo em nuvem (Render + Supabase)
- WebSockets para preços em tempo real
- Sistema de watchlist
- Mais criptomoedas
- Dockerização
- Testes automatizados
- Cache de preços
- API própria

---

## Aprendizados

Este projeto consolidou conhecimentos em:

- Desenvolvimento full-stack
- Integração de APIs
- Modelagem de banco de dados
- PostgreSQL
- Segurança em aplicações web
- Visualização de dados
- Flask
- Organização de código
- Deploy e configuração de ambiente

Projeto desenvolvido como Final Project do **CS50x: Introduction to Computer Science** da Harvard University.

---

## Contato

**Diogo Zoboli**

- GitHub: [github.com/zobolidiogo](https://github.com/zobolidiogo)
- LinkedIn: [linkedin.com/in/zobolidiogo](https://linkedin.com/in/zobolidiogo)

---

⭐ Se este projeto foi interessante para você, considere dar uma estrela no repositório.
*This was CS50!*
