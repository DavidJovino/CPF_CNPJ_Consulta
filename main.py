#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import platform
from cpf.cpf_generator import validar_cpf, gerar_combinacoes_cpf
from cpf.consultar_cpf_api import consultar_cpf_api
from cnpj.cnpj_validator import validar_cnpj
from cnpj.consultar_cnpj_api import consultar_cnpj_api
from utils.exibir_dados import exibir_dados_cpf, exibir_dados_cnpj
from utils.formatadores import formatar_cpf, formatar_cnpj


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
                    with open("resultados_cpfs.txt", "a", encoding="utf-8") as out:
                        for cpf_valido in combinacoes:
                            print(f"  - {cpf_valido} (Válido)")
                            out.write(f"  - {cpf_valido} (Válido)\n")
                            dados = consultar_cpf_api(cpf_valido)
                            # imprime na tela
                            exibir_dados_cpf(dados)
                            # grava no arquivo
                            exibir_dados_cpf(dados, file=out)
                            _throttle() #Não sobrecarregar o API
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

