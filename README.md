# 🚀 Template Enterprise para Agentes e Multiagentes (Agno + FastAPI + Next.js)

Este é um template de projeto de nível de produção completo, robusto e infinitamente escalável para o desenvolvimento de **Agentes Inteligentes**, **Equipes Multiagentes**, **Workflows** e **Skills**, utilizando o framework **Agno** (`agno`), backend **FastAPI** de alta performance e frontend moderno **Next.js 14 / TypeScript** (além de playground em **Streamlit**).

---

## 📐 Arquitetura do Projeto

```text
/
├── backend/                  # Servidor Backend FastAPI & Agno Engine
│   ├── app/
│   │   ├── api/             # Protocols: REST, SSE (Streaming) & WebSockets (Bidirecional)
│   │   ├── agents/          # Agentes individuais (Researcher, Analyst, Writer, Coder)
│   │   ├── teams/           # Equipes Multiagentes (Manager / Router / Delegadores)
│   │   ├── workflows/       # Pipelines determinísticos (MarketReportWorkflow)
│   │   ├── skills/          # Gerenciamento de Skills locais e de workspace (LocalSkills)
│   │   ├── tools/           # Suíte de +30 Ferramentas em 9 Categorias Especializadas
│   │   ├── knowledge/       # Sistemas de RAG & PgVector Vector Store
│   │   ├── storage/         # Persistência de sessões no Postgres (PostgresDb) / SQLite (SqliteDb)
│   │   └── core/            # Configurações Pydantic, Logging e Conexões
│   └── tests/               # Suíte de testes unitários e de integração com Pytest
├── .agents/
│   └── skills/              # Skills prontas do workspace (code-review, web-research, data-analysis, executive-writing)
├── frontend/                # Aplicação Web Moderna (Next.js 14+ TypeScript + Tailwind + Lucide)
├── dashboard/               # Playground rápido para prototipagem em Streamlit
├── docker-compose.yml       # Orquestração completa dos serviços (Postgres PgVector + Backend + Frontend + Streamlit)
├── Makefile                 # Automação de tarefas de desenvolvimento
└── README.md
```

---

## 🛠️ Catálogo Completo de Ferramentas (9 Categorias)

O template já vem com 9 módulos de ferramentas prontas e configuradas em `backend/app/tools/`:
1. 🔍 **Pesquisa Avançada & Acadêmica (`research_tools.py`)**: `DuckDuckGoTools`, `ArxivTools`, `WikipediaTools`, `HackerNewsTools`, `TavilyTools`, `ExaTools`.
2. 🕸️ **Scraping & Extração Web (`scraping_tools.py`)**: `Newspaper4kTools`, `WebsiteTools`, `FirecrawlTools`.
3. 📊 **Dados, SQL & Analytics (`data_tools.py`)**: `SQLTools`, `DuckDbTools`, `PandasTools`, `CsvTools`.
4. ⚙️ **DevOps, Código & VCS (`devops_tools.py`)**: `PythonTools`, `ShellTools`, `GithubTools`.
5. 📈 **Finanças & Mercado (`financial_tools.py`)**: `YFinanceTools`.
6. 📄 **Documentos & Cloud (`document_tools.py`)**: `FileTools`, `DoclingTools`.
7. 💬 **Comunicação & Mensageria (`communication_tools.py`)**: `SlackTools`, `DiscordTools`, `EmailTools`.
8. 🎨 **Mídia & Imagens (`media_tools.py`)**: `DalleTools`, `YouTubeTools`.
9. ⚡ **Protocolo MCP Standard (`mcp_tools.py`)**: `MCPTools` para conexão universal com servidores MCP.

---

## 🧠 Sistema de Skills Integrado

O projeto possui suporte nativo a **Skills** para guiar o comportamento e metodologias dos agentes.
As melhores skills já estão prontas e configuradas em `.agents/skills/`:
- 🛡️ **`code-review`**: Auditoria OWASP, validação SOLID e refatoração DRY/KISS.
- 🔬 **`web-research`**: Triangulação de fontes, hierarquia de credibilidade e citação.
- 📈 **`data-analysis`**: Verificação de nulos, estatística descritiva e tabelas formatadas.
- 📝 **`executive-writing`**: Princípio da Pirâmide de Minto e redação C-Level em Markdown.

---

## 📡 Protocolos de Comunicação no FastAPI

1. **REST JSON Standard** (`POST /api/v1/agent/run`)
2. **SSE - Server-Sent Events** (`POST /api/v1/agent/stream`)
3. **WebSockets Bidirecionais** (`WS /api/v1/ws/chat`)

---

## ⚡ Como Rodar o Projeto

### Com Docker Compose
```bash
cp backend/.env.example backend/.env
make docker-up
```
- **Frontend (Next.js)**: [http://localhost:3000](http://localhost:3000)
- **Backend API (FastAPI Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Playground (Streamlit)**: [http://localhost:8501](http://localhost:8501)

### Execução Local para Desenvolvimento
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Rodando a Suíte de Testes

```bash
make test-backend
```
