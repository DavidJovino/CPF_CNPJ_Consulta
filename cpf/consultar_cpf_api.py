import requests

BRASIL_API_BASE_URL = "https://brasilapi.com.br/api"

def consultar_cpf_api(cpf: str) -> dict | None:
    """
    Consulta CPF em API pública “não-oficial”.
    (conforme seu trecho PHP usando https://api.centralda20.com/consultar/ )
    """
    url = f"{BRASIL_API_BASE_URL}/cpf/vi/{cpf}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        print(f"CPF {cpf} não encontrado ou sem dados.")
    except requests.RequestException as e:
        return {"status": "error", "msg": f"Erro HTTP ao consultar CPF {cpf}: {e}"}
    
        # tenta decodificar JSON
    try:
        data = resp.json()
    except ValueError:
        return {"status": "error", "msg": "Resposta da API não é um JSON válido."}

    # se a própria API sinaliza erro
    if data.get("status") == "error":
        return {"status": "error", "msg": data.get("msg", "CPF não encontrado.")}

    # sucesso
    data["status"] = "ok"
    return data