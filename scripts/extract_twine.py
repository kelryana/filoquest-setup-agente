#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup
import json

def extract_twine_text(html_path):
    """Extrai o texto de todas as passagens de um arquivo HTML do Twine"""
    
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # No Twine, as passagens estão em tags <tw-passagedata>
    passages = soup.find_all('tw-passagedata')
    
    texto_extraido = []
    for passage in passages:
        # Pega o nome e o conteúdo
        name = passage.get('name', 'sem_nome')
        content = passage.get_text(strip=True)
        
        texto_extraido.append({
            'nome': name,
            'texto': content
        })
    
    return texto_extraido

if __name__ == "__main__":
    # Caminho do arquivo HTML
    html_path = "docs/strange_encounter.html"
    
    # Verifica se o arquivo existe
    if not os.path.exists(html_path):
        print(f"❌ Arquivo não encontrado: {html_path}")
        print("Certifique-se que o arquivo está em docs/")
        exit(1)
    
    # Extrai o texto
    passagens = extract_twine_text(html_path)
    
    # Salva como JSON para usar depois
    with open("docs/passagens.json", "w", encoding="utf-8") as f:
        json.dump(passagens, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Extraídas {len(passagens)} passagens do Twine")
    for p in passagens:
        print(f"📝 {p['nome']}: {p['texto'][:50]}...")
