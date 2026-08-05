from typing import List, Optional

def get_mcp_tools(server_command: Optional[str] = None):
    """
    Ferramenta de integração com o padrão Model Context Protocol (MCP).
    Permite conectar o agente a qualquer servidor MCP externo via stdio ou SSE.
    """
    if not server_command:
        return None
    try:
        from agno.tools.mcp import MCPTools
        return MCPTools(server_command=server_command)
    except Exception as e:
        print(f"MCPTools indisponível: {e}")
        return None
