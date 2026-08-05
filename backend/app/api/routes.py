import json
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from sse_starlette.sse import EventSourceResponse

from app.api.schemas import AgentRunRequest, AgentRunResponse, AgentListResponse, AgentInfo, HealthResponse
from app.agents import get_researcher_agent, get_analyst_agent, get_writer_agent, get_coder_agent
from app.teams import get_research_and_writing_team, get_software_dev_team, get_router_team
from app.workflows import MarketReportWorkflow
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["Agno Multi-Agent API"])

# Registro centralizado de Agentes e Times disponíveis
def resolve_agent(agent_id: str, model_id: str = None):
    mapping = {
        "researcher": get_researcher_agent,
        "analyst": get_analyst_agent,
        "writer": get_writer_agent,
        "coder": get_coder_agent,
        "research_team": get_research_and_writing_team,
        "dev_team": get_software_dev_team,
        "router": get_router_team,
    }
    factory = mapping.get(agent_id.lower())
    if not factory:
        raise HTTPException(status_code=404, detail=f"Agente ou Equipe '{agent_id}' não encontrado. Disponíveis: {list(mapping.keys())}")
    return factory(model_id=model_id)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Protocolo de Health Check / Liveness probe.
    """
    return HealthResponse(
        status="healthy",
        environment=settings.ENV,
        version="1.0.0"
    )

@router.get("/agents", response_model=AgentListResponse)
async def list_agents():
    """
    Lista todos os Agentes e Equipes Multiagentes disponíveis no sistema.
    """
    agents = [
        AgentInfo(id="router", name="Roteador Inteligente", description="Roteia automaticamente a mensagem para a equipe ou agente mais qualificado.", type="multi_agent_team"),
        AgentInfo(id="research_team", name="Equipe de Pesquisa & Redação", description="Equipe composta por Pesquisador Web, Analista e Redator.", type="multi_agent_team"),
        AgentInfo(id="dev_team", name="Equipe de Desenvolvimento de Software", description="Equipe com Coder e Revisor de Código Sênior.", type="multi_agent_team"),
        AgentInfo(id="researcher", name="Agente Pesquisador", description="Pesquisa e busca notícias em tempo real na Web.", type="single_agent"),
        AgentInfo(id="analyst", name="Agente Analista de Dados", description="Análises quantitativas, código Python e finanças via YFinance.", type="single_agent"),
        AgentInfo(id="writer", name="Agente Redator Executivo", description="Síntese e redação de documentos corporativos em Markdown.", type="single_agent"),
        AgentInfo(id="coder", name="Agente Coder Principal", description="Geração e auditoria de código Python, TypeScript e SQL.", type="single_agent"),
    ]
    return AgentListResponse(agents=agents)

# ---------------------------------------------------------------------------
# 1. PROTOCOLO REST (Síncrono / Resposta Completa JSON)
# ---------------------------------------------------------------------------
@router.post("/agent/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest):
    """
    Protocolo REST HTTP POST para execução síncrona de agentes.
    Retorna o payload completo com resposta e metadados.
    """
    agent = resolve_agent(request.agent_id, request.model_id)
    session_id = request.session_id or f"session_{request.agent_id}"

    try:
        response = agent.run(request.message, stream=False)
        content = response.content if hasattr(response, 'content') else str(response)
        
        return AgentRunResponse(
            agent_id=request.agent_id,
            session_id=session_id,
            content=content,
            tool_calls=[]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução do agente: {str(e)}")

# ---------------------------------------------------------------------------
# 2. PROTOCOLO SSE (Server-Sent Events / Streaming HTTP)
# ---------------------------------------------------------------------------
@router.post("/agent/stream")
async def stream_agent(request: AgentRunRequest):
    """
    Protocolo SSE (Server-Sent Events) para transmissão em tempo real (chunk-by-chunk) da resposta do agente.
    """
    agent = resolve_agent(request.agent_id, request.model_id)

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            response_stream = agent.run(request.message, stream=True)
            for chunk in response_stream:
                chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
                if chunk_text:
                    data = json.dumps({"delta": chunk_text, "agent_id": request.agent_id})
                    yield f"data: {data}\n\n"
                    await asyncio.sleep(0.01)
            yield f"data: {json.dumps({'event': 'end'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return EventSourceResponse(event_generator())

# ---------------------------------------------------------------------------
# 3. PROTOCOLO WEBSOCKET (Comunicação Bidirecional em Tempo Real)
# ---------------------------------------------------------------------------
@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    Protocolo WebSocket Bidirecional para interação em tempo real com streaming e suporte a múltiplos turnos de conversa.
    
    Estrutura do payload recebido via WS:
    {
       "action": "send_message",
       "agent_id": "router",
       "message": "Qual é a cotação da Apple hoje?",
       "session_id": "ws_sess_123"
    }
    """
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            
            action = data.get("action", "send_message")
            agent_id = data.get("agent_id", "router")
            user_message = data.get("message", "")
            
            if not user_message:
                await websocket.send_json({"event": "error", "message": "Mensagem vazia."})
                continue
                
            agent = resolve_agent(agent_id)
            
            # Notifica início de resposta
            await websocket.send_json({"event": "start", "agent_id": agent_id})
            
            # Stream de tokens via WebSocket
            try:
                response_stream = agent.run(user_message, stream=True)
                for chunk in response_stream:
                    chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
                    if chunk_text:
                        await websocket.send_json({
                            "event": "delta",
                            "delta": chunk_text,
                            "agent_id": agent_id
                        })
                        await asyncio.sleep(0.01)
                
                await websocket.send_json({"event": "done", "agent_id": agent_id})
            except Exception as e:
                await websocket.send_json({"event": "error", "message": str(e)})

    except WebSocketDisconnect:
        print("Conexão WebSocket encerrada pelo cliente.")
    except Exception as e:
        print(f"Erro inesperado no WebSocket: {e}")
