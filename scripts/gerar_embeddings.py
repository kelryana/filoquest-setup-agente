##scripts/gerar_embeddings.py

import json
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer


def load_chunked_text(filepath):
    """Carrega o JSON com os chunks de texto."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_embeddings(chunks, model_name='all-MiniLM-L6-v2'):

    print(f"Carregando modelo: {model_name}")
   
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🔧 Usando dispositivo: {device.upper()}")

    model = SentenceTransformer(model_name, device=device)
    print(f"Modelo carregado com sucesso: {model_name} (dimensão do embedding: {model.get_sentence_embedding_dimension()})")

    # Extrair apenas os textos
    texts = [chunk['text'] for chunk in chunks]

    print(f"Gerando embeddings para {len(texts)} chunks...")
    # Usar batch pequeno para evitar estouro de memória
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=8, convert_to_numpy=True)

    # Combinar embeddings com metadados originais
    results = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        results.append({
            'chunk_id': chunk['chunk_id'],
            'text': chunk['text'],
            'source_file': chunk['source_file'],
            'char_count': chunk['char_count'],
            'word_count': chunk['word_count'],
            'embedding': embedding.tolist()  # Converter numpy array para lista
        })

    return results


def main():

    # Diretórios
    BASE_DIR = Path(__file__).parent.parent
    docs_dir = BASE_DIR / 'docs'

    # Definição dos arquivos de entrada e saída (O QUE ESTAVA FALTANDO)
    input_file = docs_dir / 'texto_filosofico_fatiado.json'
    output_file = docs_dir / 'embeddings_filosofia.json'

    print("=" * 60)
    print("FASE 2: GERAR OS EMBEDDINGS")
    print("=" * 60)

    # Carregar chunks
    print(f"\nCarregando chunks de: {input_file}")
    chunks = load_chunked_text(input_file)
    print(f"Total de chunks carregados: {len(chunks)}")

    # Gerar embeddings
    embeddings_data = generate_embeddings(chunks)

    # Salvar resultado
    print(f"\nSalvando embeddings em: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

    # Estatísticas
    embedding_dim = len(embeddings_data[0]['embedding'])
    total_size_mb = output_file.stat().st_size / (1024 * 1024)

    print(f"\nResumo:")
    print(f"  - Dimensão dos embeddings: {embedding_dim}")
    print(f"  - Total de embeddings: {len(embeddings_data)}")
    print(f"  - Tamanho do arquivo: {total_size_mb:.2f} MB")
    print("\nFase 2 concluída com sucesso!")
    print("=" * 60)

if __name__ == '__main__':
    main()