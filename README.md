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

Aplicação full-stack que simula uma exchange de criptomoedas, utilizando Flask no backend, PostgreSQL em nuvem via Supabase e integração com APIs externas para dados de mercado em tempo real.

Usuários iniciam com $10.000 virtuais e podem negociar 7 criptomoedas principais:

- Bitcoin
- Ethereum
- Tether
- Solana
- Cardano
- XRP
- Dogecoin

Os preços são atualizados em tempo real via CoinGecko API, utilizando consultas otimizadas em lote para reduzir o número de requisições externas e melhorar a performance da aplicação.

---

## Funcionalidades Principais

### Sistema de Autenticação

- Registro com validação
- Login seguro com hashing de senhas
- Gerenciamento de sessões server-side
- Controle de autenticação

### Gestão de Portfólio

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

### Navegação e Interface

- Página "Sobre" com informações do projeto
- Layout responsivo para desktop e mobile
- Interface adaptada para diferentes resoluções
- Navegação simplificada e intuitiva

### Integrações API

- CoinGecko API centralizada para cotações atuais e dados históricos
- Consultas otimizadas em lote (*batch requests*) para prevenção de *rate limits*
- Tratamento de falhas, erros externos e *timeouts*

---

## Arquitetura Técnica

### Backend (Flask + Python)

#### `app.py`

Responsável por:

- Rotas da aplicação
- Sistema de autenticação
- Sistema de portfólio com agregação de dados pré-request
- Compra e venda de criptomoedas
- Histórico de transações
- Integração com PostgreSQL
- Controle de sessões
- Rota `/about`

#### `helpers.py`

Contém:

- Centralização de consultas em lote via endpoint `/simple/price` da CoinGecko
- Busca de dados históricos de criptomoedas via endpoint `market_chart`
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
- Página About

### Responsividade

O CSS da aplicação foi ajustado para melhorar a experiência em diferentes dispositivos e resoluções, tornando a navegação mais fluida em telas menores.

### Chart.js

Utilizado para:

- Histórico de preços
- Visualização temporal
- Estatísticas de mercado

---

## Estrutura de Arquivos

```txt
crypto-check/
├── app.py
├── helpers.py
├── requirements.txt
├── schema.sql
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
    ├── about.html
    └── apology.html
```

---

## `schema.sql`

Arquivo responsável pela criação da estrutura inicial do banco PostgreSQL da aplicação, incluindo:

- Tabelas
- Chaves primárias
- Relacionamentos
- Constraints

---

## Como Reproduzir o Projeto

### Pré-requisitos

- Python
- pip
- Conta no Supabase

---

### 1. Clone o repositório

```bash
git clone https://github.com/zobolidiogo/crypto-check.git
cd crypto-check
```

---

### 2. Crie um projeto no Supabase

1. Acesse o https://supabase.com
2. Crie um novo projeto
3. Aguarde a inicialização do banco PostgreSQL
4. Vá em:

```txt
Project Settings → Database
```

5. Copie a connection string do banco PostgreSQL

---

### 3. Execute o `schema.sql`

1. Abra o menu **SQL Editor** no Supabase
2. Crie uma nova query
3. Cole o conteúdo do arquivo `schema.sql`
4. Execute o script para criar as tabelas da aplicação

---

### 4. Crie um arquivo `.env`

Baseado no `.env.example`:

```env
DATABASE_URL=postgresql://usuario:SUA_SENHA@host:5432/postgres
SECRET_KEY=sua_secret_key
```

> Substitua `SUA_SENHA` pela senha definida no Supabase durante a criação do projeto.

> O arquivo `.env` não deve ser enviado para o GitHub, pois contém credenciais sensíveis da aplicação.

---

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 6. Execute a aplicação

```bash
flask run
```

---

### 7. Acesse no navegador

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

- CoinGecko API (Preços em tempo real e histórico)

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

### Otimização e Consumo de API

- **Redução de Chamadas Desnecessárias:** substituição do modelo antigo de requisições individuais por uma arquitetura centralizada, eliminando requests repetidas por página.

- **Consultas em Lote (Batching):** utilização estratégica do endpoint `/simple/price` da CoinGecko, permitindo que páginas como `market` e `index` realizem apenas uma única requisição para coletar todos os dados necessários. O processamento passa a ser feito localmente, reduzindo dependências externas e mitigando problemas com *rate limits*.

- **Padronização da Camada de Dados:** consolidação de preços atuais e históricos em um único provedor de API, tornando o backend mais simples, consistente e fácil de manter.

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

### Experiência do Usuário

- Interface responsiva
- Navegação simplificada
- Página informativa sobre o projeto
- Melhor adaptação para dispositivos móveis

---

## Melhorias Futuras

- WebSockets para preços em tempo real
- Sistema de watchlist
- Mais criptomoedas
- Dockerização
- Testes automatizados
- Implementação de sistema de cache de preços (em memória ou Redis)
- Mecanismo de atualização periódica de preços via background jobs
- Otimização contínua para redução de chamadas externas e melhor gerenciamento de *rate limits*
- API própria
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
- Responsividade
- Estruturação de aplicações web em produção

Projeto desenvolvido como Final Project do **CS50x: Introduction to Computer Science** da Harvard University.

---

## Contato

**Diogo Zoboli**

- GitHub: https://github.com/zobolidiogo
- LinkedIn: https://linkedin.com/in/zobolidiogo

---

⭐ Se este projeto foi interessante para você, considere dar uma estrela no repositório.

*This was CS50!*