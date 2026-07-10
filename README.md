# 🤖 Agente Filósofo & Sistema de Busca Semântica Filosófica

Um projeto completo que combina **IA generativa** com **processamento de narrativas interativas** e **sistema de busca semântica RAG**, permitindo criar um agente filósofo baseado em LLM, extrair embeddings de textos filosóficos e realizar buscas inteligentes por similaridade semântica.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias Usadas](#-tecnologias-usadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
  - [Preparação dos Dados](#-preparação-dos-dados)
  - [Geração de Embeddings](#-geração-de-embeddings)
  - [Busca Filosófica (RAG/GREP/Híbrida)](#-busca-filosófica-raggrephíbrida)
  - [Validação e Benchmark](#-validação-e-benchmark)
  - [Geração de Relatório](#-geração-de-relatório)
  - [Agente Filósofo (CLI)](#-agente-filósofo-cli)
  - [API do Agente Filósofo](#-api-do-agente-filósofo)
  - [Extrator de Narrativas Twine](#-extrator-de-narrativas-twine)
  - [Frontend Web](#-frontend-web)
- [Fluxo de Trabalho Completo](#-fluxo-de-trabalho-completo)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🎯 Visão Geral

Este projeto oferece múltiplas funcionalidades integradas:

1. **Processamento de Textos Filosóficos**: Pipeline completo para carregar, fatiar e gerar embeddings de textos filosóficos clássicos (Aristóteles, Kant, Bentham).

2. **Sistema de Busca Semântica**: Três métodos de busca implementados:
   - **RAG (Retrieval-Augmented Generation)**: Busca por similaridade de cosseno usando embeddings
   - **GREP**: Busca por palavras-chave exatas
   - **Híbrida**: Combinação ponderada de RAG + GREP

3. **Agente Filósofo**: Chatbot baseado no modelo **Qwen 2.5 3B** (via Ollama) que responde perguntas de forma filosófica e didática. Disponível como CLI ou API REST.

4. **Validação e Benchmark**: Sistema de validação com gabarito para medir acurácia e tempo de resposta dos diferentes métodos de busca.

5. **Processador de Narrativas Twine**: Ferramentas para extrair texto de histórias interativas criadas no Twine e gerar embeddings.

6. **Frontend Web**: Interface web moderna para interação com o sistema de busca.

---

## 📁 Estrutura do Projeto

```
/workspace/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── teste_hf.py              # Script de teste do Hugging Face
├── extract_twine.py         # Script legado (raiz)
├── frontend/                # Interface web
│   ├── index.html          # Página principal
│   ├── style.css           # Estilos CSS
│   └── script.js           # Lógica JavaScript
├── scripts/                 # Scripts principais do projeto
│   ├── preparar_dados.py    # Fatiamento de textos filosóficos
│   ├── gerar_embeddings.py  # Geração de embeddings semânticos
│   ├── busca_filosofica.py  # Sistema de busca (RAG/GREP/Híbrida)
│   ├── validar_buscas.py    # Validação e benchmark
│   ├── gerar_relatorio.py   # Geração de relatório HTML
│   ├── agente_filosofo.py   # Agente filósofo via CLI
│   ├── api_agente.py        # API REST do agente filósofo
│   ├── extract_twine.py     # Extrator de narrativas Twine
│   ├── twine_embeddings.py  # Gerador de embeddings para Twine
│   └── testar_busca.py      # Teste simples de busca semântica
└── docs/                    # Arquivos de dados e narrativas
    ├── Textos originais:
    │   ├── aristoteles_etica-e-nicomaco.txt
    │   ├── kant_metafisica-costumes.txt
    │   └── jeremy_utilitarismo.txt
    ├── Narrativas Twine:
    │   ├── "Dilema do Bonde - Uma Jornada Etica.html"
    │   └── "O Gabarito.html"
    ├── Dados processados:
    │   ├── base_filosofica.json       # Base de conhecimento
    │   ├── texto_filosofico_fatiado.json  # Chunks de texto
    │   ├── embeddings_filosofia.json  # Embeddings gerados
    │   └── resultados_validacao.json  # Resultados do benchmark
    └── Relatórios:
        └── relatorio_benchmark.html   # Relatório visual
```

---

## 🛠️ Tecnologias Usadas

### IA & Machine Learning
- **Ollama** - Runtime para modelos LLM locais
- **Qwen 2.5 3B** - Modelo de linguagem para o agente filósofo
- **Hugging Face Transformers** - Pipeline de NLP
- **Sentence-Transformers** - Geração de embeddings semânticos
- **all-MiniLM-L6-v2** - Modelo de embeddings leve e eficiente
- **PyTorch** - Backend para inferência de modelos (com suporte a CUDA)

### Backend & API
- **FastAPI** - Framework para criação da API REST
- **Uvicorn** - Servidor ASGI para rodar a API
- **Pydantic** - Validação de dados

### Processamento de Dados
- **BeautifulSoup4** - Parsing de HTML (Twine)
- **NumPy** - Operações numéricas e similaridade cosseno
- **Scikit-learn** - Utilitários de ML
- **JSON** - Armazenamento estruturado de dados

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript (Vanilla)** - Lógica do cliente
- **Chart.js** - Visualização de dados nos relatórios

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

### 📊 Preparação dos Dados

Primeiro, é necessário fatiar os textos filosóficos em chunks menores para processamento.

**Execução:**
```bash
python scripts/preparar_dados.py
```

**O que faz:**
- Lê os arquivos de texto em `docs/` (Aristóteles, Kant, Bentham)
- Divide o texto em chunks de ~150 palavras
- Salva o resultado em `docs/texto_filosofico_fatiado.json`

**Formato do JSON gerado:**
```json
[
  {
    "chunk_id": 0,
    "text": "A ética a Nicômaco é uma obra...",
    "source_file": "aristoteles_etica-e-nicomaco.txt",
    "char_count": 450,
    "word_count": 78
  },
  ...
]
```

---

### 🔢 Geração de Embeddings

Gera vetores de embeddings semânticos para cada chunk de texto.

**Pré-requisito:** Ter executado `preparar_dados.py` primeiro.

**Execução:**
```bash
python scripts/gerar_embeddings.py
```

**O que faz:**
- Carrega o modelo `all-MiniLM-L6-v2`
- Gera embeddings para cada chunk de texto
- Salva os vetores em `docs/embeddings_filosofia.json`

**Saída esperada:**
```
Carregando modelo: all-MiniLM-L6-v2
🔧 Usando dispositivo: CPU
Modelo carregado com sucesso: all-MiniLM-L6-v2 (dimensão do embedding: 384)
Gerando embeddings para 342 chunks...

Resumo:
  - Dimensão dos embeddings: 384
  - Total de embeddings: 342
  - Tamanho do arquivo: 1.84 MB
```

---

### 🔍 Busca Filosófica (RAG/GREP/Híbrida)

Sistema de busca com três métodos diferentes.

**Execução:**
```bash
python scripts/busca_filosofica.py
```

**Métodos de busca:**

| Método | Descrição | Melhor para |
|--------|-----------|-------------|
| **RAG** | Similaridade de cosseno com embeddings | Buscas conceituais, sinônimos |
| **GREP** | Busca exata por palavras-chave | Termos específicos, citações |
| **Híbrida** | Combinação ponderada (RAG + GREP) | Melhor dos dois mundos |

**Exemplo de uso no código:**
```python
from scripts.busca_filosofica import BuscaFilosofica

busca = BuscaFilosofica('embeddings_filosofia.json')

# Busca RAG
resultados = busca.busca_rag('O que é justiça?', top_k=3)

# Busca GREP
resultados = busca.busca_grep('lei universal', top_k=3)

# Busca Híbrida (alpha=0.7 dá 70% de peso para RAG)
resultados = busca.busca_hibrida('ética kantiana', top_k=3, alpha=0.7)
```

---

### ✅ Validação e Benchmark

Valida a acurácia dos métodos de busca usando um gabarito.

**Pré-requisito:** Ter executado `gerar_embeddings.py` primeiro.

**Execução:**
```bash
python scripts/validar_buscas.py
```

**O que faz:**
- Executa perguntas de teste nos 3 métodos
- Compara resultados com o gabarito (`docs/O Gabarito.html`)
- Mede tempo de resposta e acurácia
- Salva resultados em `docs/resultados_validacao.json`

**Métricas coletadas:**
- Taxa de acerto por método
- Tempo médio de resposta
- Ranking de chunks retornados

---

### 📈 Geração de Relatório

Gera um relatório HTML visual com os resultados do benchmark.

**Pré-requisito:** Ter executado `validar_buscas.py` primeiro.

**Execução:**
```bash
python scripts/gerar_relatorio.py
```

**Saída:**
- Cria `docs/relatorio_benchmark.html`
- Gráficos comparativos com Chart.js
- Tabelas com métricas detalhadas

**Para visualizar:**
```bash
# Abra no navegador
xdg-open docs/relatorio_benchmark.html  # Linux
open docs/relatorio_benchmark.html      # Mac
start docs/relatorio_benchmark.html     # Windows
```

---

### 🧠 Agente Filósofo (CLI)

Script interativo que permite fazer perguntas diretamente no terminal.

**Pré-requisito:** Ollama instalado e rodando com o modelo Qwen.

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

1. Via navegador (Swagger UI):
```
Acesse: http://localhost:8000/docs
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

### 🔢 Gerador de Embeddings (Twine)

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

### 🌐 Frontend Web

Interface web moderna para interação com o sistema de busca.

**Pré-requisito:** Ter executado todo o pipeline de processamento dos dados.

**Como usar:**
1. Abra o arquivo `frontend/index.html` em um navegador moderno
2. Digite perguntas ou termos filosóficos na barra de busca
3. Visualize os resultados com as similaridades

**Funcionalidades:**
- Interface responsiva e moderna
- Busca em tempo real
- Exibição de chunks relevantes com destaque
- Comparação visual dos métodos de busca

---

## 🔬 Fluxo de Trabalho Completo

### Pipeline Principal (Textos Filosóficos)

```
1. preparar_dados.py → texto_filosofico_fatiado.json
2. gerar_embeddings.py → embeddings_filosofia.json
3. validar_buscas.py → resultados_validacao.json
4. gerar_relatorio.py → relatorio_benchmark.html
5. (Opcional) frontend/index.html → Interface web
```

### Pipeline Twine (Narrativas Interativas)

```
1. extract_twine.py → passagens.json
2. twine_embeddings.py → embeddings.json
3. testar_busca.py → Teste de busca semântica
```

### Agente Filósofo

```
1. ollama serve (iniciar serviço)
2. agente_filosofo.py (CLI) OU api_agente.py (API REST)
```

---

## ⚠️ Troubleshooting -- erros que voce pode identificar

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

### Embeddings não gerados
- Execute `preparar_dados.py` antes de `gerar_embeddings.py`
- Verifique se `texto_filosofico_fatiado.json` existe em `docs/`

### Erro de memória ao gerar embeddings
- Reduza o batch size no script `gerar_embeddings.py`
- Use `device='cpu'` se estiver com pouca VRAM na GPU

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

## 🔗 Recursos

- **Ollama**: https://ollama.com
- **Qwen Model**: https://huggingface.co/Qwen
- **Twine**: https://twinery.org
- **Hugging Face**: https://huggingface.co
- **FastAPI**: https://fastapi.tiangolo.com
- **Sentence-Transformers**: https://www.sbert.net
- **Chart.js**: https://www.chartjs.org
- **PyTorch**: https://pytorch.org

---

## 📊 Dados de Exemplo

O projeto já inclui dados processados prontos para uso:

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `texto_filosofico_fatiado.json` | 342 chunks de textos filosóficos | ~171 KB |
| `embeddings_filosofia.json` | Embeddings gerados (384 dimensões) | ~1.9 MB |
| `resultados_validacao.json` | Resultados do benchmark | ~3 KB |
| `relatorio_benchmark.html` | Relatório visual interativo | ~9 KB |

**Textos originais incluídos:**
- Aristóteles: *Ética a Nicômaco*
- Immanuel Kant: *Fundamentação da Metafísica dos Costumes*
- Jeremy Bentham: *Princípios de Moral e Legislação*

---

## 🎯 Próximos Passos Sugeridos

1. **Teste o pipeline completo:**
   ```bash
   python scripts/preparar_dados.py
   python scripts/gerar_embeddings.py
   python scripts/validar_buscas.py
   python scripts/gerar_relatorio.py
   ```

2. **Explore o relatório:** Abra `docs/relatorio_benchmark.html` no navegador

3. **Experimente o agente filósofo:**
   ```bash
   ollama serve  # Em um terminal
   python scripts/agente_filosofo.py  # Em outro
   ```

4. **Use o frontend:** Abra `frontend/index.html` no navegador

---
