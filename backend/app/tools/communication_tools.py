from typing import List, Optional
from app.core.config import settings

def get_slack_tools(bot_token: Optional[str] = None):
    """Ferramenta de envio de mensagens e interação com canais do Slack."""
    target_token = bot_token or getattr(settings, "SLACK_BOT_TOKEN", None)
    if not target_token:
        return None
    try:
        from agno.tools.slack import SlackTools
        return SlackTools(token=target_token)
    except Exception as e:
        print(f"SlackTools indisponível: {e}")
        return None

def get_discord_tools(bot_token: Optional[str] = None):
    """Ferramenta de envio de mensagens para servidores e canais do Discord."""
    target_token = bot_token or getattr(settings, "DISCORD_BOT_TOKEN", None)
    if not target_token:
        return None
    try:
        from agno.tools.discord import DiscordTools
        return DiscordTools(bot_token=target_token)
    except Exception as e:
        print(f"DiscordTools indisponível: {e}")
        return None

def get_email_tools():
    """Ferramenta de envio de e-mails formatados."""
    try:
        from agno.tools.email import EmailTools
        return EmailTools()
    except Exception as e:
        print(f"EmailTools indisponível: {e}")
        return None

def get_communication_tools() -> List:
    """
    Retorna o conjunto consolidado de ferramentas de comunicação e mensageria.
    """
    tools = []
    
    slack = get_slack_tools()
    if slack:
        tools.append(slack)
        
    discord = get_discord_tools()
    if discord:
        tools.append(discord)
        
    email = get_email_tools()
    if email:
        tools.append(email)

    return tools
