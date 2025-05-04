import re
import itertools

def validar_cpf(cpf):
    """Valida um número de CPF."""
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = (soma * 10) % 11
    digito1 = resto if resto < 10 else 0

    if digito1 != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = (soma * 10) % 11
    digito2 = resto if resto < 10 else 0

    return digito2 == int(cpf[11])

def gerar_combinacoes_cpf(cpf_incompleto):
    """Gera combinações válidas para um CPF incompleto com asteriscos."""
    cpf_incompleto = re.sub(r'[^0-9*]', '', cpf_incompleto)
    if len(cpf_incompleto) != 11:
        raise ValueError("Formato de CPF incompleto inválido. Deve ter 11 caracteres (dígitos ou '*').")

    posicoes_asterisco = [i for i, char in enumerate(cpf_incompleto) if char == '*']
    num_asteriscos = len(posicoes_asterisco)

    if num_asteriscos == 0:
        if validar_cpf(cpf_incompleto):
            return [cpf_incompleto]
        else:
            return []

    cpfs_validos = []
    # Usar itertools.product para gerar combinações de dígitos
    for combinacao in itertools.product('0123456789', repeat=num_asteriscos):
        cpf_lista = list(cpf_incompleto)
        for i, pos in enumerate(posicoes_asterisco):
            cpf_lista[pos] = combinacao[i]
        cpf_candidato = "".join(cpf_lista)

        if validar_cpf(cpf_candidato):
            # Formata o CPF válido
            cpf_formatado = f"{cpf_candidato[:3]}.{cpf_candidato[3:6]}.{cpf_candidato[6:9]}-{cpf_candidato[9:]}"
            cpfs_validos.append(cpf_formatado)

    return cpfs_validos

# Exemplo de uso (pode ser removido ou comentado na versão final)
# cpf_teste = '***.123.456-**'
# try:
#     combinacoes = gerar_combinacoes_cpf(cpf_teste)
#     print(f"Combinações válidas para {cpf_teste}:")
#     if combinacoes:
#         for cpf in combinacoes:
#             print(cpf)
#     else:
#         print("Nenhuma combinação válida encontrada.")
# except ValueError as e:
#     print(f"Erro: {e}")

