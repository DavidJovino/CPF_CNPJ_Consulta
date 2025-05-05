#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import time
import platform
from cpf_generator import validar_cpf, gerar_combinacoes_cpf
from cnpj_validator import validar_cnpj

BRASIL_API_BASE_URL = "https://brasilapi.com.br/api"

RATE_LIMIT = 3  # máximo de requisições por minuto para ReceitaWS (CNPJ)
_last_call = 0
_counter = 0

def _throttle():
    global _last_call, _counter
    now = time.time()
    # reset a cada 60s
    if now - _last_call > 60:
        _last_call, _counter = now, 0
    if _counter >= RATE_LIMIT:
        sleep_for = 60 - (now - _last_call)
        print(f"Ratelimit alcançado, aguardando {sleep_for:.0f}s...")
        time.sleep(sleep_for)
        _last_call, _counter = time.time(), 0
    _counter += 1


def limpar_terminal():
    """Limpa o terminal dependendo do sistema operacional."""
    if platform.system() == "Windows":
        import os
        os.system("cls")
    else:
        import os
        os.system("clear")

def formatar_cpf(cpf):
    """Formata um CPF no padrão XXX.XXX.XXX-XX."""
    cpf_limpo = re.sub(r"[^0-9]", "", cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf # Retorna original se não tiver 11 dígitos

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

def formatar_cnpj(cnpj):
    """Formata um CNPJ no padrão XX.XXX.XXX/XXXX-XX."""
    cnpj_limpo = re.sub(r"[^0-9]", "", cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj # Retorna original se não tiver 14 dígitos

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
    
def exibir_dados_cpf(dados):
    """Exibe os dados do CPF de forma organizada."""
    # Verifica se veio algum erro ou status de falha
    if not dados or dados.get('status') == 'error' or 'CPF' not in dados:
        print(f"Erro ao obter dados: {dados.get('msg', 'Nenhum dado retornado.')}")
        return

    print("\n--- Dados do CPF ---")
    # Assumindo que exista uma função formatar_cpf() semelhante ao formatar_cnpj()
    print(f"CPF: {formatar_cpf(dados.get('CPF', 'N/A'))}")
    print(f"Nome: {dados.get('NOME', 'N/A')}")
    print(f"Sexo: {dados.get('SEXO', 'N/A')}")
    print(f"Data de Nascimento: {dados.get('NASC', 'N/A')}")
    print(f"Nome da Mãe: {dados.get('NOME_MAE', 'N/A')}")
    print(f"RG: {dados.get('RG', 'N/A')}")
    print(f"Órgão Emissor: {dados.get('ORGAO_EMISSOR', 'N/A')} - {dados.get('UF_EMISSAO', 'N/A')}")
    print(f"CBO: {dados.get('CBO', 'N/A')}")
    # Formata renda, se existir
    renda = dados.get('RENDA')
    if renda and renda != "Não encontrado":
        # supondo que 'RENDA' já venha como string 'R$xxx,xx'
        print(f"Renda Informada: {renda}")
    else:
        print("Renda Informada: N/A")
    print(f"Título de Eleitor: {dados.get('TITULO_ELEITOR', 'N/A')}")
    print(f"CD Mosaic Antigo: {dados.get('CD_MOSAIC', 'N/A')}")
    print(f"CD Mosaic Novo: {dados.get('CD_MOSAIC_NOVO', 'N/A')}")
    print("---------------------")

def exibir_dados_cnpj(dados, file=None):
    """Exibe os dados do CNPJ de forma organizada."""

    # aponta para stdout se não vier file
    dest = file or sys.stdout

    if not dados or "erro" in dados:
        # Use single quotes for keys/defaults inside the f-string expression
        print(f"Erro ao obter dados: {dados.get('erro', 'Nenhum dado retornado.')}")
        return

    print("\n--- Dados do CNPJ ---")
    # Use single quotes for keys/defaults inside the f-string expression
    print(f"CNPJ: {formatar_cnpj(dados.get('cnpj', 'N/A'))}")
    print(f"Razão Social: {dados.get('razao_social', 'N/A')}")
    print(f"Nome Fantasia: {dados.get('nome_fantasia', 'N/A')}")
    print(f"Situação Cadastral: {dados.get('descricao_situacao_cadastral', 'N/A')}")
    print(f"Data Situação Cadastral: {dados.get('data_situacao_cadastral', 'N/A')}")
    print(f"Motivo Situação Cadastral: {dados.get('descricao_motivo_situacao_cadastral', 'N/A')}")
    print(f"Data Início Atividade: {dados.get('data_inicio_atividade', 'N/A')}")
    print(f"CNAE Fiscal Principal: {dados.get('cnae_fiscal', 'N/A')} - {dados.get('cnae_fiscal_descricao', 'N/A')}")

    # Use single quotes for keys/defaults inside the f-string expression
    endereco = f"{dados.get('descricao_tipo_logradouro', '')} {dados.get('logradouro', '')}, {dados.get('numero', 'S/N')}"
    complemento = dados.get('complemento')
    if complemento:
        endereco += f" - {complemento}"
    print(f"Endereço: {endereco}")
    print(f"Bairro: {dados.get('bairro', 'N/A')}")
    print(f"CEP: {dados.get('cep', 'N/A')}")
    print(f"Município: {dados.get('municipio', 'N/A')} - {dados.get('uf', 'N/A')}")
    print(f"Telefone: {dados.get('ddd_telefone_1', 'N/A')}")
    # Use single quotes for keys/defaults inside the f-string expression
    capital_social_str = f"{dados.get('capital_social', 0.0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"Capital Social: R$ {capital_social_str}")

    qsa = dados.get('qsa', [])
    if qsa:
        print("\n--- Quadro de Sócios e Administradores (QSA) ---")
        for socio in qsa:
            # Use single quotes for keys/defaults inside the f-string expression
            print(f"  Nome/Sócio: {socio.get('nome_socio', 'N/A')}")
            print(f"  Qualificação: {socio.get('qualificacao_socio', 'N/A')}")
            print("  ---")
    print("---------------------")

def main():
    limpar_terminal()
    print("Consulta de CPF/CNPJ")
    print("====================")
    print("AVISO: A consulta de dados detalhados de CPF diretamente na Receita Federal")
    print("não é publicamente disponível via API devido à LGPD.")
    print("Este programa valida CPFs, gera combinações para CPFs incompletos")
    print("e consulta dados públicos de CNPJs usando a BrasilAPI.")
    print("----------------------------------------------------------------------")

    while True:
        entrada = input("Digite o CPF (com ou sem máscara, use * para desconhecido) ou CNPJ (com ou sem máscara), ou \'sair\' para terminar: ")
        if entrada.lower() == 'sair':
            break

        entrada_limpa = re.sub(r"[^0-9*]", "", entrada)

        if "*" in entrada_limpa and len(entrada_limpa) == 11:
            # CPF Incompleto
            print(f"\nProcessando CPF incompleto: {entrada}")
            try:
                combinacoes = gerar_combinacoes_cpf(entrada)
                if combinacoes:
                    print(f"Encontradas {len(combinacoes)} combinações de CPF válidas:")
                    # Limitar a exibição e consulta se forem muitas combinações?
                    # Por enquanto, vamos listar todas.
                    with open("resultados_cpfs.txt", "a", encoding="utf-8") as out:
                        for cpf_valido in combinacoes:
                            print(f"  - {cpf_valido} (Válido)")
                            out.write(f"  - {cpf_valido} (Válido)\n")
                            dados = consultar_cpf_api(cpf_valido)
                            # imprime na tela
                            exibir_dados_cpf(dados)
                            # grava no arquivo
                            exibir_dados_cpf(dados, file=out)
                else:
                    print("Nenhuma combinação válida encontrada para o padrão informado.")
            except ValueError as e:
                print(f"Erro ao processar CPF incompleto: {e}")
            except Exception as e:
                 print(f"Erro inesperado ao gerar combinações: {e}")

        elif len(entrada_limpa) == 11:
            # CPF Completo
            cpf_formatado = formatar_cpf(entrada_limpa)
            print(f"\nVerificando CPF: {cpf_formatado}")
            if validar_cpf(entrada_limpa):
                print(f"CPF {cpf_formatado} é VÁLIDO.")
                dados = consultar_cpf_api(entrada_limpa)
                exibir_dados_cpf(dados)
            else:
                print(f"CPF {cpf_formatado} é INVÁLIDO.")

        elif len(entrada_limpa) == 14:
            # CNPJ
            cnpj_formatado = formatar_cnpj(entrada_limpa)
            print(f"\nConsultando CNPJ: {cnpj_formatado}")
            if validar_cnpj(entrada_limpa):
                print("CNPJ com formato válido. Consultando API...")
                dados = consultar_cnpj_api(entrada_limpa)
                exibir_dados_cnpj(dados)
            else:
                print(f"CNPJ {cnpj_formatado} é INVÁLIDO.")

        else:
            print("\nEntrada inválida. Por favor, digite um CPF (11 dígitos ou com *) ou CNPJ (14 dígitos) válido.")

        print("\n--------------------------------------------------")

    print("\nPrograma encerrado.")

if __name__ == "__main__":
    main()

