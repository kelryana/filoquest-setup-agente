# 🤖 Agente Filósofo & Processador de Narrativas Twine

Um projeto que combina **IA generativa** com **processamento de narrativas interativas**, permitindo criar um agente filósofo baseado em LLM e extrair/embeddings de histórias criadas no Twine.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias Usadas](#-tecnologias-usadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
  - [Agente Filósofo (CLI)](#-agente-filósofo-cli)
  - [API do Agente Filósofo](#-api-do-agente-filósofo)
  - [Extrator de Narrativas Twine](#-extrator-de-narrativas-twine)
  - [Gerador de Embeddings](#-gerador-de-embeddings)
  - [Busca Semântica](#-busca-semântica)
  - [Teste Hugging Face](#-teste-hugging-face)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🎯 Visão Geral

Este projeto oferece duas funcionalidades principais:

1. **Agente Filósofo**: Um chatbot baseado no modelo **Qwen 2.5 3B** (via Ollama) que responde perguntas de forma filosófica e didática. Disponível como script CLI ou API REST.

2. **Processador de Narrativas Twine**: Ferramentas para extrair texto de histórias interativas criadas no Twine, gerar embeddings semânticos e realizar buscas inteligentes nas passagens.

---

## 📁 Estrutura do Projeto

```
/workspace/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── teste_hf.py              # Script de teste do Hugging Face
├── extract_twine.py         # Script legado (raiz)
├── scripts/                 # Scripts principais do projeto
│   ├── agente_filosofo.py   # Agente filósofo via CLI
│   ├── api_agente.py        # API REST do agente filósofo
│   ├── extract_twine.py     # Extrator de narrativas Twine
│   ├── twine_embeddings.py  # Gerador de embeddings
│   └── testar_busca.py      # Teste de busca semântica
└── docs/                    # Arquivos de narrativas e dados
    ├── "Dilema do Bonde - Uma Jornada Etica.html"
    ├── "O Gabarito.html"
    ├── passagens.json       # (gerado) Passagens extraídas
    └── embeddings.json      # (gerado) Embeddings das passagens
```

---

## 🛠️ Tecnologias Usadas

### IA & Machine Learning
- **Ollama** - Runtime para modelos LLM locais
- **Qwen 2.5 3B** - Modelo de linguagem para o agente filósofo
- **Hugging Face Transformers** - Pipeline de NLP
- **Sentence-Transformers** - Geração de embeddings semânticos
- **all-MiniLM-L6-v2** - Modelo de embeddings leve e eficiente

### Backend & API
- **FastAPI** - Framework para criação da API REST
- **Uvicorn** - Servidor ASGI para rodar a API
- **Pydantic** - Validação de dados

### Processamento de Dados
- **BeautifulSoup4** - Parsing de HTML (Twine)
- **NumPy** - Operações numéricas e similaridade cosseno
- **Scikit-learn** - Utilitários de ML

### Outros
- **Python 3.8+**
- **CUDA Toolkit** - Suporte a GPU NVIDIA (opcional, para aceleração)

---

## 📦 Pré-requisitos

### 1. Python e Dependências
```bash
# Python 3.8 ou superior
python --version

# Instalar dependências
pip install -r requirements.txt
```

### 2. Ollama (para o Agente Filósofo)
O Ollama precisa estar instalado e rodando para usar os scripts do agente filósofo.

**Instalação do Ollama:**
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Baixe em https://ollama.com/download
```

**Baixar o modelo Qwen:**
```bash
ollama pull qwen2.5:3b
```

**Iniciar o servidor Ollama:**
```bash
ollama serve
```

> ⚠️ **Importante:** O Ollama deve estar rodando na porta `11434` para que os scripts funcionem.

### 3. Variáveis de Ambiente (Opcional)
Para usar funcionalidades do Hugging Face:
```bash
export HF_TOKEN='seu_token_aqui'
```

---

## 🚀 Instalação

1. **Clone o repositório** (se aplicável):
```bash
cd /workspace
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Verifique o Ollama**:
```bash
# Verificar se está instalado
ollama --version

# Listar modelos disponíveis
ollama list

# Se necessário, baixe o modelo
ollama pull qwen2.5:3b
```

---

## 📖 Como Usar

### 🧠 Agente Filósofo (CLI)

Script interativo que permite fazer perguntas diretamente no terminal.

**Execução:**
```bash
python scripts/agente_filosofo.py
```

**Uso:**
```
🤖 Agente Filósofo (Qwen 3B)
Digite 'sair' para encerrar.

🧠 Você: Qual o sentido da vida?
🤔 Pensando...
📚 Filósofo: [resposta do modelo]

🧠 Você: sair
```

---

### 🌐 API do Agente Filósofo

Servidor REST que expõe o agente filósofo como uma API.

**Iniciar o servidor:**
```bash
python scripts/api_agente.py
```

A API estará disponível em `http://localhost:8000`

**Endpoints:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Teste de saúde da API |
| POST | `/perguntar` | Enviar pergunta e receber resposta |

**Testar a API:**

1. Via navegador:
```
http://localhost:8000/
```

2. Via curl:
```bash
curl -X POST http://localhost:8000/perguntar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Qual é o propósito da existência?"}'
```

3. Via Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/perguntar",
    json={"texto": "O que é ética?"}
)
print(response.json())
```

**Resposta esperada:**
```json
{
  "pergunta": "O que é ética?",
  "resposta": "Ética é o ramo da filosofia que estuda..."
}
```

---

### 📚 Extrator de Narrativas Twine

Extrai todo o texto das passagens de um arquivo HTML exportado do Twine.

**Configuração:**
Edite o arquivo `scripts/extract_twine.py` e altere o caminho do arquivo HTML:
```python
html_path = "docs/Dilema do Bonde - Uma Jornada Etica.html"
```

**Execução:**
```bash
python scripts/extract_twine.py
```

**Saída:**
- Cria o arquivo `docs/passagens.json` com todas as passagens
- Exibe no terminal um resumo das passagens extraídas

**Formato do JSON gerado:**
```json
[
  {
    "nome": "Start",
    "texto": "Você está diante de um bonde desgovernado..."
  },
  ...
]
```

---

### 🔢 Gerador de Embeddings

Gera vetores de embeddings para cada passagem, permitindo busca semântica.

**Pré-requisito:** Ter executado o extrator primeiro (`passagens.json` deve existir).

**Execução:**
```bash
python scripts/twine_embeddings.py
```

**Saída:**
- Cria o arquivo `docs/embeddings.json` com os vetores
- Exibe dimensão dos embeddings e exemplo

**Formato do JSON gerado:**
```json
{
  "nomes": ["Start", "Path1", "Path2"],
  "embeddings": [
    [0.123, -0.456, 0.789, ...],
    ...
  ]
}
```

---

### 🔍 Busca Semântica

Testa a busca por similaridade entre textos e as passagens da narrativa.

**Pré-requisito:** Ter executado o gerador de embeddings primeiro.

**Execução:**
```bash
python scripts/testar_busca.py
```

**Exemplo de saída:**
```
🔍 'O que acontece se eu puxar a alavanca?' → Alavanca (similaridade: 0.8234)
🔍 'O homem gordo' → Ponte (similaridade: 0.7891)
🔍 'O bonde desgovernado' → Start (similaridade: 0.9012)
🔍 'Ética e moral' -> Dilema (similaridade: 0.7654)
```

---

### 🤗 Teste Hugging Face

Script simples para testar integração com Hugging Face usando análise de sentimento.

**Configurar token (opcional):**
```bash
export HF_TOKEN='hf_seu_token_aqui'
```

**Execução:**
```bash
python teste_hf.py
```

**Saída esperada:**
```
login no Hugging Face realizado com sucesso!
resultado: [{'label': 'POSITIVE', 'score': 0.9998}]
```

---

## 💡 Exemplos de Uso

### Cenário 1: Conversar com o Filósofo
```bash
# Inicie o Ollama primeiro
ollama serve

# Em outro terminal, rode o agente
python scripts/agente_filosofo.py

# Faça perguntas como:
# - "O que é justiça?"
# - "Explique o dilema do bonde"
# - "Qual a diferença entre ética e moral?"
```

### Cenário 2: API Integrada
```bash
# Inicie a API
python scripts/api_agente.py

# Em outro projeto, integre via HTTP
import requests

pergunta = "O utilitarismo justifica qualquer meio?"
resp = requests.post("http://localhost:8000/perguntar",
                     json={"texto": pergunta})
print(resp.json()["resposta"])
```

### Cenário 3: Analisar Narrativa Interativa
```bash
# 1. Extraia as passagens do HTML do Twine
python scripts/extract_twine.py

# 2. Gere embeddings para busca semântica
python scripts/twine_embeddings.py

# 3. Teste a busca
python scripts/testar_busca.py

# Agora você pode buscar conceitos na narrativa!
```

---

## 🧩 Fluxo de Trabalho Sugerido

Para usar o projeto completo:

1. **Agente Filósofo**:
   - Inicie Ollama → Execute `agente_filosofo.py` ou `api_agente.py`

2. **Processamento Twine**:
   - HTML → `extract_twine.py` → `passagens.json`
   - `passagens.json` → `twine_embeddings.py` → `embeddings.json`
   - `embeddings.json` → `testar_busca.py` → Busca semântica

---

## ⚠️ Troubleshooting

### Ollama não conecta
```bash
# Verifique se o serviço está rodando
ollama serve

# Teste a conexão
curl http://localhost:11434/api/tags
```

### Modelo não encontrado
```bash
# Baixe o modelo necessário
ollama pull qwen2.5:3b
```

### Erro de dependências
```bash
# Reinstale as dependências
pip install -r requirements.txt --upgrade
```

### CUDA/GPU não detectado
Os scripts funcionam sem GPU, mas mais lentamente. Para ativar:
- Verifique se os drivers NVIDIA estão instalados
- Confirme que `nvidia-smi` funciona
- O PyTorch já deve detectar automaticamente

### Arquivo HTML do Twine não encontrado
- Certifique-se de que o caminho no script `extract_twine.py` aponta para o arquivo correto
- Os arquivos de exemplo estão em `docs/`

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commitar suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abrir um Pull Request

---

## 📄 Licença

Este projeto está sob licença aberta. Sinta-se livre para usar, modificar e distribuir.

---

## 📞 Contato & Recursos

- **Ollama**: https://ollama.com
- **Qwen Model**: https://huggingface.co/Qwen
- **Twine**: https://twinery.org
- **Hugging Face**: https://huggingface.co
- **FastAPI**: https://fastapi.tiangolo.com
- **Sentence-Transformers**: https://www.sbert.net

---

<div align="center">

**Feito com ❤️ e muita filosofia**

⭐ Se gostou, deixe uma estrela!

</div>
