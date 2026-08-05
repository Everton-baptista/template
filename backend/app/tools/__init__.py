from app.tools.search_tools import get_search_tools
from app.tools.research_tools import get_research_tools, get_duckduckgo_tools, get_arxiv_tools, get_wikipedia_tools, get_hackernews_tools, get_tavily_tools, get_exa_tools
from app.tools.scraping_tools import get_scraping_tools, get_newspaper4k_tools, get_website_tools, get_firecrawl_tools
from app.tools.data_tools import get_data_tools, get_sql_tools, get_duckdb_tools, get_pandas_tools, get_csv_tools
from app.tools.devops_tools import get_devops_tools, get_python_tools, get_shell_tools, get_github_tools
from app.tools.financial_tools import get_financial_tools
from app.tools.document_tools import get_document_tools, get_file_tools, get_docling_tools
from app.tools.communication_tools import get_communication_tools, get_slack_tools, get_discord_tools, get_email_tools
from app.tools.media_tools import get_media_tools, get_dalle_tools, get_youtube_tools
from app.tools.mcp_tools import get_mcp_tools
from app.tools.custom_tools import get_custom_toolkit

__all__ = [
    # Consolidated groups
    "get_search_tools",
    "get_research_tools",
    "get_scraping_tools",
    "get_data_tools",
    "get_devops_tools",
    "get_financial_tools",
    "get_document_tools",
    "get_communication_tools",
    "get_media_tools",
    "get_mcp_tools",
    "get_custom_toolkit",
    # Specific tool factories
    "get_duckduckgo_tools",
    "get_arxiv_tools",
    "get_wikipedia_tools",
    "get_hackernews_tools",
    "get_tavily_tools",
    "get_exa_tools",
    "get_newspaper4k_tools",
    "get_website_tools",
    "get_firecrawl_tools",
    "get_sql_tools",
    "get_duckdb_tools",
    "get_pandas_tools",
    "get_csv_tools",
    "get_python_tools",
    "get_shell_tools",
    "get_github_tools",
    "get_file_tools",
    "get_docling_tools",
    "get_slack_tools",
    "get_discord_tools",
    "get_email_tools",
    "get_dalle_tools",
    "get_youtube_tools",
]
