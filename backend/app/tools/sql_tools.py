from agno.tools.sql import SQLTools
from app.core.config import settings

def get_sql_tools(db_url: str = None):
    """
    Retorna ferramentas de execução e inspeção de banco de dados SQL.
    """
    target_url = db_url or settings.DATABASE_URL
    return SQLTools(db_url=target_url)
