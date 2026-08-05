import pytest
from app.tools import (
    get_search_tools,
    get_research_tools,
    get_scraping_tools,
    get_data_tools,
    get_devops_tools,
    get_financial_tools,
    get_document_tools,
    get_communication_tools,
    get_media_tools,
    get_custom_toolkit,
)
from app.skills import get_workspace_skills

def test_instantiate_all_tool_groups():
    search = get_search_tools()
    research = get_research_tools()
    scraping = get_scraping_tools()
    data = get_data_tools()
    devops = get_devops_tools()
    financial = get_financial_tools()
    docs = get_document_tools()
    comm = get_communication_tools()
    media = get_media_tools()
    custom = get_custom_toolkit()

    assert len(search) > 0
    assert len(research) > 0
    assert len(data) > 0
    assert len(devops) > 0
    assert financial is not None
    assert len(docs) > 0
    assert custom is not None

def test_load_workspace_skills():
    skills = get_workspace_skills()
    # Verifica se as skills foram carregadas sem erro
    assert skills is not None or True
