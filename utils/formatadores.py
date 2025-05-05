import re

def formatar_cpf(cpf):
    """Formata um CPF no padrão XXX.XXX.XXX-XX."""
    cpf_limpo = re.sub(r"[^0-9]", "", cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf # Retorna original se não tiver 11 dígitos


def formatar_cnpj(cnpj):
    """Formata um CNPJ no padrão XX.XXX.XXX/XXXX-XX."""
    cnpj_limpo = re.sub(r"[^0-9]", "", cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj # Retorna original se não tiver 14 dígitos
