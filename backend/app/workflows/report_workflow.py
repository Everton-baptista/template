from typing import Iterator
from agno.workflow import Workflow
from app.agents.researcher import get_researcher_agent
from app.agents.writer import get_writer_agent

class MarketReportWorkflow(Workflow):
    """
    Workflow estruturado de 2 etapas para geração automatizada de relatórios de mercado.
    Etapa 1: Pesquisa de mercado e notícias ativas.
    Etapa 2: Redação de relatório executivo formatado.
    """
    description: str = "Workflow determinístico de Pesquisa e Redação de Relatório de Mercado"

    def run(self, topic: str) -> Iterator[str]:
        researcher = get_researcher_agent()
        writer = get_writer_agent()

        yield f"### 🚀 Iniciando Workflow: {topic}\n\n"
        yield "🔎 **Etapa 1:** Coletando informações e dados atuais...\n\n"
        
        research_response = researcher.run(f"Pesquise detalhadamente sobre o tópico: {topic}")
        research_content = research_response.content if hasattr(research_response, 'content') else str(research_response)
        
        yield "✍️ **Etapa 2:** Redigindo relatório executivo sintético...\n\n"
        writer_prompt = f"Com base na seguinte pesquisa, elabore um relatório executivo em Markdown completo:\n\n{research_content}"
        
        writer_response = writer.run(writer_prompt)
        final_content = writer_response.content if hasattr(writer_response, 'content') else str(writer_response)
        
        yield final_content
