from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from app.core.config import settings

def get_agent_storage(table_name: str = "agent_sessions"):
    """
    Retorna uma instância de banco de dados persistente (db) para histórico e estados do agente.
    Utiliza PostgresDb se disponível ou SqliteDb como fallback local.
    """
    try:
        if settings.DATABASE_URL.startswith("postgresql"):
            return PostgresDb(
                session_table=table_name,
                db_url=settings.DATABASE_URL
            )
    except Exception as e:
        print(f"Postgres DB indisponível, usando SqliteDb local: {e}")

    return SqliteDb(
        session_table=table_name,
        db_file="storage.db"
    )
