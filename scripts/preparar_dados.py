##scripts/preparar_dados.py 

import json
import os
from pathlib import Path


def chunk_text_by_words(text, max_words=150):
   
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = ' '.join(words[i:i + max_words])
        if chunk.strip():
            chunks.append(chunk.strip())

    return chunks


def chunk_text_by_characters(text, max_chars=500):
  
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars

        # Se não chegamos ao fim do texto, tentar quebrar na última palavra completa
        if end < len(text):
            # Procurar o último espaço antes do limite
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end
        # Pular espaços em branco no início do próximo chunk
        while start < len(text) and text[start] in ' \n\t':
            start += 1

    return chunks


def process_file(filepath, chunk_method='words', chunk_size=150):
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Limpar o texto (remover múltiplos espaços em branco)
    text = ' '.join(text.split())

    if chunk_method == 'words':
        chunks = chunk_text_by_words(text, chunk_size)
    else:
        chunks = chunk_text_by_characters(text, chunk_size)

    # Criar estrutura com metadados
    filename = os.path.basename(filepath)
    result = []

    for i, chunk in enumerate(chunks):
        result.append({
            'chunk_id': i,
            'text': chunk,
            'source_file': filename,
            'char_count': len(chunk),
            'word_count': len(chunk.split())
        })

    return result


def main():
    """Função principal que processa todos os arquivos de texto filosófico."""

    # Diretórios
    docs_dir = Path('/workspace/docs')
    output_file = docs_dir / 'texto_filosofico_fatiado.json'

    # Arquivos de texto para processar
    text_files = [
        docs_dir / 'aristoteles_etica-e-nicomaco.txt',
        docs_dir / 'kant_metafisica-costumes.txt',
        docs_dir / 'jeremy_utilitarismo.txt'
    ]

    all_chunks = []

    print("=" * 60)
    print("FASE 1: PREPARAÇÃO DOS DADOS")
    print("=" * 60)

    for filepath in text_files:
        if filepath.exists():
            print(f"\nProcessando: {filepath.name}")
            chunks = process_file(filepath, chunk_method='words', chunk_size=150)
            print(f"  -> {len(chunks)} chunks criados")
            all_chunks.extend(chunks)
        else:
            print(f"\nArquivo não encontrado: {filepath}")

    # Salvar resultado
    print(f"\nTotal de chunks: {len(all_chunks)}")
    print(f"Salvando em: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print("\nFase 1 concluída com sucesso!")
    print("=" * 60)


if __name__ == '__main__':
    main()