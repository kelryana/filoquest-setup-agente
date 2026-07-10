# Teste - Twine + IA

## 📂 Estrutura do Projeto

```text
filoquest-twine_teste/
├── docs/                     # Histórias exportadas do Twine e JSONs gerados
│   ├── strange_encounter.html
│   ├── passagens.json
│   └── embeddings.json
├── scripts/                  # Scripts Python principais
│   ├── agente_filosofo.py    # Agente que conversa com o Ollama
│   ├── api_agente.py         # API FastAPI para expor o agente
│   ├── extract_twine.py      # Extrai texto do HTML do Twine
│   └── twine_embeddings.py   # Gera embeddings da história
├── .gitignore                # Arquivos ignorados pelo Git
├── extract_twine.py          # (Raiz) Extrai texto do HTML do Twine
├── requirements.txt          # Dependências do projeto
├── teste_hf.py               # Teste de autenticação do Hugging Face
└── README.md                 # Este arquivo
```

## ⚙️ Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

1. **Python 3.12+** e o gerenciador de pacotes `pip`.
2. **Git** (para clonar o repositório).
3. **Ollama** (para rodar o modelo de IA localmente). Instale com:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

## 🚀 Como configurar o ambiente (Passo a passo)

### 1. Clone o repositório
```bash
git clone https://huggingface.co/aninnnha/filoquest-twine_teste
cd filoquest-twine_teste
```

### 2. Crie e ative um ambiente virtual (venv)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o token do Hugging Face
1. Crie um token em: `https://huggingface.co/settings/tokens`
2. No terminal, faça o login:
   ```bash
   hf auth login
   ```
3. Cole o token quando solicitado.


## 🧪 Como testar o projeto

### Teste 1: Verificar autenticação do Hugging Face
```bash
python3 teste_hf.py
```
**Resultado esperado:** Uma análise de sentimento (ex: `{'label': 'POSITIVE', 'score': 0.99}`).

### Teste 2: Extrair texto do Twine (gerar `passagens.json`)
```bash
python3 extract_twine.py
```
**Resultado esperado:** `✅ Extraídas 6 passagens do Twine` e o arquivo `docs/passagens.json` gerado.

### Teste 3: Gerar embeddings da história (gerar `embeddings.json`)
```bash
python3 scripts/twine_embeddings.py
```
**Resultado esperado:** `✅ Embeddings gerados para 6 passagens` e o arquivo `docs/embeddings.json` gerado.


## 🤖 Rodando o Agente Filósofo e a API

### Passo 1: Inicie o Ollama (em um terminal separado)
```bash
ollama serve
```
*(Se aparecer `address already in use`, o Ollama já está rodando.)*

### Passo 2: Baixe o modelo de IA (Qwen 2.5 3B)
```bash
ollama pull qwen2.5:3b
```

### Passo 3: Inicie a API do Agente Filósofo (em outro terminal)
```bash
cd scripts
python3 api_agente.py
```
**Saída esperada:** `Uvicorn running on http://0.0.0.0:8000`

### Passo 4: Teste a API no navegador
Abra `http://localhost:8000/docs` e clique em **POST /perguntar**. Digite uma pergunta filosófica no campo `texto` e veja a resposta.


## 🌐 Space no Hugging Face

O projeto também está hospedado em um **Space** no Hugging Face, onde você pode testar a busca por similaridade das passagens da história.

**Acesse:** `https://huggingface.co/spaces/aninnnha/filoquest-demo-estudo`


## 🛠️ Tecnologias Utilizadas

- **Linux Mint** (Sistema Operacional)
- **Python 3.12** (Linguagem)
- **Twine** (Narrativas interativas)
- **Hugging Face** (Modelos de IA e Embeddings)
- **Ollama + Qwen 2.5 3B** (Modelo de IA local)
- **FastAPI + Uvicorn** (API REST)
- **Gradio** (Interface web do Space)

---
