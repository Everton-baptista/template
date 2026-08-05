from agno.tools.yfinance import YFinanceTools

def get_financial_tools():
    """
    Retorna ferramentas de análises financeiras e dados de mercado via YFinance.
    """
    return YFinanceTools(all=True)
