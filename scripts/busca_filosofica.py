##scripts/busca_filosofica.py

import json
import torch
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pathlib import Path


class BuscaFilosofica:
    """Classe que implementa os mecanismos de busca RAG, Grep e Híbrido."""

    def __init__(self, embeddings_file, model_name='all-MiniLM-L6-v2'):
      
        BASE_DIR = Path(__file__).parent.parent 
        self.docs_dir = BASE_DIR / 'docs' 
        self.embeddings_file = self.docs_dir / embeddings_file
        self.chunked_file = self.docs_dir / 'texto_filosofico_fatiado.json'

        # Carregar dados
        print(f"Carregando embeddings de: {self.embeddings_file}")
        with open(self.embeddings_file, 'r', encoding='utf-8') as f:
            self.embeddings_data = json.load(f)

        print(f"Carregando chunks de: {self.chunked_file}")
        with open(self.chunked_file, 'r', encoding='utf-8') as f:
            self.chunks_data = json.load(f)

        # Carregar modelo para gerar embeddings de queries
        print(f"Carregando modelo: {model_name}")
        
        self.model = SentenceTransformer(model_name, device='cpu')

        # Pré-computar matriz de embeddings para eficiência
        self.embedding_matrix = np.array([
            item['embedding'] for item in self.embeddings_data
        ])

        print(f"Total de documentos indexados: {len(self.embeddings_data)}")

    def _cosine_similarity(self, query_embedding, document_embeddings):
       
        # Normalizar vetores
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        doc_norms = document_embeddings / np.linalg.norm(document_embeddings, axis=1, keepdims=True)

        # Calcular similaridade de cosseno
        similarities = np.dot(doc_norms, query_norm)
        return similarities

    def busca_rag(self, query, top_k=3):
       
        # Gerar embedding da query
        query_embedding = self.model.encode(query, convert_to_numpy=True)

        # Calcular similaridades
        similarities = self._cosine_similarity(query_embedding, self.embedding_matrix)

        # Obter índices dos top_k resultados
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'chunk_id': self.embeddings_data[idx]['chunk_id'],
                'text': self.embeddings_data[idx]['text'],
                'source_file': self.embeddings_data[idx]['source_file'],
                'score': float(similarities[idx]),
                'method': 'RAG'
            })

        return results

    def _extract_keywords(self, query):
      
        # Stopwords em português
        stopwords = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
            'de', 'da', 'do', 'das', 'dos',
            'em', 'no', 'na', 'nos', 'nas',
            'por', 'para', 'com', 'sem',
            'que', 'qual', 'quais', 'quem',
            'se', 'não', 'sim',
            'é', 'são', 'foi', 'foram', 'ser', 'estar', 'está',
            'ter', 'tem', 'têm', 'haver', 'há',
            'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas',
            'isto', 'isso', 'aquilo',
            'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
            'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'seu', 'sua',
            'ao', 'aos', 'às', 'dum', 'duma', 'num', 'numa',
            'mais', 'menos', 'muito', 'pouco', 'tanto', 'quão',
            'como', 'quando', 'onde', 'porque', 'porquê',
            'mas', 'ou', 'e', 'nem', 'quer', 'bem', 'mal',
            'já', 'ainda', 'sempre', 'nunca', 'jamais',
            'só', 'somente', 'apenas', 'também',
            'entre', 'sobre', 'sob', 'até', 'desde', 'após',
            'contra', 'segundo', 'conforme', 'mediante',
            'lhe', 'lhes', 'o', 'a', 'os', 'as', 'lo', 'la', 'los', 'las',
            'me', 'te', 'se', 'nos', 'vos', 'lhe', 'lhes',
            'do', 'da', 'disso', 'disto', 'daquilo',
            'relativo', 'referente', 'acerca', 'respeito'
        }

        # Tokenizar e filtrar
        words = query.lower().split()
        keywords = [
            word.strip('.,;:!?()[]{}"\'')
            for word in words
            if word.strip('.,;:!?()[]{}"\'').lower() not in stopwords
            and len(word.strip('.,;:!?()[]{}"\'')) > 2
        ]

        return keywords

    def busca_grep(self, query, top_k=3):
       
        keywords = self._extract_keywords(query)

        if not keywords:
            # Se não houver palavras-chave, retornar vazio
            return []

        results = []
        for item in self.chunks_data:
            text_lower = item['text'].lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)

            if match_count > 0:
                results.append({
                    'chunk_id': item['chunk_id'],
                    'text': item['text'],
                    'source_file': item['source_file'],
                    'score': match_count / len(keywords),  # Proporção de palavras encontradas
                    'method': 'GREP',
                    'matched_keywords': [kw for kw in keywords if kw in text_lower]
                })

        # Ordenar por score (maior proporção de matches primeiro)
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:top_k]

    def busca_hibrida(self, query, top_k=3, rag_weight=0.7, grep_weight=0.3):
      
        # Obter resultados de ambos os métodos
        rag_results = self.busca_rag(query, top_k=top_k * 2)  # Pegar mais para combinar
        grep_results = self.busca_grep(query, top_k=top_k * 2)

        # Criar dicionário para combinar resultados pelo chunk_id
        combined = {}

        # Adicionar resultados RAG
        for result in rag_results:
            chunk_id = result['chunk_id']
            combined[chunk_id] = {
                'chunk_id': chunk_id,
                'text': result['text'],
                'source_file': result['source_file'],
                'rag_score': result['score'],
                'grep_score': 0.0,
                'method': 'HIBRIDA'
            }

        # Adicionar/atualizar com resultados Grep
        for result in grep_results:
            chunk_id = result['chunk_id']
            if chunk_id in combined:
                combined[chunk_id]['grep_score'] = result['score']
            else:
                combined[chunk_id] = {
                    'chunk_id': chunk_id,
                    'text': result['text'],
                    'source_file': result['source_file'],
                    'rag_score': 0.0,
                    'grep_score': result['score'],
                    'method': 'HIBRIDA'
                }

        # Calcular score ponderado
        for chunk_id, result in combined.items():
            result['score'] = (
                rag_weight * result['rag_score'] +
                grep_weight * result['grep_score']
            )

        # Ordenar por score combinado
        sorted_results = sorted(combined.values(), key=lambda x: x['score'], reverse=True)

        # Limpar campos intermediários e retornar top_k
        final_results = []
        for result in sorted_results[:top_k]:
            final_results.append({
                'chunk_id': result['chunk_id'],
                'text': result['text'],
                'source_file': result['source_file'],
                'score': result['score'],
                'rag_score': result['rag_score'],
                'grep_score': result['grep_score'],
                'method': 'HIBRIDA'
            })

        return final_results


def main():
    """Função principal para testar os mecanismos de busca."""

    print("=" * 60)
    print("FASE 3: MECANISMO DE BUSCA")
    print("=" * 60)

    # Inicializar buscador
    buscador = BuscaFilosofica('embeddings_filosofia.json')

    # Testar com algumas perguntas
    test_queries = [
        "O que Kant diz sobre a lei universal?",
        "O que é a virtude para Aristóteles?",
        "Qual o princípio da utilidade segundo Bentham?"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"PERGUNTA: {query}")
        print(f"{'='*60}")

        print("\n--- BUSCA RAG ---")
        rag_results = buscador.busca_rag(query, top_k=2)
        for i, result in enumerate(rag_results, 1):
            print(f"\n{i}. Score: {result['score']:.4f} | Fonte: {result['source_file']}")
            print(f"   Texto: {result['text'][:200]}...")

        print("\n--- BUSCA GREP ---")
        grep_results = buscador.busca_grep(query, top_k=2)
        for i, result in enumerate(grep_results, 1):
            print(f"\n{i}. Score: {result['score']:.4f} | Fonte: {result['source_file']}")
            print(f"   Palavras encontradas: {result.get('matched_keywords', [])}")
            print(f"   Texto: {result['text'][:200]}...")

        print("\n--- BUSCA HÍBRIDA ---")
        hibrida_results = buscador.busca_hibrida(query, top_k=2)
        for i, result in enumerate(hibrida_results, 1):
            print(f"\n{i}. Score: {result['score']:.4f} | RAG: {result['rag_score']:.4f} | GREP: {result['grep_score']:.4f}")
            print(f"   Fonte: {result['source_file']}")
            print(f"   Texto: {result['text'][:200]}...")

    print(f"\n{'='*60}")
    print("Fase 3 concluída!")
    print("=" * 60)


if __name__ == '__main__':
    main()