import re

def validar_cnpj(cnpj):
    """Valida um número de CNPJ."""
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * pesos[i]
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if digito1 != int(cnpj[12]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        soma += int(cnpj[i]) * pesos[i]
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return digito2 == int(cnpj[13])

# Exemplo de uso 
# cnpj_teste = "11.444.777/0001-61" # Exemplo válido
# print(f"CNPJ {cnpj_teste} é válido? {validar_cnpj(cnpj_teste)}")
# cnpj_teste_inv = "11.444.777/0001-60" # Exemplo inválido
# print(f"CNPJ {cnpj_teste_inv} é válido? {validar_cnpj(cnpj_teste_inv)}")

