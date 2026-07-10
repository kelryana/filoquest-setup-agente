#!/usr/bin/env python3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Carrega modelo
model = SentenceTransformer('all-MiniLM-L6-v2')

# Carrega embeddings
with open("docs/embeddings_bonde.json", "r") as f:
    dados = json.load(f)

def buscar(texto):
    emb_busca = model.encode([texto])
    similaridades = []
    for emb in dados['embeddings']:
        sim = np.dot(emb_busca[0], emb) / (np.linalg.norm(emb_busca[0]) * np.linalg.norm(emb))
        similaridades.append(sim)
    
    idx = np.argmax(similaridades)
    return dados['nomes'][idx], similaridades[idx]

# Teste
testes = [
    "O que acontece se eu puxar a alavanca?",
    "O homem gordo",
    "O bonde desgovernado",
    "Ética e moral",
]

for texto in testes:
    nome, sim = buscar(texto)
    print(f"🔍 '{texto}' → {nome} (similaridade: {sim:.4f})")