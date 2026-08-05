from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AgentRunRequest(BaseModel):
    message: str = Field(..., description="Mensagem ou instrução enviada ao agente/equipe", json_schema_extra={"example": "Pesquise sobre as últimas novidades de IA em 2026."})
    agent_id: str = Field(default="router", description="ID do agente ou equipe a ser executado (ex: researcher, analyst, writer, coder, research_team, dev_team, router)")
    session_id: Optional[str] = Field(default=None, description="ID único de sessão para manter memória de contexto")
    model_id: Optional[str] = Field(default=None, description="Sobrescreve o ID do modelo LLM para esta chamada (ex: gpt-4o, claude-3-5-sonnet-20241022)")
    stream: bool = Field(default=False, description="Indica se a resposta deve ser transmitida em formato streaming")

class AgentRunResponse(BaseModel):
    agent_id: str
    session_id: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

class AgentInfo(BaseModel):
    id: str
    name: str
    description: str
    type: str  # "single_agent" ou "multi_agent_team"

class AgentListResponse(BaseModel):
    agents: List[AgentInfo]

class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str
