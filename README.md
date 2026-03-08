# crypto.check: Simulador de Investimentos em Criptomoedas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

Plataforma web para simulação de investimentos em criptomoedas com dados de mercado em tempo real, desenvolvida como projeto final do CS50 (Harvard University).

## O Desafio

Criar uma aplicação web completa que permitisse aos usuários praticar investimentos em criptomoedas sem risco financeiro, integrando cotações reais de mercado, gerenciamento de portfólio, histórico de transações e visualização de dados através de uma interface intuitiva e responsiva.

---

## A Solução

Aplicação full-stack que simula uma exchange de criptomoedas, onde usuários iniciam com $10.000 virtuais e podem negociar 7 criptomoedas principais (Bitcoin, Ethereum, Tether, Solana, Cardano, XRP, Dogecoin) com preços atualizados em tempo real via APIs públicas.

### Funcionalidades Principais

**Sistema de Autenticação:**
- Registro com validação robusta (username 3-20 chars, senha 6-10 chars com requisitos de segurança)
- Login seguro com hash de senha (Werkzeug)
- Gerenciamento de sessões server-side (Flask-Session)

**Gestão de Portfolio:**
- Dashboard interativo mostrando todas as criptomoedas do usuário
- Cálculo automático de valor total (holdings + saldo disponível)
- Atualização de preços em tempo real
- Exibição de quantidade, preço unitário e valor total por ativo

**Sistema de Negociação:**
- Compra de criptomoedas com validação de saldo
- Venda de ativos com verificação de quantidade disponível
- Registro completo de todas as transações com timestamp
- Histórico detalhado (tipo, quantidade, preço, data)

**Análise de Mercado:**
- Lista de todas as criptomoedas disponíveis com preços atuais
- Página individual por cripto com gráfico de 30 dias
- Estatísticas: preço máximo e mínimo do período
- Visualização interativa (Chart.js)

**Integrações API:**
- CoinPaprika: cotações em tempo real
- CoinGecko: histórico de preços (30 dias)
- Tratamento robusto de erros e timeouts

---

## Arquitetura Técnica

### Backend (Flask + Python)

**app.py** - Aplicação principal com 9 rotas:
- `/register`, `/login`, `/logout` - Autenticação
- `/` - Portfolio
- `/market` - Lista de criptomoedas
- `/market/<crypto>` - Detalhes individuais com dashboard
- `/buy/<crypto>`, `/sell/<crypto>` - Transações
- `/history` - Histórico completo

**helpers.py** - Funções auxiliares:
- `crypto_price_now()` - Busca preço atual (CoinPaprika API)
- `crypto_history_format_day()` - Histórico 30 dias (CoinGecko API)
- `val_senha()`, `val_nome()` - Validações customizadas
- `usd()`, `brl()` - Formatação de moeda
- `login_required` - Decorator de autenticação
- `apology()` - Renderização de erros

### Banco de Dados (SQLite)

**T_USUARIO:**
- id_usuario (PK, autoincrement)
- nm_usuario (UNIQUE, NOT NULL)
- cd_hash (NOT NULL)
- qt_dinheiro (DEFAULT 10000)

**T_TRANSACAO:**
- id_transacao (PK, autoincrement)
- id_usuario (FK → T_USUARIO)
- nm_crypto (NOT NULL)
- qt_crypto (NOT NULL)
- vl_unitario_usd (NOT NULL)
- tp_transacao (CHECK: 'BUY' ou 'SELL')
- dt_transacao (DEFAULT CURRENT_TIMESTAMP)

**Design decisions:**
- Foreign keys habilitadas (`PRAGMA foreign_keys = ON`)
- Transações armazenadas individualmente (audit trail completo)
- Quantidade negativa para vendas (simplifica cálculos com SUM)
- CHECK constraint garantindo tipos válidos

### Frontend (HTML/CSS/JavaScript)

**Templates Jinja2:**
- `layout.html` - Base template (navbar + footer)
- `index.html` - Dashboard portfolio
- `market.html` - Lista de mercado
- `crypto.html` - Página individual com gráfico
- `buy.html`, `sell.html` - Formulários de transação
- `history.html` - Tabela de histórico
- `login.html`, `register.html` - Autenticação
- `apology.html` - Página de erros

**styles.css** - Design profissional:
- CSS Flexbox para layouts responsivos
- Paleta: navbar dark (#111827), accents blue (#2563eb)
- Cards para dashboard
- Tabelas hover effect
- Formulários consistentes

**chart.js** - Visualização de dados:
- Chart.js para gráfico de linha
- 30 dias de histórico de preços
- Labels de data no eixo X
- Preços no eixo Y
- Animação suave

---

## Decisões de Design

### Validação em Camadas

Implementei validação tanto no backend quanto no banco de dados:
- Backend: valida antes de processar (economiza recursos)
- Database: constraints garantem integridade mesmo se backend falhar
- UX: mensagens claras de erro via `apology()`

### Cálculo Dinâmico vs Cache

Optei por calcular portfolio em tempo real a cada request ao invés de cachear:
- **Vantagem:** Sempre atualizado com preços de mercado reais
- **Desvantagem:** Múltiplas chamadas API por página
- **Justificativa:** Precisão > performance para a aplicação educacional no momento

### Armazenamento de Transações

Escolhi armazenar transações individuais ao invés de saldo corrente:
- **Vantagem:** Histórico completo, audit trail, debugging fácil
- **Desvantagem:** Cálculos mais complexos (GROUP BY, SUM)
- **Justificativa:** Integridade de dados prioritária para app financeiro

### Limitação de Criptomoedas

7 criptos ao invés de catálogo completo:
- **Vantagem:** APIs mais confiáveis, testes mais fáceis, UX não sobrecarregada
- **Desvantagem:** Menor variedade
- **Justificativa:** Escopo adequado para projeto acadêmico, foco em qualidade

---

## Desafios e Aprendizados

### API Integration

**Desafio:** Coordenar chamadas assíncronas de API com rotas síncronas do Flask.

**Solução:** Implementei tratamento de exceções. Se API falhar, aplicação continua funcional mas informa o usuário.

**Aprendizado:** Sempre planejar para falhas de serviços externos.

### Concorrência em Transações

**Desafio:** Garantir que vendas simultâneas não resultassem em saldo negativo.

**Solução:** Constraints de banco de dados + validação pré-transação + foreign keys.

**Aprendizado:** Múltiplas camadas de validação são essenciais em apps financeiros.

### Data Visualization

**Desafio:** Processar dados de API (timestamps em milissegundos) para formato Chart.js.

**Solução:** Função `crypto_history_format_day()` que converte, agrupa por dia e formata.

**Aprendizado:** ETL (Extract, Transform, Load) é crítico mesmo em pequenos projetos.

### Segurança de Senhas

**Desafio:** Balancear segurança com usabilidade em validação de senhas.

**Solução:** Requisitos mínimos (6-10 chars, maiúscula + minúscula + número) sem caracteres especiais para simplicidade.

**Aprendizado:** Segurança deve ser forte mas não frustrar usuários.

---

## Estrutura de Arquivos
```
crypto_check/
├── app.py                  # Aplicação Flask principal (320 linhas)
├── helpers.py              # Funções auxiliares (140 linhas)
├── crypto.db               # Banco SQLite
├── requirements.txt        # Dependências Python
├── static/
│   ├── chart.js           # Config Chart.js
│   ├── styles.css         # CSS completo
│   └── favicon.ico        # Ícone
└── templates/
    ├── layout.html        # Template base
    ├── index.html         # Portfolio dashboard
    ├── market.html        # Lista mercado
    ├── crypto.html        # Página individual + gráfico
    ├── buy.html           # Formulário compra
    ├── sell.html          # Formulário venda
    ├── history.html       # Histórico transações
    ├── login.html         # Login
    ├── register.html      # Registro
    └── apology.html       # Erros
```

---

## Como Reproduzir o Projeto

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/zobolidiogo/crypto-check.git
cd crypto-check
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
flask run
```

4. Acesse no navegador:
```
http://127.0.0.1:5000
```

### Primeiro Uso

1. Clique em "Registrar" na navbar
2. Crie uma conta (username 3-20 chars, senha 6-10 chars)
3. Faça login
4. Explore o mercado (`/market`)
5. Compre sua primeira criptomoeda
6. Acompanhe seu portfolio na página inicial

---

## Tecnologias Utilizadas

**Backend:**
- Python 3.8
- Flask 2.0 - Framework web
- Flask-Session - Gerenciamento de sessões
- Werkzeug - Segurança (hashing de senhas)
- CS50 Library - SQL helper

**Database:**
- SQLite - Banco de dados relacional

**Frontend:**
- HTML5 - Estrutura
- CSS3 - Estilização (Flexbox)
- JavaScript (Vanilla) - Interatividade
- Jinja2 - Template engine
- Chart.js - Visualização de dados

**APIs Externas:**
- CoinPaprika API - Cotações em tempo real
- CoinGecko API - Histórico de preços

**Ferramentas:**
- Git/GitHub - Versionamento
- VS Code - Editor

---

## Diferenciais do Projeto

**Integração Dupla de APIs:**
- Combinação de 2 APIs diferentes para dados complementares
- CoinPaprika (snapshot atual) + CoinGecko (série temporal)
- Tratamento robusto de falhas

**Arquitetura em Camadas:**
- Separação clara: apresentação (templates), lógica (app.py), utilitários (helpers.py), dados (crypto.db)
- Código modular e reutilizável
- Manutenção facilitada

**Validação Completa:**
- Client-side (HTML5 attributes)
- Server-side (funções customizadas)
- Database-level (constraints)
- Mensagens de erro user-friendly

**Data Visualization:**
- Gráficos interativos com Chart.js
- Análise temporal (30 dias)
- Estatísticas de extremos (max/min)

**Design Profissional:**
- UI limpa e moderna
- Paleta de cores consistente
- Responsividade (Flexbox)
- Feedback visual (hover effects, loading states)

**Segurança:**
- Hashing de senhas (não plaintext)
- Sessões server-side
- Proteção de rotas (@login_required)
- Validação de inputs

---

## Melhorias Futuras

Se continuasse desenvolvendo este projeto:

**Features:**
- WebSocket para atualização de preços em tempo real (sem reload)
- Gráficos de performance de portfolio ao longo do tempo
- Watchlist (acompanhar cryptos sem comprar)
- Ordens limitadas (limit orders) e stop-loss
- Mais criptomoedas (integração dinâmica com API)
- Export de histórico (CSV/PDF)

**UX/UI:**
- Dark mode toggle
- Notificações de preço (alerts)
- Mobile-first redesign
- PWA (Progressive Web App)
- Animações de transição

**Técnico:**
- Migração para PostgreSQL (produção)
- Caching de preços (Redis)
- API própria (backend separado)
- Testes automatizados (pytest)
- CI/CD pipeline
- Dockerização

---

## Aprendizados CS50

Este projeto consolida conceitos de todas as 10 semanas do CS50:

- **Week 0-2 (C):** Lógica de programação, estruturas de controle
- **Week 3-5 (Algoritmos):** Eficiência, ordenação (histórico de transações)
- **Week 6 (Python):** Linguagem principal do backend
- **Week 7 (SQL):** Modelagem de dados, queries complexas (JOIN, GROUP BY)
- **Week 8 (HTML/CSS/JS):** Frontend completo
- **Week 9 (Flask):** Framework web, rotas, templates
- **Week 10 (Final Project):** Integração de todos os conceitos

**Habilidades demonstradas:**
- Full-stack development
- Database design e normalização
- API integration
- Autenticação e segurança
- Data visualization
- Error handling
- Code organization

Projeto desenvolvido como Final Project do **CS50x: Introduction to Computer Science** (Harvard University, 2026).

---

## Contato

**Diogo Zoboli**

zobolidiogo@gmail.com

LinkedIn: [linkedin.com/in/zobolidiogo](https://linkedin.com/in/zobolidiogo)

GitHub: [github.com/zobolidiogo](https://github.com/zobolidiogo)

---

**Se este projeto foi útil, considere dar uma ⭐ no repositório!**

---

*This was CS50!*
