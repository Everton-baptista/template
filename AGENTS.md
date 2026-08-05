# Project Architecture & Standards Guide for AI Coding Agents

Welcome to the **Agno Multi-Agent Enterprise Template**. All AI coding assistants (Antigravity, Cursor, Claude Code, Windsurf, Aider, GitHub Copilot) working in this repository MUST comply with the following standards:

---

## 🏛️ Layer Boundaries

- `backend/app/agents/`: Single agent factories returning `agno.agent.Agent`.
- `backend/app/teams/`: Multi-agent team factories returning `agno.team.Team` using `members=[...]`.
- `backend/app/workflows/`: Hybrid pipelines extending `agno.workflow.Workflow`.
- `backend/app/tools/`: Custom and built-in tool definitions (`DuckDuckGoTools`, `YFinanceTools`, `SQLTools`, `PythonTools`, `FileTools`, `EnterpriseAPIToolkit`).
- `backend/app/storage/`: Database persistence layer (`PostgresDb`, `SqliteDb`).
- `backend/app/api/`: FastAPI layer offering **REST**, **SSE Streaming**, and **WebSockets**.
- `frontend/`: Next.js 14 App Router, TypeScript, Tailwind CSS, SSE + WS chat clients.

---

## 🚀 Agno 2.x Conventions

- Single agent: `from agno.agent import Agent`
- Multi-agent team: `from agno.team import Team` with `members=[agent1, agent2]`
- Database storage: `from agno.db.postgres import PostgresDb` and `from agno.db.sqlite import SqliteDb` using `session_table="..."`
- Model providers: `from agno.models.openai import OpenAIChat`, `from agno.models.anthropic import Claude`, etc.

---

## 🧪 Testing Requirement

Always verify code edits by running pytest:
```bash
cd backend && PYTHONPATH=. pytest tests/ -v
```
