from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn
import sys
import logging
from pathlib import Path

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório scripts ao path para importar busca_filosofica
sys.path.insert(0, str(Path(__file__).parent))

# Importa a sua classe de busca
from busca_filosofica import BuscaFilosofica

# Cria a aplicação FastAPI
app = FastAPI(title="Agente Filósofo API")

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar o buscador uma única vez (Verifica se o arquivo existe)
logger.info("🔍 Inicializando buscador filosófico...")
try:
    buscador = BuscaFilosofica('embeddings_filosofia.json')
    logger.info("✅ Buscador inicializado com sucesso!")
except Exception as e:
    logger.warning(f"⚠️ Aviso: Buscador não pôde ser inicializado: {e}")
    buscador = None

# Define o formato da pergunta
class Pergunta(BaseModel):
    texto: str

def perguntar_ao_filosofo(pergunta: str, contexto: str = None) -> str:
    url = "http://localhost:11434/api/generate"

    if contexto:
        prompt = f"""Você é um filósofo especialista em ética e filosofia moral.

Você teve acesso a textos filosóficos relevantes para embasar seu conhecimento.
Use o conteúdo desses textos para formar sua resposta, mas responda com suas próprias palavras, de forma natural, clara e didática, como se você tivesse estudado o assunto há anos. Não copie os textos literalmente.
Use o seguinte contexto para responder:

{contexto}

Pergunta: {pergunta}

Resposta:"""
    else:
        prompt = f"""Você é um filósofo. Responda à pergunta de forma clara e didática:

Pergunta: {pergunta}

Resposta:"""

    payload = {
        "model": "qwen2.5:3b",
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

@app.get("/")
def root():
    return {"mensagem": "API do Agente Filósofo. Use POST /perguntar com JSON: {'texto': 'sua pergunta'}"}

@app.post("/perguntar")
def responder(pergunta: Pergunta):
    contexto = ""
    resultados_busca = []

    if buscador:
        try:
            logger.info(f"🔍 Buscando contexto para: '{pergunta.texto}'")
            resultados_busca = buscador.busca_hibrida(pergunta.texto, top_k=3)

            if resultados_busca:
                contextos = []
                for i, resultado in enumerate(resultados_busca, 1):
                    fonte = resultado.get('source_file', 'Desconhecida')
                    texto = resultado.get('text', '')
                    score = resultado.get('score', 0)
                    contextos.append(f"[Fonte {i}: {fonte}] (Score: {score:.4f})\n{texto}\n")

                contexto = "\n---\n".join(contextos)
                logger.info(f"✅ Contexto encontrado: {len(contexto)} caracteres")
            else:
                logger.warning("⚠️ Nenhum contexto relevante encontrado")
        except Exception as e:
            logger.error(f"⚠️ Erro na busca: {e}")
            contexto = ""
    else:
        logger.warning("⚠️ Buscador não disponível")

    logger.info("🤖 Consultando o filósofo IA...")
    resposta = perguntar_ao_filosofo(pergunta.texto, contexto)

    return {
        "pergunta": pergunta.texto,
        "resposta": resposta,
        "contexto_usado": bool(contexto),
        "fontes": [r.get('source_file', '') for r in resultados_busca] if resultados_busca else []
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)