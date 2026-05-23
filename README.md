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

Criar uma aplicação web completa que permitisse aos usuários praticar investimentos em criptomoedas sem risco financeiro, integrando cotações reais de mercado, gerenciamento de portfólio, histórico de transações e visualização de dados através de uma interface intuitiva, responsiva e acessível em diferentes dispositivos.

---

## A Solução

Aplicação full-stack que simula uma exchange de criptomoedas, utilizando Flask no backend, PostgreSQL em nuvem via Supabase e integração com a CoinGecko API para dados de mercado em tempo real — com sistema de cache em memória para otimizar requisições e respeitar rate limits.

Usuários iniciam com $10.000 virtuais e podem negociar 7 criptomoedas principais:

- Bitcoin
- Ethereum
- Tether
- Solana
- Cardano
- XRP
- Dogecoin

---

## Funcionalidades Principais

### Sistema de Autenticação

- Registro com validação de nome de usuário e senha
- Login seguro com hashing de senhas via Werkzeug
- Gerenciamento de sessões server-side com Flask-Session
- Proteção de rotas com decorator `@login_required`
- Redirecionamento automático para usuários já autenticados

### Validações de Formulário

**Nome de usuário:**
- Entre 3 e 20 caracteres
- Não pode começar com número
- Apenas letras, números e `_`

**Senha:**
- Entre 6 e 20 caracteres
- Obrigatório: letra minúscula, maiúscula e número
- Sem caracteres especiais

### Gestão de Portfólio

- Dashboard interativo com ativos do usuário
- Cálculo automático do valor total da carteira em tempo real
- Exibição de quantidade, preço unitário e valor total por ativo
- Saldo em dinheiro virtual separado dos ativos

### Sistema de Negociação

- Compra de criptomoedas com validação de saldo
- Venda de ativos com verificação de quantidade disponível
- Transações atômicas com `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK`
- Registro completo de todas as operações

### Histórico de Transações

- Listagem completa ordenada por data (mais recente primeiro)
- Exibe tipo (BUY/SELL), quantidade, preço unitário e data de cada operação

### Análise de Mercado

- Lista de criptomoedas disponíveis com preços atuais
- Página individual para cada criptomoeda
- Gráfico histórico de preços dos últimos 30 dias via Chart.js
- Estatísticas de preço máximo e mínimo no período
- Acesso ao mercado disponível mesmo sem login

### Interface

- Layout responsivo para desktop e mobile
- Filtros Jinja2 customizados: `usd` (dólar) e `brl` (real brasileiro)
- Formulário de contato integrado ao layout
- Página `/about` com informações do projeto
- Cache HTTP via `@app.after_request` para evitar páginas desatualizadas após logout

---

## Arquitetura Técnica

### Backend (`app.py`)

- 9 rotas Flask cobrindo autenticação, portfólio, mercado, negociação, histórico e about
- Integração com PostgreSQL via CS50 SQL
- Controle de sessões e proteção de rotas
- Transações atômicas para operações financeiras

### Helpers (`helpers.py`)

- `index_crypto_func()` — consulta em lote via `/simple/price` da CoinGecko com cache em memória
- `crypto_history_format_day()` — histórico de preços via `market_chart` com cache em memória
- `db_query()` — wrapper seguro para queries com tratamento de exceções
- `val_nome()` / `val_senha()` — validações de formulário com regras explícitas
- `usd()` / `brl()` — filtros de formatação monetária registrados no Jinja2
- `login_required` — decorator de proteção de rotas
- `apology()` — renderização padronizada de erros
- `requests.Session()` persistente com API key no header para maior limite de requisições

---

## Sistema de Cache

A aplicação implementa cache em memória para preços e históricos, reduzindo chamadas à API externa e evitando rate limits:

```python
CACHE_TEMPO = 60  # segundos
```

**Como funciona:**
- Preços em tempo real e históricos são armazenados em dicionários em memória (`cache_precos`, `cache_historico`)
- Chave do cache é composta por `ids_cryptos:moeda` (preços) ou `crypto:moeda:dias` (histórico)
- A cada requisição, verifica se o cache existe e se ainda é válido (menos de 60 segundos)
- Se válido, retorna os dados em cache sem chamar a API
- Se expirado ou ausente, busca da CoinGecko, atualiza o cache e retorna os dados

**Benefícios:**
- Redução drástica de chamadas externas em páginas com múltiplos usuários simultâneos
- Respeito aos rate limits da CoinGecko
- Melhora na performance e tempo de resposta da aplicação

**API Key:**
- Autenticação via `x-cg-demo-api-key` no header da `requests.Session()`, aumentando o limite de requisições permitidas pela CoinGecko

---

## Banco de Dados (PostgreSQL + Supabase)

> Inicialmente o projeto utilizava SQLite durante o desenvolvimento local. Posteriormente, a aplicação foi migrada para PostgreSQL via Supabase, aproximando o projeto de um ambiente de produção real.

### `T_USUARIO`

| Campo | Tipo | Descrição |
|---|---|---|
| id_usuario | SERIAL PK | Identificador único |
| nm_usuario | VARCHAR(20) UNIQUE | Nome de usuário |
| cd_hash | TEXT | Hash da senha |
| qt_dinheiro | NUMERIC | Saldo virtual (default: 10000) |

### `T_TRANSACAO`

| Campo | Tipo | Descrição |
|---|---|---|
| id_transacao | SERIAL PK | Identificador único |
| id_usuario | INTEGER FK | Referência ao usuário |
| nm_crypto | TEXT | Nome da criptomoeda |
| qt_crypto | NUMERIC | Quantidade (negativa em SELL) |
| vl_unitario_usd | NUMERIC | Preço unitário na transação |
| tp_transacao | TEXT | Tipo: BUY ou SELL |
| dt_transacao | TIMESTAMP | Data e hora da operação |

---

## Frontend (HTML/CSS/JavaScript)

### Templates Jinja2

- `layout.html` — base com navegação e formulário de contato
- `index.html` — dashboard do portfólio
- `market.html` — lista de criptomoedas com preços
- `crypto.html` — página individual com gráfico e estatísticas
- `buy.html` / `sell.html` — formulários de negociação
- `history.html` — histórico de transações
- `login.html` / `register.html` — autenticação
- `about.html` — sobre o projeto
- `apology.html` — página de erros

### Chart.js

- Gráfico de linha com histórico de preços dos últimos 30 dias
- Labels formatados como `dd/mm/aaaa`
- Estatísticas de máximo e mínimo no período

---

### JavaScript (`static/trade.js`)

Cálculo dinâmico do valor estimado nos formulários de compra e venda — atualiza em tempo real conforme o usuário digita a quantidade, multiplicando pelo preço atual sem necessidade de recarregar a página.

---

### Responsividade

Layout adaptado para diferentes resoluções via CSS, com navegação fluida em dispositivos móveis e desktop.

---

## Estrutura de Arquivos

```txt
crypto_check/
├── app.py
├── helpers.py
├── requirements.txt
├── schema.sql
├── .env.example
├── static/
│   ├── chart.js
│   ├── trade.js
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
    ├── about.html
    └── apology.html
```

---

## Como Reproduzir o Projeto

### Pré-requisitos

- Python
- pip
- Conta no Supabase

### 1. Clone o repositório

```bash
git clone https://github.com/zobolidiogo/crypto_check.git
cd crypto_check
```

### 2. Crie um projeto no Supabase

1. Acesse https://supabase.com
2. Crie um novo projeto
3. Vá em `Project Settings → Database`
4. Copie a connection string do PostgreSQL

### 3. Execute o `schema.sql`

1. Abra o **SQL Editor** no Supabase
2. Cole o conteúdo do `schema.sql`
3. Execute para criar as tabelas

### 4. Crie o arquivo `.env`

Baseado no `.env.example`:

```env
DATABASE_URL=postgresql://usuario:SUA_SENHA@host:5432/postgres
SECRET_KEY=sua_secret_key
COINGECKO_API_KEY=sua_api_key
```

> O arquivo `.env` não deve ser enviado ao GitHub.

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
flask run
```

### 7. Acesse no navegador

```txt
http://127.0.0.1:5000
```

---

## Deploy

A aplicação foi publicada utilizando:

- **Render** — deploy da aplicação Flask
- **Supabase** — PostgreSQL em nuvem

### Variáveis de ambiente

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
COINGECKO_API_KEY=your_api_key
```

---

## Segurança

- Hashing de senhas com Werkzeug
- Sessões server-side com Flask-Session
- Proteção de rotas com `@login_required`
- Validação de inputs no servidor
- Transações atômicas com rollback em caso de erro
- Variáveis sensíveis protegidas via `.env`
- API key no header da sessão HTTP (não exposta no frontend)
- Cache HTTP para evitar dados desatualizados após logout

---

## Diferenciais do Projeto

### Cache em Memória
Sistema de cache implementado do zero sem dependências externas, com TTL de 60 segundos, chaves compostas e invalidação automática por tempo — reduz chamadas à API e melhora performance.

### Consultas em Lote (Batching)
Endpoint `/simple/price` da CoinGecko utilizado para buscar múltiplos preços em uma única requisição, com IDs ordenados para maximizar reaproveitamento do cache.

### Transações Atômicas
Operações de compra e venda protegidas com `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK`, garantindo consistência dos dados mesmo em caso de falha.

### Arquitetura Modular
Separação clara entre `app.py` (rotas e lógica de negócio) e `helpers.py` (utilitários, API, validações, formatação) — código reutilizável e fácil de manter.

### Estrutura Próxima de Produção
PostgreSQL em nuvem, deploy cloud, variáveis de ambiente, API key autenticada e configuração segura — projeto preparado para ambiente real.

---

## Melhorias Futuras

- Verificação de email para recuperação de senha
- WebSockets para atualização de preços sem recarregar a página
- Sistema de watchlist de criptomoedas
- Mais criptomoedas disponíveis
- Dockerização
- Testes automatizados
- Cache persistente com Redis (substituindo cache em memória)
- Background jobs para atualização periódica de preços
- API própria
- Sistema de ranking de usuários

---

## Tecnologias Utilizadas

**Backend:** Python, Flask, Flask-Session, Werkzeug, CS50 Library

**Database:** PostgreSQL, Supabase

**Frontend:** HTML5, CSS3, JavaScript, Jinja2, Chart.js

**APIs Externas:** CoinGecko API

**Infraestrutura:** Render, GitHub

**Ferramentas:** VS Code, Git

---

## Aprendizados

Este projeto consolidou conhecimentos em desenvolvimento full-stack, integração de APIs, cache em memória, modelagem de banco de dados relacional, PostgreSQL, deploy cloud, segurança em aplicações web, visualização de dados, organização de código e arquitetura web.

Projeto desenvolvido como Final Project do **CS50x: Introduction to Computer Science** da Harvard University.

---

## Contato

**Diogo Zoboli**

- GitHub: https://github.com/zobolidiogo
- LinkedIn: https://linkedin.com/in/zobolidiogo

---

⭐ Se este projeto foi interessante para você, considere dar uma estrela no repositório.

*This was CS50!*
