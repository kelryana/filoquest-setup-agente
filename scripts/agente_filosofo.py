#!/usr/bin/env python3
import requests
import json

def perguntar_ao_filosofo(pergunta):
    """Envia uma pergunta para o Qwen via Ollama"""
    url = "http://localhost:11434/api/generate"
    
    # Persona de filósofo
    prompt = f"""Você é um filósofo. Responda à pergunta de forma clara:
    
    Pergunta: {pergunta}
    
    Resposta:"""
    
    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    return response.json()['response']

if __name__ == "__main__":
    print("🤖 Agente Filósofo (Qwen 3B)")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        pergunta = input("🧠 Você: ")
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            break
        
        print("🤔 Pensando...")
        resposta = perguntar_ao_filosofo(pergunta)
        print(f"📚 Filósofo: {resposta}\n")
