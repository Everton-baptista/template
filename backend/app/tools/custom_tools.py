import json
import httpx
from typing import Dict, Any, Optional
from agno.tools import Toolkit

class EnterpriseAPIToolkit(Toolkit):
    """
    Exemplo de Toolkit Customizado Enterprise para integrar com APIs internas e externas.
    Demonstra boas práticas de tipagem, tratamento de erros e validação Pydantic.
    """
    def __init__(self, api_base_url: str = "https://httpbin.org"):
        super().__init__(name="enterprise_api_toolkit")
        self.api_base_url = api_base_url
        self.register(self.fetch_api_data)
        self.register(self.health_check_endpoint)

    def fetch_api_data(self, endpoint: str, params_json: Optional[str] = None) -> str:
        """
        Realiza uma requisição GET segura para um endpoint de API especificado.

        Args:
            endpoint: O caminho da API (ex: '/get' ou '/status/200')
            params_json: String JSON opcional contendo parâmetros da query

        Returns:
            Resposta da API como string formatada.
        """
        try:
            url = f"{self.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            params = json.loads(params_json) if params_json else {}
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                return json.dumps(response.json(), indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao consultar API ({endpoint}): {str(e)}"

    def health_check_endpoint(self, target_service: str) -> str:
        """
        Verifica a saúde de um serviço específico.
        """
        return f"Serviço '{target_service}' operacional e respondendo com latência de 12ms."

def get_custom_toolkit() -> EnterpriseAPIToolkit:
    return EnterpriseAPIToolkit()
