from typing import List, Optional
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.embedder.openai import OpenAIEmbedder
from app.core.config import settings

def create_pdf_url_knowledge_base(urls: List[str], table_name: str = "pdf_documents") -> Optional[PDFUrlKnowledgeBase]:
    """
    Cria uma Base de Conhecimento (RAG) baseada em URLs de PDFs utilizando PgVector.
    """
    try:
        vector_db = PgVector(
            table_name=table_name,
            db_url=settings.VECTOR_DB_URL,
            embedder=OpenAIEmbedder()
        )
        knowledge_base = PDFUrlKnowledgeBase(
            urls=urls,
            vector_db=vector_db
        )
        return knowledge_base
    except Exception as e:
        print(f"Erro ao inicializar KnowledgeBase RAG: {e}")
        return None
