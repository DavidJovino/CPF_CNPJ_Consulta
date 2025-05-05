import requests

BRASIL_API_BASE_URL = "https://brasilapi.com.br/api"

def consultar_cnpj_api(cnpj):
    """Consulta um CNPJ na BrasilAPI."""
    cnpj_limpo = re.sub(r"[^0-9]", "", cnpj)
    if not validar_cnpj(cnpj_limpo):
        return {"erro": "CNPJ inválido."}

    url = f"{BRASIL_API_BASE_URL}/cnpj/v1/{cnpj_limpo}"
    response = None # Inicializa response como None
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Lança exceção para erros HTTP (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Use single quotes for keys/defaults inside the f-string expression
        print(f"\nErro ao consultar API para CNPJ {formatar_cnpj(cnpj)}: {e}")
        if response is not None and response.status_code == 404:
             # Use single quotes for keys/defaults inside the f-string expression
             return {"erro": f"CNPJ {formatar_cnpj(cnpj)} não encontrado na base de dados."}
        return {"erro": f"Falha na comunicação com a API: {e}"}
    except Exception as e:
        # Use single quotes for keys/defaults inside the f-string expression
        print(f"\nErro inesperado ao processar CNPJ {formatar_cnpj(cnpj)}: {e}")
        return {"erro": f"Erro inesperado: {e}"}
 