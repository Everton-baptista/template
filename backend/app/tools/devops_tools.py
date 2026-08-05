from typing import List, Optional
from agno.tools.python import PythonTools
from app.core.config import settings

def get_python_tools() -> PythonTools:
    """Ferramenta de execução segura de código Python."""
    return PythonTools()

def get_shell_tools():
    """Ferramenta de execução de comandos Shell/Terminal."""
    try:
        from agno.tools.shell import ShellTools
        return ShellTools()
    except Exception as e:
        print(f"ShellTools indisponível: {e}")
        return None

def get_github_tools(access_token: Optional[str] = None):
    """Ferramenta de interação com repositórios, PRs e issues do GitHub."""
    target_token = access_token or getattr(settings, "GITHUB_TOKEN", None)
    if not target_token:
        return None
    try:
        from agno.tools.github import GithubTools
        return GithubTools(access_token=target_token)
    except Exception as e:
        print(f"GithubTools indisponível: {e}")
        return None

def get_devops_tools() -> List:
    """
    Retorna o conjunto consolidado de ferramentas de código, execução e DevOps.
    """
    tools = [get_python_tools()]
    
    shell_t = get_shell_tools()
    if shell_t:
        tools.append(shell_t)
        
    github_t = get_github_tools()
    if github_t:
        tools.append(github_t)

    return tools
