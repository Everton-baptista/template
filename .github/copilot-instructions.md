# GitHub Copilot Instructions for Agno Multi-Agent Template

This workspace contains an enterprise template for Agno Multi-Agent systems:
- Backend: FastAPI + Agno 2.x + Pydantic v2 + SQLAlchemy + PgVector + Pytest.
- Protocols: REST JSON (`/agent/run`), SSE Streaming (`/agent/stream`), WebSockets (`/ws/chat`).
- Frontend: Next.js 14 App Router, TypeScript, Tailwind CSS.
- Dashboard: Streamlit playground in `dashboard/app.py`.
- Architectural rules are defined in `AGENTS.md` and `.agents/AGENTS.md`.
