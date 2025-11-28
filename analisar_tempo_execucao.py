"""
Análise e Visualização dos Tempos de Classificação
==================================================

Este script analisa os resultados de tempo de execução do classificador
de árvore de decisão e cria visualizações comparativas.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def carregar_resultados_tempo():
    """
    Carrega os resultados de tempo do arquivo JSON.
    """
    with open('./resultados/modelos/tempos_classificacao.json', 'r') as f:
        resultados = json.load(f)
    
    # Converte para DataFrame para análise
    data = []
    for num_exec, tempos in resultados.items():
        data.append({
            'execucoes': int(num_exec),
            'perf_counter_ms': tempos['perf_counter_por_predicao_ms'],
            'process_time_ms': tempos['process_time_por_predicao_ms'],
            'perf_counter_total': tempos['perf_counter_total'],
            'process_time_total': tempos['process_time_total']
        })
    
    df = pd.DataFrame(data)
    return df

def analisar_resultados(df):
    """
    Análise estatística dos resultados de tempo.
    """
    print("📊 ANÁLISE ESTATÍSTICA DOS TEMPOS DE EXECUÇÃO")
    print("="*60)
    
    # Estatísticas básicas
    print("\n📈 Estatísticas do tempo por predição (perf_counter):")
    print(f"   Média: {df['perf_counter_ms'].mean():.4f} ms")
    print(f"   Desvio padrão: {df['perf_counter_ms'].std():.4f} ms")
    print(f"   Mínimo: {df['perf_counter_ms'].min():.4f} ms")
    print(f"   Máximo: {df['perf_counter_ms'].max():.4f} ms")
    print(f"   Coeficiente de variação: {(df['perf_counter_ms'].std()/df['perf_counter_ms'].mean())*100:.2f}%")
    
    print("\n📈 Estatísticas do tempo por predição (process_time):")
    print(f"   Média: {df['process_time_ms'].mean():.4f} ms")
    print(f"   Desvio padrão: {df['process_time_ms'].std():.4f} ms")
    print(f"   Mínimo: {df['process_time_ms'].min():.4f} ms")
    print(f"   Máximo: {df['process_time_ms'].max():.4f} ms")
    print(f"   Coeficiente de variação: {(df['process_time_ms'].std()/df['process_time_ms'].mean())*100:.2f}%")
    
    # Comparação entre métodos
    diferenca_media = abs(df['perf_counter_ms'].mean() - df['process_time_ms'].mean())
    print(f"\n🔍 Diferença média entre métodos: {diferenca_media:.4f} ms")
    
    return df

def criar_visualizacoes(df):
    """
    Cria visualizações dos resultados de tempo.
    """
    print("\n📊 Criando visualizações...")
    
    # Configuração do estilo
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Figura com múltiplos gráficos
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Tempo por predição vs Número de execuções
    ax1 = axes[0, 0]
    ax1.plot(df['execucoes'], df['perf_counter_ms'], 'o-', linewidth=2, 
             markersize=8, color='#2E86AB', label='perf_counter')
    ax1.plot(df['execucoes'], df['process_time_ms'], 's-', linewidth=2, 
             markersize=8, color='#A23B72', label='process_time')
    ax1.set_xlabel('Número de Execuções', fontweight='bold')
    ax1.set_ylabel('Tempo por Predição (ms)', fontweight='bold')
    ax1.set_title('Tempo de Predição vs Volume de Execuções', fontweight='bold', pad=20)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # 2. Comparação direta entre métodos
    ax2 = axes[0, 1]
    x = np.arange(len(df))
    width = 0.35
    ax2.bar(x - width/2, df['perf_counter_ms'], width, 
            label='perf_counter', color='#2E86AB', alpha=0.8)
    ax2.bar(x + width/2, df['process_time_ms'], width, 
            label='process_time', color='#A23B72', alpha=0.8)
    ax2.set_xlabel('Teste', fontweight='bold')
    ax2.set_ylabel('Tempo por Predição (ms)', fontweight='bold')
    ax2.set_title('Comparação entre Métodos de Medição', fontweight='bold', pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{exec}' for exec in df['execucoes']])
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores nas barras
    for i, (perf, proc) in enumerate(zip(df['perf_counter_ms'], df['process_time_ms'])):
        ax2.text(i - width/2, perf + 0.001, f'{perf:.3f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax2.text(i + width/2, proc + 0.001, f'{proc:.3f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 3. Tempo total vs Número de execuções
    ax3 = axes[1, 0]
    ax3.plot(df['execucoes'], df['perf_counter_total']*1000, 'o-', linewidth=2, 
             markersize=8, color='#F18F01', label='perf_counter')
    ax3.plot(df['execucoes'], df['process_time_total']*1000, 's-', linewidth=2, 
             markersize=8, color='#C73E1D', label='process_time')
    ax3.set_xlabel('Número de Execuções', fontweight='bold')
    ax3.set_ylabel('Tempo Total (ms)', fontweight='bold')
    ax3.set_title('Tempo Total de Execução', fontweight='bold', pad=20)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    
    # 4. Eficiência (tempo por predição normalizado)
    ax4 = axes[1, 1]
    # Calcula eficiência relativa (menor tempo = 100%)
    min_time = df['perf_counter_ms'].min()
    eficiencia_perf = (min_time / df['perf_counter_ms']) * 100
    eficiencia_proc = (min_time / df['process_time_ms']) * 100
    
    ax4.bar(x - width/2, eficiencia_perf, width, 
            label='perf_counter', color='#4CAF50', alpha=0.8)
    ax4.bar(x + width/2, eficiencia_proc, width, 
            label='process_time', color='#FF9800', alpha=0.8)
    ax4.set_xlabel('Teste', fontweight='bold')
    ax4.set_ylabel('Eficiência Relativa (%)', fontweight='bold')
    ax4.set_title('Eficiência Relativa dos Métodos', fontweight='bold', pad=20)
    ax4.set_xticks(x)
    ax4.set_xticklabels([f'{exec}' for exec in df['execucoes']])
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.set_ylim(0, 105)
    
    plt.tight_layout()
    plt.savefig('./resultados/visualizacoes/analise_tempo_classificacao.png', 
                dpi=300, bbox_inches='tight')
    print("   ✅ Salvo: ./resultados/visualizacoes/analise_tempo_classificacao.png")
    
    plt.show()

def comparar_com_benchmarks():
    """
    Compara os resultados com benchmarks típicos de classificadores.
    """
    print("\n🏆 COMPARAÇÃO COM BENCHMARKS")
    print("="*60)
    
    # Benchmarks típicos (valores aproximados)
    benchmarks = {
        'Árvore de Decisão Simples': {'tempo_ms': 0.01, 'precisao': 85},
        'Árvore de Decisão Otimizada': {'tempo_ms': 0.05, 'precisao': 90},
        'Nosso Modelo': {'tempo_ms': 0.097, 'precisao': 92.08},
        'Random Forest (100 árvores)': {'tempo_ms': 2.0, 'precisao': 94.58},
        'SVM RBF': {'tempo_ms': 0.5, 'precisao': 90.67},
        'Rede Neural Simples': {'tempo_ms': 0.2, 'precisao': 91}
    }
    
    print("\nModelo                    | Tempo (ms) | Precisão (%)")
    print("-" * 55)
    
    for modelo, stats in benchmarks.items():
        tempo_str = f"{stats['tempo_ms']:.3f}".ljust(10)
        precisao_str = f"{stats['precisao']:.2f}".ljust(11)
        
        if modelo == 'Nosso Modelo':
            print(f"🎯 {modelo:<20} | {tempo_str} | {precisao_str} ⭐")
        else:
            print(f"   {modelo:<20} | {tempo_str} | {precisao_str}")
    
    print(f"\n💡 ANÁLISE COMPARATIVA:")
    print(f"   • Nosso modelo oferece excelente balance tempo/precisão")
    print(f"   • Tempo competitivo para aplicações em tempo real")
    print(f"   • Precisão superior a árvores simples")
    print(f"   • Mais rápido que ensemble methods (Random Forest)")

def avaliar_aplicabilidade():
    """
    Avalia a aplicabilidade do modelo em diferentes cenários.
    """
    print("\n🎯 AVALIAÇÃO DE APLICABILIDADE")
    print("="*60)
    
    tempo_medio = 0.097  # ms por predição
    
    # Diferentes cenários de uso
    cenarios = {
        'Detecção em tempo real (10 Hz)': {'freq_hz': 10, 'limite_ms': 100},
        'Detecção rápida (50 Hz)': {'freq_hz': 50, 'limite_ms': 20},
        'Sistema embarcado (1 Hz)': {'freq_hz': 1, 'limite_ms': 1000},
        'Aplicativo móvel (5 Hz)': {'freq_hz': 5, 'limite_ms': 200},
        'Monitoramento contínuo (100 Hz)': {'freq_hz': 100, 'limite_ms': 10}
    }
    
    print("\nCenário                        | Freq.  | Limite  | Nosso Tempo | Status")
    print("-" * 80)
    
    for cenario, config in cenarios.items():
        freq = config['freq_hz']
        limite = config['limite_ms']
        
        if tempo_medio <= limite:
            status = "✅ ADEQUADO"
        elif tempo_medio <= limite * 2:
            status = "⚠️  MARGINAL"
        else:
            status = "❌ INADEQUADO"
        
        print(f"{cenario:<30} | {freq:>4} Hz | {limite:>6} ms | {tempo_medio:>9.3f} ms | {status}")
    
    print(f"\n🚀 CAPACIDADE MÁXIMA TEÓRICA:")
    freq_max = 1000 / tempo_medio  # Hz
    print(f"   • Frequência máxima: ~{freq_max:.0f} Hz")
    print(f"   • Predições por segundo: ~{freq_max:.0f}")
    print(f"   • Adequado para a maioria das aplicações práticas")

def main():
    """
    Função principal para análise completa dos tempos.
    """
    print("⏱️  ANÁLISE COMPLETA DOS TEMPOS DE CLASSIFICAÇÃO")
    print("Baseado nas medições do classificador de árvore de decisão")
    print("="*70)
    
    try:
        # Carrega resultados
        df = carregar_resultados_tempo()
        
        # Análise estatística
        df = analisar_resultados(df)
        
        # Visualizações
        criar_visualizacoes(df)
        
        # Comparações e avaliações
        comparar_com_benchmarks()
        avaliar_aplicabilidade()
        
        print(f"\n✅ ANÁLISE CONCLUÍDA!")
        print(f"📁 Visualização salva em: ./resultados/visualizacoes/")
        
    except Exception as e:
        print(f"❌ Erro durante análise: {str(e)}")

if __name__ == "__main__":
    main()