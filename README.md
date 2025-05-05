# Consulta de CPF e CNPJ

🚀 Projeto Python para consulta e validação de CPFs e CNPJs, com geração de combinações para CPFs incompletos e integração com APIs públicas.

## 📌 Funcionalidades

- ✅ Validação de CPFs e CNPJs
- 🔄 Geração de combinações válidas para CPFs com dígitos ocultos
- 🔍 Consulta de informações via API para CPFs e CNPJs
- 📄 Exibição formatada dos dados retornados
- ⏱️ Controle de *rate limit* para evitar bloqueios na API
- 🧼 Compatibilidade com Windows/Linux (limpeza de terminal automatizada)

## 🧠 Dica de Uso

Caso você **não saiba o número completo do CPF**, pode utilizar `*` nos dígitos desconhecidos (ex: `***.123.456-78`).
O programa irá calcular todas as combinações possíveis para os dígitos faltantes e consultar apenas os CPFs válidos.

⚠️ **Atenção:** A API de consulta de CPF **não está funcional atualmente** devido a restrições legais impostas pela Lei Geral de Proteção de Dados (LGPD).

## 📁 Estrutura do Projeto

```
CPF_Consulta/
├── main.py                  # Script principal
├── cpf/
│   ├── cpf_generator.py     # Validação e geração de CPFs
│   └── consultar_cpf_api.py # Consulta de CPFs em API
├── cnpj/
│   └── cnpj_validator.py    # Validação de CNPJs
│   └── consultar_cnpj_api.py # Consulta de CNPJ em API
├── utils/
│   └── exibir_dados.py      # Funções para exibir os dados formatados
└── .git/                    # Diretório de controle do Git
```

## 🧪 Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/CPF_Consulta.git
cd CPF_Consulta
```

### 2. Instalar dependências

Este projeto utiliza apenas bibliotecas padrão do Python (`requests`, `re`, `platform`, etc). Se necessário:

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
python3 main.py
```

## 📄 Licença

Este projeto está sob a licença MIT.