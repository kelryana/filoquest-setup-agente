#!/usr/bin/env python3
import json
from sentence_transformers import SentenceTransformer
import torch

def gerar_embeddings(passagens):
    """Gera embeddings para cada passagem usando Sentence-Transformers"""
    
    # Carrega o modelo (pequeno e rápido)
    print("📥 Carregando modelo all-MiniLM-L6-v2...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    textos = [p['texto'] for p in passagens]
    nomes = [p['nome'] for p in passagens]
    
    # Gera os embeddings
    print("🔄 Gerando embeddings...")
    embeddings = model.encode(textos, convert_to_tensor=True)
    
    # Converte para lista (para salvar como JSON)
    embeddings_lista = embeddings.tolist()
    
    return {
        'nomes': nomes,
        'embeddings': embeddings_lista
    }

if __name__ == "__main__":
    # Carrega as passagens extraídas
    try:
        with open("docs/passagens.json", "r", encoding="utf-8") as f:
            passagens = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo docs/passagens.json não encontrado!")
        print("Execute primeiro: python scripts/extract_twine.py")
        exit(1)
    
    # Gera os embeddings
    resultado = gerar_embeddings(passagens)
    
    # Salva os embeddings
    with open("docs/embeddings.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Embeddings gerados para {len(resultado['nomes'])} passagens")
    print(f"📊 Dimensão dos embeddings: {len(resultado['embeddings'][0])}")
    
    # Mostra um exemplo
    print("\n📝 Exemplo da primeira passagem:")
    print(f"Nome: {resultado['nomes'][0]}")
    print(f"Embedding (primeiros 5 valores): {resultado['embeddings'][0][:5]}...")
