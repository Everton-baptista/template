from typing import List, Optional
from agno.tools.sql import SQLTools
from app.core.config import settings

def get_sql_tools(db_url: Optional[str] = None) -> SQLTools:
    """Ferramenta de inspeção e consultas SQL relacionais em banco de dados."""
    target_url = db_url or settings.DATABASE_URL
    return SQLTools(db_url=target_url)

def get_duckdb_tools():
    """Ferramenta de consultas analíticas ultrarrápidas em arquivos parquet/csv via DuckDB."""
    try:
        from agno.tools.duckdb import DuckDbTools
        return DuckDbTools()
    except Exception as e:
        print(f"DuckDbTools indisponível: {e}")
        return None

def get_pandas_tools():
    """Ferramenta de manipulação de DataFrames e dados tabulares via Pandas."""
    try:
        from agno.tools.pandas import PandasTools
        return PandasTools()
    except Exception as e:
        print(f"PandasTools indisponível: {e}")
        return None

def get_csv_tools():
    """Ferramenta de leitura e processamento de arquivos CSV."""
    try:
        from agno.tools.csv_toolkit import CsvTools
        return CsvTools()
    except Exception as e:
        print(f"CsvTools indisponível: {e}")
        return None

def get_data_tools() -> List:
    """
    Retorna o conjunto consolidado de ferramentas de análise de dados, SQL e arquivos tabulares.
    """
    tools = [get_sql_tools()]
    
    duck = get_duckdb_tools()
    if duck:
        tools.append(duck)
        
    pandas_t = get_pandas_tools()
    if pandas_t:
        tools.append(pandas_t)
        
    csv_t = get_csv_tools()
    if csv_t:
        tools.append(csv_t)

    return tools
