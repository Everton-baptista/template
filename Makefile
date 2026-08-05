.PHONY: help install-backend dev-backend dev-frontend dev-dashboard test-backend docker-up docker-down clean new-agent new-team new-skill

help:
	@echo "Comandos disponíveis no Template Enterprise Agno:"
	@echo "  make install-backend  - Instala dependências do backend usando pip"
	@echo "  make dev-backend      - Inicia o servidor backend (FastAPI) em modo recarga"
	@echo "  make dev-frontend     - Inicia o frontend (Next.js)"
	@echo "  make dev-dashboard    - Inicia o playground Streamlit"
	@echo "  make test-backend     - Executa a suíte de testes do backend"
	@echo "  make docker-up        - Sobe a infraestrutura completa no Docker Compose"
	@echo "  make docker-down      - Para todos os containers Docker"
	@echo "  make new-agent NAME=  - Gera um novo Agente (ex: make new-agent NAME=FinancialAdvisor)"
	@echo "  make new-team NAME=   - Gera uma nova Equipe Multiagente (ex: make new-team NAME=FinTechTeam)"
	@echo "  make new-skill NAME=  - Gera uma nova Skill (ex: make new-skill NAME=sentiment-analysis)"
	@echo "  make clean            - Limpa arquivos temporários e caches"

install-backend:
	cd backend && pip install -r requirements.txt

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev-dashboard:
	cd dashboard && streamlit run app.py

test-backend:
	cd backend && PYTHONPATH=. .venv/bin/pytest tests/ -v

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

new-agent:
	cd backend && python3 scripts/create_agent.py --name $(NAME)

new-team:
	cd backend && python3 scripts/create_team.py --name $(NAME)

new-skill:
	cd backend && python3 scripts/create_skill.py --name $(NAME)

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".next" -exec rm -r {} +
