##scripts/validar_buscas.py 

import json
import time
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


class ValidadorBuscas:

    def __init__(self, embeddings_file, gabarito_file):

        BASE_DIR = Path(__file__).parent.parent
        self.docs_dir = BASE_DIR / 'docs'
    
        self.embeddings_file = self.docs_dir / embeddings_file
        self.gabarito_file = self.docs_dir / gabarito_file
        self.chunked_file = self.docs_dir / 'texto_filosofico_fatiado.json'

        # Carregar dados
        with open(self.embeddings_file, 'r', encoding='utf-8') as f:
            self.embeddings_data = json.load(f)

        with open(self.chunked_file, 'r', encoding='utf-8') as f:
            self.chunks_data = json.load(f)

        with open(self.gabarito_file, 'r', encoding='utf-8') as f:
            self.gabarito = json.load(f)

        # Carregar modelo
        print("Carregando modelo para embeddings...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

        # Pré-computar matriz de embeddings
        self.embedding_matrix = np.array([
            item['embedding'] for item in self.embeddings_data
        ])

        # Definir perguntas de teste baseadas no gabarito
        self.perguntas_teste = [
            {
                'pergunta': 'O que Kant diz sobre a lei universal?',
                'autor_esperado': 'Immanuel Kant',
                'texto_gabarito': next(
                    (item['texto'] for item in self.gabarito if item['autor'] == 'Immanuel Kant'),
                    ''
                )
            },
            {
                'pergunta': 'Qual o princípio da utilidade segundo Bentham?',
                'autor_esperado': 'Jeremy Bentham',
                'texto_gabarito': next(
                    (item['texto'] for item in self.gabarito if item['autor'] == 'Jeremy Bentham'),
                    ''
                )
            },
            {
                'pergunta': 'O que é a virtude para Aristóteles?',
                'autor_esperado': 'Aristóteles',
                'texto_gabarito': next(
                    (item['texto'] for item in self.gabarito if item['autor'] == 'Aristóteles'),
                    ''
                )
            }
        ]

        print(f"Total de documentos indexados: {len(self.embeddings_data)}")
        print(f"Total de perguntas no gabarito: {len(self.perguntas_teste)}")

    def _cosine_similarity(self, query_embedding, document_embeddings):
        """Calcula similaridade de cosseno."""
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        doc_norms = document_embeddings / np.linalg.norm(document_embeddings, axis=1, keepdims=True)
        return np.dot(doc_norms, query_norm)

    def _extract_keywords(self, query):
        """Extrai palavras-chave removendo stopwords."""
        stopwords = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
            'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas',
            'por', 'para', 'com', 'sem', 'que', 'qual', 'quais', 'quem',
            'se', 'não', 'sim', 'é', 'são', 'foi', 'foram', 'ser', 'estar', 'está',
            'ter', 'tem', 'têm', 'haver', 'há', 'este', 'esta', 'estes', 'estas',
            'esse', 'essa', 'esses', 'essas', 'isto', 'isso', 'aquilo',
            'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
            'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'seu', 'sua',
            'ao', 'aos', 'às', 'dum', 'duma', 'num', 'numa',
            'mais', 'menos', 'muito', 'pouco', 'tanto', 'quão',
            'como', 'quando', 'onde', 'porque', 'porquê',
            'mas', 'ou', 'e', 'nem', 'quer', 'bem', 'mal',
            'já', 'ainda', 'sempre', 'nunca', 'jamais',
            'só', 'somente', 'apenas', 'também'
        }

        words = query.lower().split()
        keywords = [
            word.strip('.,;:!?()[]{}"\'')
            for word in words
            if word.strip('.,;:!?()[]{}"\'').lower() not in stopwords
            and len(word.strip('.,;:!?()[]{}"\'')) > 2
        ]
        return keywords

    def busca_rag(self, query, top_k=1):
        """Busca RAG baseada em similaridade semântica."""
        start_time = time.time()

        query_embedding = self.model.encode(query, convert_to_numpy=True)
        similarities = self._cosine_similarity(query_embedding, self.embedding_matrix)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'chunk_id': self.embeddings_data[idx]['chunk_id'],
                'text': self.embeddings_data[idx]['text'],
                'source_file': self.embeddings_data[idx]['source_file'],
                'score': float(similarities[idx])
            })

        elapsed = time.time() - start_time
        return results, elapsed

    def busca_grep(self, query, top_k=1):
        """Busca GREP literal por palavras-chave."""
        start_time = time.time()

        keywords = self._extract_keywords(query)
        results = []

        for item in self.chunks_data:
            text_lower = item['text'].lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)

            if match_count > 0:
                results.append({
                    'chunk_id': item['chunk_id'],
                    'text': item['text'],
                    'source_file': item['source_file'],
                    'score': match_count / len(keywords) if keywords else 0
                })

        results.sort(key=lambda x: x['score'], reverse=True)
        elapsed = time.time() - start_time
        return results[:top_k], elapsed

    def busca_hibrida(self, query, top_k=1, rag_weight=0.7, grep_weight=0.3):

        start_time = time.time()

        rag_results, _ = self.busca_rag(query, top_k=top_k * 2)
        grep_results, _ = self.busca_grep(query, top_k=top_k * 2)

        combined = {}

        for result in rag_results:
            chunk_id = result['chunk_id']
            combined[chunk_id] = {
                'chunk_id': chunk_id,
                'text': result['text'],
                'source_file': result['source_file'],
                'rag_score': result['score'],
                'grep_score': 0.0
            }

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
                    'grep_score': result['score']
                }

        for chunk_id, result in combined.items():
            result['score'] = rag_weight * result['rag_score'] + grep_weight * result['grep_score']

        sorted_results = sorted(combined.values(), key=lambda x: x['score'], reverse=True)

        final_results = []
        for result in sorted_results[:top_k]:
            final_results.append({
                'chunk_id': result['chunk_id'],
                'text': result['text'],
                'source_file': result['source_file'],
                'score': result['score']
            })

        elapsed = time.time() - start_time
        return final_results, elapsed

    def _calcular_similaridade_texto(self, texto1, texto2):
        
        emb1 = self.model.encode(texto1, convert_to_numpy=True)
        emb2 = self.model.encode(texto2, convert_to_numpy=True)

        # Similaridade de cosseno
        sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(sim)

    def validar_resultado(self, resultado, texto_gabarito, threshold=0.5):
       
        if not resultado or not texto_gabarito:
            return False

        similaridade = self._calcular_similaridade_texto(
            resultado['text'],
            texto_gabarito
        )

        return similaridade >= threshold

    def executar_validacao(self):
       
        resultados = {
            'RAG': {'acertos': 0, 'erros': 0, 'tempos': [], 'detalhes': []},
            'GREP': {'acertos': 0, 'erros': 0, 'tempos': [], 'detalhes': []},
            'HIBRIDA': {'acertos': 0, 'erros': 0, 'tempos': [], 'detalhes': []}
        }

        print("\n" + "=" * 70)
        print("EXECUTANDO VALIDAÇÃO DAS BUSCAS")
        print("=" * 70)

        for i, teste in enumerate(self.perguntas_teste, 1):
            print(f"\nPergunta {i}: {teste['pergunta']}")
            print(f"Gabarito esperado (autor): {teste['autor_esperado']}")

            # Testar RAG
            print("  Testando RAG...", end=" ")
            rag_results, rag_time = self.busca_rag(teste['pergunta'], top_k=1)
            rag_acertou = self.validar_resultado(
                rag_results[0] if rag_results else None,
                teste['texto_gabarito']
            )
            if rag_acertou:
                resultados['RAG']['acertos'] += 1
                print(f"ACERTOU (tempo: {rag_time:.4f}s)")
            else:
                resultados['RAG']['erros'] += 1
                print(f"ERROU (tempo: {rag_time:.4f}s)")

            resultados['RAG']['tempos'].append(rag_time)
            resultados['RAG']['detalhes'].append({
                'pergunta': teste['pergunta'],
                'acertou': rag_acertou,
                'tempo': rag_time,
                'resultado': rag_results[0]['text'][:100] if rag_results else None
            })

            # Testar GREP
            print("  Testando GREP...", end=" ")
            grep_results, grep_time = self.busca_grep(teste['pergunta'], top_k=1)
            grep_acertou = self.validar_resultado(
                grep_results[0] if grep_results else None,
                teste['texto_gabarito']
            )
            if grep_acertou:
                resultados['GREP']['acertos'] += 1
                print(f"ACERTOU (tempo: {grep_time:.4f}s)")
            else:
                resultados['GREP']['erros'] += 1
                print(f"ERROU (tempo: {grep_time:.4f}s)")

            resultados['GREP']['tempos'].append(grep_time)
            resultados['GREP']['detalhes'].append({
                'pergunta': teste['pergunta'],
                'acertou': grep_acertou,
                'tempo': grep_time,
                'resultado': grep_results[0]['text'][:100] if grep_results else None
            })

            # Testar Híbrida
            print("  Testando HÍBRIDA...", end=" ")
            hibrida_results, hibrida_time = self.busca_hibrida(teste['pergunta'], top_k=1)
            hibrida_acertou = self.validar_resultado(
                hibrida_results[0] if hibrida_results else None,
                teste['texto_gabarito']
            )
            if hibrida_acertou:
                resultados['HIBRIDA']['acertos'] += 1
                print(f"ACERTOU (tempo: {hibrida_time:.4f}s)")
            else:
                resultados['HIBRIDA']['erros'] += 1
                print(f"ERROU (tempo: {hibrida_time:.4f}s)")

            resultados['HIBRIDA']['tempos'].append(hibrida_time)
            resultados['HIBRIDA']['detalhes'].append({
                'pergunta': teste['pergunta'],
                'acertou': hibrida_acertou,
                'tempo': hibrida_time,
                'resultado': hibrida_results[0]['text'][:100] if hibrida_results else None
            })

        return resultados


def main():
    """Função principal da Fase 4."""

    print("=" * 70)
    print("FASE 4: PROCESSO DE VALIDAÇÃO")
    print("=" * 70)

    # Criar validador
    validador = ValidadorBuscas(
        embeddings_file='embeddings_filosofia.json',
        gabarito_file='base_filosofica.json'
    )

    # Executar validação
    resultados = validador.executar_validacao()

    # Salvar resultados para a Fase 5
    BASE_DIR = Path(__file__).parent.parent
    output_file = BASE_DIR / 'docs' / 'resultados_validacao.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    # Imprimir resumo
    print("\n" + "=" * 70)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 70)

    for metodo, dados in resultados.items():
        total = dados['acertos'] + dados['erros']
        taxa_acerto = (dados['acertos'] / total * 100) if total > 0 else 0
        tempo_medio = sum(dados['tempos']) / len(dados['tempos']) if dados['tempos'] else 0

        print(f"\n{metodo}:")
        print(f"  Acertos: {dados['acertos']}/{total}")
        print(f"  Taxa de acerto: {taxa_acerto:.1f}%")
        print(f"  Tempo médio: {tempo_medio:.4f}s")

    print(f"\nResultados salvos em: {output_file}")
    print("\nFase 4 concluída!")
    print("=" * 70)


if __name__ == '__main__':
    main()