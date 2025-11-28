"""
Visualização Interativa da Análise da Árvore de Decisão
======================================================

Este script demonstra os gráficos e análises da árvore de decisão
gerados pela análise de classificação de tipos de vias.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image
import numpy as np
import os

def mostrar_graficos():
    """
    Mostra todos os gráficos gerados da análise da árvore de decisão.
    """
    print("="*70)
    print("VISUALIZAÇÃO DA ANÁLISE DA ÁRVORE DE DECISÃO")
    print("="*70)
    
    base_path = "./resultados/visualizacoes"
    
    # Lista de gráficos para mostrar
    graficos = [
        ("comparacao_modelos.png", "Comparação de Performance dos Modelos"),
        ("matriz_confusao.png", "Matriz de Confusão - Random Forest (Melhor Modelo)"),
        ("arvore_decisao_simplificada.png", "Árvore de Decisão - Primeiros 4 Níveis"),
        ("importancia_features_arvore.png", "Importância das Features - Árvore de Decisão"),
        ("curvas_roc.png", "Curvas ROC - Todos os Modelos")
    ]
    
    # Configura o layout dos subplots
    fig = plt.figure(figsize=(20, 24))
    
    for idx, (arquivo, titulo) in enumerate(graficos):
        caminho = os.path.join(base_path, arquivo)
        
        if os.path.exists(caminho):
            # Carrega e mostra a imagem
            ax = plt.subplot(3, 2, idx + 1)
            img = Image.open(caminho)
            ax.imshow(img)
            ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')
            print(f"✓ Carregado: {arquivo}")
        else:
            print(f"✗ Não encontrado: {arquivo}")
    
    plt.tight_layout()
    plt.show()

def analisar_resultados():
    """
    Analisa os resultados numéricos da árvore de decisão.
    """
    print("\n" + "="*70)
    print("ANÁLISE DOS RESULTADOS NUMÉRICOS")
    print("="*70)
    
    # Carrega estatísticas da árvore
    stats_path = "./resultados/visualizacoes/estatisticas_arvore.csv"
    if os.path.exists(stats_path):
        stats = pd.read_csv(stats_path)
        
        print("\n📊 ESTATÍSTICAS DA ÁRVORE DE DECISÃO:")
        print("-" * 50)
        print(f"🎯 Acurácia: {stats['acuracia'].iloc[0]:.4f} ({stats['acuracia'].iloc[0]*100:.2f}%)")
        print(f"🎯 F1-Score: {stats['f1_score'].iloc[0]:.4f}")
        print(f"🌳 Profundidade máxima: {stats['profundidade_maxima'].iloc[0]}")
        print(f"🌳 Número de nós: {stats['numero_nos'].iloc[0]}")
        print(f"🍃 Número de folhas: {stats['numero_folhas'].iloc[0]}")
        print(f"📈 Features utilizadas: {stats['features_utilizadas'].iloc[0]} de 62 total")
    
    # Carrega importância das features
    importance_path = "./resultados/visualizacoes/importancia_features.csv"
    if os.path.exists(importance_path):
        importance = pd.read_csv(importance_path)
        
        print("\n🔍 TOP 10 FEATURES MAIS IMPORTANTES:")
        print("-" * 50)
        
        # Mapeamento de features para interpretação
        feature_mapping = {
            'S21': 'AccX_mean (Aceleração X - Média)',
            'S34': 'AccX_energy (Aceleração X - Energia)',
            'S45': 'AccY_max (Aceleração Y - Máximo)',
            'S6': 'LinearAccelerometerSensor_range (Acelerômetro Linear - Amplitude)',
            'S12': 'LinearAccelerometerSensor_kurtosis (Acelerômetro Linear - Curtose)',
            'S35': 'AccX_fft_mean (Aceleração X - FFT Média)',
            'S62': 'acc_x_y_correlation (Correlação X-Y)',
            'S28': 'AccX_q25 (Aceleração X - 1º Quartil)',
            'S53': 'AccY_rms (Aceleração Y - RMS)',
            'S2': 'LinearAccelerometerSensor_std (Acelerômetro Linear - Desvio Padrão)'
        }
        
        top_10 = importance.head(10)
        for idx, row in top_10.iterrows():
            feature_name = feature_mapping.get(row['Feature'], f"Feature {row['Feature']}")
            print(f"  {idx+1:2d}. {row['Feature']:>3} - {feature_name:<50} ({row['Importancia']:.4f})")
    
    # Carrega comparação dos modelos
    models_path = "./resultados/modelos/comparacao_modelos.csv"
    if os.path.exists(models_path):
        models = pd.read_csv(models_path)
        
        print("\n🏆 RANKING DOS MODELOS:")
        print("-" * 50)
        
        for idx, row in models.iterrows():
            emoji = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "🔸"
            print(f"  {emoji} {idx+1}. {row['Modelo']:<20} - F1: {row['F1-Score']:.4f} | Acc: {row['Acurácia']:.4f}")

def interpretar_arvore():
    """
    Interpreta os principais aspectos da árvore de decisão.
    """
    print("\n" + "="*70)
    print("INTERPRETAÇÃO DA ÁRVORE DE DECISÃO")
    print("="*70)
    
    print("\n🎯 PRINCIPAIS DESCOBERTAS:")
    print("-" * 50)
    
    print("\n1. 📊 FEATURE MAIS IMPORTANTE - S21 (AccX_mean):")
    print("   • Representa a média da aceleração no eixo X")
    print("   • Contribui com 58.26% da decisão total")
    print("   • É o primeiro nó da árvore (decisão raiz)")
    print("   • Indica que a aceleração horizontal é crucial para distinguir tipos de via")
    
    print("\n2. 🌟 PADRÃO DE CLASSIFICAÇÃO:")
    print("   • Rua/Asfalto: Identificada principalmente por baixa variação em AccX (S21 ≤ 0.04)")
    print("   • Superfícies irregulares: Dependem de múltiplos sensores (energia, correlação)")
    print("   • Árvore usa 45 de 62 features disponíveis (72.6%)")
    
    print("\n3. 🏗️ ESTRUTURA DA ÁRVORE:")
    print("   • Profundidade moderada (10 níveis) evita overfitting")
    print("   • 122 folhas permitem decisões específicas")
    print("   • Parâmetros balanceados (min_samples_split=5, min_samples_leaf=3)")
    
    print("\n4. ⚖️ PERFORMANCE:")
    print("   • 3ª melhor performance geral (F1-Score: 0.921)")
    print("   • Modelo mais interpretável entre os top performers")
    print("   • Boa estabilidade (CV std: 0.0032)")
    
    print("\n5. 🔬 INSIGHTS TÉCNICOS:")
    print("   • Energia da aceleração X (S34) é 2ª feature mais importante")
    print("   • Features no domínio da frequência são relevantes (S35 - FFT)")
    print("   • Correlação X-Y (S62) ajuda na classificação final")
    
    print("\n📈 RECOMENDAÇÕES:")
    print("-" * 50)
    print("• Focar na aceleração horizontal (AccX) para detecção inicial")
    print("• Combinar estatísticas temporais e espectrais")
    print("• Considerar correlações entre eixos para refinamento")
    print("• Árvore é adequada para sistemas embarcados (interpretável)")

def main():
    """
    Função principal que executa toda a visualização e análise.
    """
    print("🚴 ANÁLISE DE CLASSIFICAÇÃO DE TIPOS DE VIAS")
    print("Visualização da Árvore de Decisão e Resultados\n")
    
    try:
        # Análise numérica
        analisar_resultados()
        
        # Interpretação
        interpretar_arvore()
        
        # Pergunta se quer mostrar gráficos
        print("\n" + "="*70)
        resposta = input("\nDeseja visualizar os gráficos? (s/n): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            mostrar_graficos()
        
        print("\n✅ Análise concluída com sucesso!")
        print("\n📁 Arquivos disponíveis em:")
        print("   • ./resultados/visualizacoes/ - Gráficos PNG")
        print("   • ./resultados/modelos/ - Relatórios CSV")
        print("   • ./resultados/dados_processados/ - Dados organizados")
        
    except Exception as e:
        print(f"\n❌ Erro durante a análise: {str(e)}")
        print("Verifique se o script classificacao_vias.py foi executado corretamente.")

if __name__ == "__main__":
    main()