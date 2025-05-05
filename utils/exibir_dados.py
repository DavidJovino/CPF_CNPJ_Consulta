import sys
from utils.formatadores import formatar_cpf, formatar_cnpj

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
