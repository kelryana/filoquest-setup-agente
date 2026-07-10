##scripts/api_agente.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

# Cria a aplicação FastAPI
app = FastAPI(title="Agente Filósofo API")

# Configura CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Define o formato da pergunta que a API vai receber
class Pergunta(BaseModel):
    texto: str

def perguntar_ao_filosofo(pergunta: str) -> str:
    
    url = "http://localhost:11434/api/generate"

    # Dá uma "personalidade" de filósofo para o modelo
    prompt = f"""Você é um filósofo. Responda à pergunta de forma clara e didática:

Pergunta: {pergunta}

Resposta:"""

    payload = {
        "model": "qwen2.5:3b",  # O modelo que você baixou
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.ConnectionError:
        return "❌ Erro: O Ollama não está rodando. Execute 'ollama serve' em outro terminal."
    except Exception as e:
        return f"❌ Erro: {str(e)}"

# Rota raiz (só para testar se a API está no ar)
@app.get("/")
def root():
    return {"mensagem": "API do Agente Filósofo. Use POST /perguntar com JSON: {'texto': 'sua pergunta'}"}

# Rota principal: recebe a pergunta e devolve a resposta
@app.post("/perguntar")
def responder(pergunta: Pergunta):
    resposta = perguntar_ao_filosofo(pergunta.texto)
    return {"pergunta": pergunta.texto, "resposta": resposta}

# Só roda o servidor se executar este arquivo diretamente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
