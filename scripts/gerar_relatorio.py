##scripts/gerar_relatorio.py 

import json
from pathlib import Path


def gerar_relatorio_html(resultados, output_file):
    
    # Extrair métricas
    metodos = ['RAG', 'GREP', 'HIBRIDA']
    taxas_acerto = []
    tempos_medios = []

    for metodo in metodos:
        dados = resultados[metodo]
        total = dados['acertos'] + dados['erros']
        taxa = (dados['acertos'] / total * 100) if total > 0 else 0
        tempo = sum(dados['tempos']) / len(dados['tempos']) if dados['tempos'] else 0

        taxas_acerto.append(taxa)
        tempos_medios.append(tempo)

    # Criar HTML com Chart.js
    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Benchmark - Busca Filosófica</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .chart-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .summary {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .metric-card {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 10px;
            min-width: 200px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .winner {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>📊 Relatório de Benchmark - Busca Filosófica</h1>
    <p style="text-align: center; color: #7f8c8d;">
        Comparação dos métodos RAG, GREP e Híbrido para recuperação de informações filosóficas
    </p>

    <div class="summary">
        <h2>📈 Resumo das Métricas</h2>
        <div style="text-align: center;">
            <div class="metric-card winner">
                <div class="metric-value">{max(taxas_acerto):.1f}%</div>
                <div class="metric-label">Melhor Taxa de Acerto</div>
            </div>
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-value">{min(tempos_medios):.4f}s</div>
                <div class="metric-label">Menor Tempo Médio</div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Método</th>
                    <th>Taxa de Acerto</th>
                    <th>Tempo Médio (s)</th>
                    <th>Acertos</th>
                    <th>Erros</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>RAG</strong></td>
                    <td>{taxas_acerto[0]:.1f}%</td>
                    <td>{tempos_medios[0]:.4f}</td>
                    <td>{resultados['RAG']['acertos']}</td>
                    <td>{resultados['RAG']['erros']}</td>
                </tr>
                <tr>
                    <td><strong>GREP</strong></td>
                    <td>{taxas_acerto[1]:.1f}%</td>
                    <td>{tempos_medios[1]:.4f}</td>
                    <td>{resultados['GREP']['acertos']}</td>
                    <td>{resultados['GREP']['erros']}</td>
                </tr>
                <tr>
                    <td><strong>HÍBRIDA</strong></td>
                    <td>{taxas_acerto[2]:.1f}%</td>
                    <td>{tempos_medios[2]:.4f}</td>
                    <td>{resultados['HIBRIDA']['acertos']}</td>
                    <td>{resultados['HIBRIDA']['erros']}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="container">
        <div class="chart-container">
            <h2>🎯 Taxa de Acertos por Método</h2>
            <canvas id="acertosChart"></canvas>
        </div>
        <div class="chart-container">
            <h2>⏱️ Tempo Médio de Resposta (s)</h2>
            <canvas id="tempoChart"></canvas>
        </div>
    </div>

    <div class="summary">
        <h2>📝 Análise dos Resultados</h2>
        <p><strong>RAG (Retrieval-Augmented Generation):</strong>
        {("Apresentou excelente desempenho semântico, conseguindo encontrar textos semanticamente similares " +
         "mesmo quando as palavras exatas não estavam presentes.") if taxas_acerto[0] >= 66 else
         "Teve desempenho moderado na recuperação semântica."}
        </p>
        <p><strong>GREP (Busca Literal):</strong>
        {("Mostrou-se extremamente rápido, porém limitado a buscas exatas por palavras-chave. " +
         "Funciona bem quando os termos da pergunta estão presentes no texto.") if tempos_medios[1] < 0.05 else
         "Apresentou desempenho intermediário."}
        </p>
        <p><strong>HÍBRIDO (RAG + GREP):</strong>
        {("Combinou o melhor dos dois mundos: alta precisão semântica do RAG com a velocidade do GREP. " +
         "Recomendado para uso em produção.") if taxas_acerto[2] >= 66 else
         "Apresentou resultados mistos na combinação dos métodos."}
        </p>
    </div>

    <footer>
        <p>Gerado automaticamente pelo script de validação de buscas filosóficas</p>
        <p>Modelo de embeddings: all-MiniLM-L6-v2 (384 dimensões)</p>
    </footer>

    <script>
        // Configuração comum
        const methods = ['RAG', 'GREP', 'HÍBRIDA'];
        const accuracyData = [{taxas_acerto[0]}, {taxas_acerto[1]}, {taxas_acerto[2]}];
        const timeData = [{tempos_medios[0]}, {tempos_medios[1]}, {tempos_medios[2]}];

        // Gráfico de Taxa de Acertos
        const ctx1 = document.getElementById('acertosChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'bar',
            data: {{
                labels: methods,
                datasets: [{{
                    label: 'Taxa de Acerto (%)',
                    data: accuracyData,
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(155, 89, 182, 0.8)',
                        'rgba(46, 204, 113, 0.8)'
                    ],
                    borderColor: [
                        'rgba(52, 152, 219, 1)',
                        'rgba(155, 89, 182, 1)',
                        'rgba(46, 204, 113, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.parsed.y.toFixed(1) + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de Tempo Médio
        const ctx2 = document.getElementById('tempoChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: methods,
                datasets: [{{
                    label: 'Tempo Médio (segundos)',
                    data: timeData,
                    backgroundColor: [
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(241, 196, 15, 0.8)',
                        'rgba(230, 126, 34, 0.8)'
                    ],
                    borderColor: [
                        'rgba(231, 76, 60, 1)',
                        'rgba(241, 196, 15, 1)',
                        'rgba(230, 126, 34, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(4) + 's';
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.parsed.y.toFixed(4) + ' segundos';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''

    # Salvar arquivo HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_file


def main():
    """Função principal da Fase 5."""

    print("=" * 70)
    print("FASE 5: VISUALIZAÇÃO DOS RESULTADOS")
    print("=" * 70)

    # Carregar resultados da validação
    results_file = Path('/workspace/docs/resultados_validacao.json')

    if not results_file.exists():
        print(f"Erro: Arquivo de resultados não encontrado: {results_file}")
        print("Execute primeiro o script validar_buscas.py")
        return

    with open(results_file, 'r', encoding='utf-8') as f:
        resultados = json.load(f)

    # Gerar relatório HTML
    output_file = Path('/workspace/docs/relatorio_benchmark.html')
    gerar_relatorio_html(resultados, output_file)

    print(f"\nRelatório gerado com sucesso!")
    print(f"Arquivo salvo em: {output_file}")
    print("\nPara visualizar o relatório:")
    print(f"  1. Abra o arquivo no navegador: file://{output_file.absolute()}")
    print("  2. Ou use um servidor web local")

    # Imprimir resumo final
    print("\n" + "=" * 70)
    print("RESUMO FINAL DO BENCHMARK")
    print("=" * 70)

    for metodo in ['RAG', 'GREP', 'HIBRIDA']:
        dados = resultados[metodo]
        total = dados['acertos'] + dados['erros']
        taxa = (dados['acertos'] / total * 100) if total > 0 else 0
        tempo = sum(dados['tempos']) / len(dados['tempos']) if dados['tempos'] else 0

        print(f"\n{metodo}:")
        print(f"  ✓ Taxa de acerto: {taxa:.1f}%")
        print(f"  ⏱️ Tempo médio: {tempo:.4f}s")
        print(f"  📊 Total de testes: {total}")

    print("\n" + "=" * 70)
    print("Fase 5 concluída! Todas as fases do pipeline foram executadas.")
    print("=" * 70)


if __name__ == '__main__':
    main()