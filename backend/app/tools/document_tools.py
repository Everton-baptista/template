from pathlib import Path
from typing import List
from agno.tools.file import FileTools

def get_file_tools(base_dir: str = ".") -> FileTools:
    """Ferramenta de leitura, escrita e manipulação de arquivos locais."""
    target_path = Path(base_dir) if base_dir else Path.cwd()
    return FileTools(base_dir=target_path)

def get_docling_tools():
    """Ferramenta avançada de conversão e parsing estruturado de documentos (PDF, DOCX, PPTX)."""
    try:
        from agno.tools.docling import DoclingTools
        return DoclingTools()
    except Exception as e:
        print(f"DoclingTools indisponível: {e}")
        return None

def get_document_tools() -> List:
    """
    Retorna o conjunto de ferramentas de manipulação de documentos e arquivos.
    """
    tools = [get_file_tools()]
    
    docling = get_docling_tools()
    if docling:
        tools.append(docling)

    return tools
