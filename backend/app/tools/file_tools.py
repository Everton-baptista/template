from pathlib import Path
from agno.tools.file import FileTools

def get_file_tools(base_dir: str = "."):
    """
    Retorna ferramentas de leitura, escrita e manipulação de arquivos locais.
    """
    target_path = Path(base_dir) if base_dir else Path.cwd()
    return FileTools(base_dir=target_path)
