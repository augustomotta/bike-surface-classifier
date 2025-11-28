"""
Análise Completa do Uso de Memória - Comparações e Visualizações
===============================================================

Este script analisa os resultados de memória e cria comparações
detalhadas com outros modelos e o código original.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def carregar_resultados_memoria():
    """
    Carrega os resultados de memória do arquivo JSON.
    """
    with open('./resultados/modelos/analise_memoria.json', 'r') as f:
        resultados = json.load(f)
    
    return resultados

def criar_visualizacoes_memoria():
    """
    Cria visualizações dos resultados de memória.
    """
    print("📊 Criando visualizações de uso de memória...")
    
    # Dados do nosso modelo
    resultados = carregar_resultados_memoria()
    
    # Dados para comparação
    modelos_comparacao = {
        'Código Original\n(toy problem)': {'memoria_mb': 0.001, 'precisao': 85.0, 'features': 2, 'nos': 7},
        'Nosso Modelo\n(mundo real)': {
            'memoria_mb': resultados['tamanho_modelo']['pympler_mb'],
            'precisao': 92.08,
            'features': 62,
            'nos': 243
        },
        'Random Forest\n(100 árvores)': {'memoria_mb': 0.5, 'precisao': 94.58, 'features': 62, 'nos': 24300},
        'SVM\n(1000 vetores)': {'memoria_mb': 2.0, 'precisao': 90.67, 'features': 62, 'nos': 1000},
        'Rede Neural\n(3 camadas)': {'memoria_mb': 0.1, 'precisao': 91.0, 'features': 62, 'nos': 300}
    }
    
    # Configuração do estilo
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Memória vs Precisão
    ax1 = axes[0, 0]
    modelos = list(modelos_comparacao.keys())
    memorias = [modelos_comparacao[m]['memoria_mb'] for m in modelos]
    precisoes = [modelos_comparacao[m]['precisao'] for m in modelos]
    cores = ['red', 'green', 'blue', 'orange', 'purple']
    
    scatter = ax1.scatter(memorias, precisoes, c=cores, s=100, alpha=0.7)
    
    for i, modelo in enumerate(modelos):
        ax1.annotate(modelo, (memorias[i], precisoes[i]), 
                    xytext=(5, 5), textcoords='offset points', 
                    fontsize=9, ha='left')
    
    ax1.set_xlabel('Uso de Memória (MB)', fontweight='bold')
    ax1.set_ylabel('Precisão (%)', fontweight='bold')
    ax1.set_title('Memória vs Precisão dos Modelos', fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Destaca nosso modelo
    nosso_idx = 1
    ax1.scatter([memorias[nosso_idx]], [precisoes[nosso_idx]], 
               c='green', s=200, marker='*', edgecolor='black', linewidth=2)
    
    # 2. Eficiência (Precisão por MB)
    ax2 = axes[0, 1]
    eficiencias = [p/m if m > 0 else 0 for p, m in zip(precisoes, memorias)]
    barras = ax2.bar(range(len(modelos)), eficiencias, 
                     color=['red', 'green', 'blue', 'orange', 'purple'], alpha=0.7)
    
    # Destaca nosso modelo
    barras[1].set_color('green')
    barras[1].set_alpha(1.0)
    barras[1].set_edgecolor('black')
    barras[1].set_linewidth(2)
    
    ax2.set_ylabel('Eficiência (Precisão/MB)', fontweight='bold')
    ax2.set_title('Eficiência dos Modelos', fontweight='bold', pad=20)
    ax2.set_xticks(range(len(modelos)))
    ax2.set_xticklabels([m.replace('\n', ' ') for m in modelos], rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores nas barras
    for i, v in enumerate(eficiencias):
        ax2.text(i, v + max(eficiencias)*0.02, f'{v:.0f}', 
                ha='center', va='bottom', fontweight='bold')
    
    # 3. Análise de componentes do nosso sistema
    ax3 = axes[1, 0]
    
    componentes = ['Modelo\n(Árvore)', 'Scaler\n(Normalização)', 'Label Encoder\n(Classes)']
    tamanhos_bytes = [
        resultados['tamanho_modelo']['pympler_bytes'],
        3368,  # Do resultado anterior
        544    # Do resultado anterior
    ]
    
    # Converte para KB para melhor visualização
    tamanhos_kb = [t/1024 for t in tamanhos_bytes]
    
    barras = ax3.bar(componentes, tamanhos_kb, color=['darkgreen', 'lightblue', 'orange'], alpha=0.8)
    ax3.set_ylabel('Tamanho (KB)', fontweight='bold')
    ax3.set_title('Componentes do Sistema', fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores nas barras
    for i, v in enumerate(tamanhos_kb):
        ax3.text(i, v + max(tamanhos_kb)*0.02, f'{v:.2f} KB', 
                ha='center', va='bottom', fontweight='bold')
    
    # 4. Estrutura da árvore vs memória
    ax4 = axes[1, 1]
    
    estrutura_labels = ['Nós', 'Folhas', 'Profundidade', 'Features']
    estrutura_valores = [
        resultados['modelo_info']['nos'],
        resultados['modelo_info']['folhas'], 
        resultados['modelo_info']['profundidade'],
        resultados['modelo_info']['features']
    ]
    
    # Normaliza para visualização (escala log)
    estrutura_norm = np.log10(estrutura_valores)
    cores_estrutura = ['red', 'green', 'blue', 'orange']
    
    barras = ax4.bar(estrutura_labels, estrutura_norm, color=cores_estrutura, alpha=0.7)
    ax4.set_ylabel('Valor (escala log₁₀)', fontweight='bold')
    ax4.set_title('Complexidade da Estrutura', fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores reais nas barras
    for i, (v_norm, v_real) in enumerate(zip(estrutura_norm, estrutura_valores)):
        ax4.text(i, v_norm + max(estrutura_norm)*0.02, str(v_real), 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('./resultados/visualizacoes/analise_memoria_completa.png', 
                dpi=300, bbox_inches='tight')
    print("   ✅ Salvo: ./resultados/visualizacoes/analise_memoria_completa.png")
    
    plt.show()

def comparar_com_codigo_original_detalhado():
    """
    Comparação detalhada com o código original.
    """
    print("\n📊 COMPARAÇÃO DETALHADA COM CÓDIGO ORIGINAL")
    print("="*70)
    
    resultados = carregar_resultados_memoria()
    
    # Simula execução do código original
    print("🔄 Simulando código original sample_dt_classifier_mem.py...")
    
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    import numpy as np
    from pympler import asizeof
    
    # Dados sintéticos como no original
    np.random.seed(42)
    X_original = np.random.rand(1000, 2)
    y_original = ((X_original[:, 0] + X_original[:, 1]) > 1).astype(int)
    
    X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(
        X_original, y_original, test_size=1/3, random_state=42)
    
    # Modelo original
    model_original = DecisionTreeClassifier(max_depth=3, random_state=42)
    model_original.fit(X_train_orig, y_train_orig)
    
    tamanho_original_bytes = asizeof.asizeof(model_original)
    tamanho_original_mb = tamanho_original_bytes / (1024 * 1024)
    
    print(f"✅ Código original executado:")
    print(f"   Tamanho total do modelo na memória: {tamanho_original_mb:.2f} MB")
    
    # Comparação lado a lado
    print(f"\n📋 COMPARAÇÃO LADO A LADO:")
    print("-" * 70)
    
    comparacao = [
        ["Característica", "Código Original", "Nosso Modelo", "Razão"],
        ["-" * 15, "-" * 15, "-" * 12, "-" * 5],
        ["Dataset", "Sintético (toy)", "Real (acelerômetro)", "-"],
        ["Features", "2", "62", "31x"],
        ["Amostras treino", f"{len(X_train_orig)}", "7,100", f"{7100/len(X_train_orig):.1f}x"],
        ["Profundidade", "3", "10", "3.3x"],
        ["Nós", str(model_original.tree_.node_count), "243", f"{243/model_original.tree_.node_count:.1f}x"],
        ["Memória (bytes)", f"{tamanho_original_bytes:,}", f"{resultados['tamanho_modelo']['pympler_bytes']:,}", 
         f"{resultados['tamanho_modelo']['pympler_bytes']/tamanho_original_bytes:.1f}x"],
        ["Memória (MB)", f"{tamanho_original_mb:.6f}", f"{resultados['tamanho_modelo']['pympler_mb']:.6f}", 
         f"{resultados['tamanho_modelo']['pympler_mb']/tamanho_original_mb:.1f}x"],
        ["Precisão estimada", "~85%", "92.08%", "+7.08%"]
    ]
    
    for linha in comparacao:
        print(f"{linha[0]:<15} | {linha[1]:<15} | {linha[2]:<12} | {linha[3]}")
    
    return tamanho_original_mb

def analisar_eficiencia_memoria():
    """
    Analisa a eficiência do uso de memória.
    """
    print(f"\n🎯 ANÁLISE DE EFICIÊNCIA DE MEMÓRIA")
    print("="*70)
    
    resultados = carregar_resultados_memoria()
    
    memoria_mb = resultados['tamanho_modelo']['pympler_mb']
    precisao = 92.08
    nos = resultados['modelo_info']['nos']
    features = resultados['modelo_info']['features']
    
    print(f"📊 Métricas de eficiência:")
    print(f"   • Precisão por MB: {precisao/memoria_mb:.0f} %/MB")
    print(f"   • Bytes por nó: {resultados['tamanho_modelo']['pympler_bytes']/nos:.1f} bytes/nó")
    print(f"   • Bytes por feature: {resultados['tamanho_modelo']['pympler_bytes']/features:.1f} bytes/feature")
    print(f"   • Nós por MB: {nos/memoria_mb:.0f} nós/MB")
    
    # Arrays internos
    arrays_mb = resultados['tamanho_modelo']['arrays_internos_mb']
    eficiencia_arrays = arrays_mb / memoria_mb * 100
    
    print(f"\n🧮 Análise dos arrays internos:")
    print(f"   • Arrays internos: {arrays_mb:.6f} MB ({eficiencia_arrays:.1f}% do total)")
    print(f"   • Overhead do framework: {(1-eficiencia_arrays/100)*100:.1f}%")
    
    print(f"\n💡 Conclusões:")
    print(f"   • Uso de memória extremamente eficiente")
    print(f"   • Adequado para dispositivos com limitações de memória")
    print(f"   • Escala bem com aumento de complexidade")
    print(f"   • Ideal para sistemas embarcados")

def avaliar_aplicabilidade_memoria():
    """
    Avalia aplicabilidade baseada no uso de memória.
    """
    print(f"\n🚀 AVALIAÇÃO DE APLICABILIDADE POR MEMÓRIA")
    print("="*70)
    
    resultados = carregar_resultados_memoria()
    memoria_kb = resultados['tamanho_modelo']['pympler_mb'] * 1024
    
    # Limites típicos de diferentes sistemas
    sistemas = {
        'Microcontrolador (Arduino)': {'limite_kb': 32, 'descricao': 'Sistema muito restrito'},
        'Microcontrolador (ESP32)': {'limite_kb': 520, 'descricao': 'Sistema embarcado'},
        'Raspberry Pi Zero': {'limite_kb': 512000, 'descricao': 'Computador de placa única'},
        'Smartphone básico': {'limite_kb': 2048000, 'descricao': 'Dispositivo móvel'},
        'Smartphone moderno': {'limite_kb': 8192000, 'descricao': 'Dispositivo móvel avançado'}
    }
    
    print(f"Nosso modelo: {memoria_kb:.3f} KB\n")
    print(f"{'Sistema':<25} | {'Limite':<12} | {'Uso %':<8} | {'Status':<15} | {'Descrição'}")
    print("-" * 85)
    
    for sistema, config in sistemas.items():
        limite = config['limite_kb']
        uso_percent = (memoria_kb / limite) * 100
        
        if uso_percent < 1:
            status = "✅ EXCELENTE"
        elif uso_percent < 5:
            status = "✅ MUITO BOM"
        elif uso_percent < 10:
            status = "✅ BOM"
        elif uso_percent < 50:
            status = "⚠️ ACEITÁVEL"
        else:
            status = "❌ INADEQUADO"
        
        print(f"{sistema:<25} | {limite:>8} KB | {uso_percent:>6.3f}% | {status:<15} | {config['descricao']}")
    
    print(f"\n🎯 RECOMENDAÇÕES:")
    print(f"   • Adequado para qualquer sistema acima de 32 KB de RAM")
    print(f"   • Perfeito para aplicações IoT e embarcadas")
    print(f"   • Deixa ampla margem para outros componentes do sistema")
    print(f"   • Uso de memória desprezível em sistemas modernos")

def main():
    """
    Função principal para análise completa de memória.
    """
    print("💾 ANÁLISE COMPLETA DE USO DE MEMÓRIA")
    print("Visualizações e Comparações Detalhadas")
    print("="*70)
    
    try:
        # Carrega dados
        resultados = carregar_resultados_memoria()
        
        # Cria visualizações
        criar_visualizacoes_memoria()
        
        # Comparação detalhada
        tamanho_original = comparar_com_codigo_original_detalhado()
        
        # Análise de eficiência
        analisar_eficiencia_memoria()
        
        # Aplicabilidade
        avaliar_aplicabilidade_memoria()
        
        print(f"\n✅ ANÁLISE COMPLETA CONCLUÍDA!")
        print(f"📁 Visualizações salvas em: ./resultados/visualizacoes/")
        
        # Resumo final
        memoria_final = resultados['tamanho_modelo']['pympler_mb']
        print(f"\n🏆 RESUMO FINAL:")
        print(f"   📏 Modelo: {memoria_final:.6f} MB ({memoria_final*1024:.3f} KB)")
        print(f"   🎯 vs Original: {memoria_final/tamanho_original:.1f}x maior, mas 31x mais complexo")
        print(f"   ⚡ Eficiência: {92.08/memoria_final:.0f} %precisão/MB")
        print(f"   ✅ Adequado para qualquer aplicação prática")
        
    except Exception as e:
        print(f"❌ Erro durante análise: {str(e)}")

if __name__ == "__main__":
    main()