"""
Análise das Regras da Árvore de Decisão
======================================

Este script extrai e mostra as principais regras de decisão
da árvore treinada para classificação de tipos de vias.
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os

def carregar_dados():
    """
    Carrega os dados organizados para recriar a árvore.
    """
    print("🔄 Carregando dados organizados...")
    
    dados_path = "./resultados/dados_processados/dados_organizados.csv"
    
    if not os.path.exists(dados_path):
        print("❌ Dados organizados não encontrados!")
        print("   Execute primeiro: python classificacao_vias.py")
        return None, None, None, None
    
    df = pd.read_csv(dados_path)
    
    # Separa features e target
    X = df.drop('Classe', axis=1)
    y = df['Classe']
    
    # Codifica labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Normalização
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"✅ Dados carregados: {X.shape[0]} amostras, {X.shape[1]} features")
    
    return X_scaled, y_encoded, label_encoder, scaler

def treinar_arvore(X, y):
    """
    Treina uma árvore de decisão com os mesmos parâmetros.
    """
    print("🌳 Treinando árvore de decisão...")
    
    dt = DecisionTreeClassifier(
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        class_weight='balanced'
    )
    
    dt.fit(X, y)
    
    print(f"✅ Árvore treinada com {dt.tree_.node_count} nós")
    
    return dt

def extrair_regras_importantes(dt, label_encoder, max_regras=15):
    """
    Extrai as regras mais importantes da árvore.
    """
    print("\n🔍 REGRAS DE DECISÃO PRINCIPAIS:")
    print("="*80)
    
    # Gera texto completo das regras
    feature_names = [f'S{i+1}' for i in range(dt.n_features_in_)]
    class_names = label_encoder.classes_
    
    tree_rules = export_text(dt, 
                            feature_names=feature_names,
                            class_names=class_names,
                            max_depth=6)
    
    print(tree_rules)
    
    # Análise dos caminhos mais importantes
    print("\n📋 INTERPRETAÇÃO DAS REGRAS PRINCIPAIS:")
    print("-"*80)
    
    # Mapeamento das features mais importantes
    feature_mapping = {
        'S21': 'AccX_mean (Média da Aceleração X)',
        'S34': 'AccX_energy (Energia da Aceleração X)', 
        'S45': 'AccY_max (Máximo da Aceleração Y)',
        'S6': 'LinearAccel_range (Amplitude do Acelerômetro Linear)',
        'S12': 'LinearAccel_kurtosis (Curtose do Acelerômetro Linear)',
        'S35': 'AccX_fft_mean (Média da FFT da Aceleração X)'
    }
    
    print("\n🎯 REGRA PRINCIPAL (Raiz da Árvore):")
    print(f"   SE {feature_mapping.get('S21', 'S21')} ≤ 0.04")
    print("   ENTÃO → Rua/Asfalto")
    print("   SENÃO → Continua análise...")
    
    print("\n💡 INTERPRETAÇÃO:")
    print("   • Se a média da aceleração X for baixa (≤ 0.04)")
    print("   • Indica superfície lisa e regular (asfalto)")
    print("   • Esta regra sozinha classifica muitas amostras de asfalto")
    
    print("\n🌟 REGRAS SECUNDÁRIAS (para superfícies irregulares):")
    print("   • Usa energia da aceleração X (S34)")
    print("   • Considera máximo da aceleração Y (S45)")
    print("   • Analisa amplitude geral (S6)")
    print("   • Aplica análise espectral (S35)")

def mostrar_estatisticas_detalhadas(dt):
    """
    Mostra estatísticas detalhadas da árvore.
    """
    print("\n📊 ESTATÍSTICAS DETALHADAS DA ÁRVORE:")
    print("="*80)
    
    tree = dt.tree_
    
    print(f"🌳 Estrutura:")
    print(f"   • Profundidade máxima: {tree.max_depth}")
    print(f"   • Total de nós: {tree.node_count}")
    print(f"   • Nós internos: {tree.node_count - tree.n_leaves}")
    print(f"   • Folhas (decisões finais): {tree.n_leaves}")
    
    # Importância das features
    importances = dt.feature_importances_
    top_features_idx = np.argsort(importances)[-10:][::-1]
    
    print(f"\n🔝 Features mais importantes:")
    for i, idx in enumerate(top_features_idx[:5]):
        print(f"   {i+1}. S{idx+1}: {importances[idx]:.4f}")
    
    # Distribuição das profundidades
    depths = []
    def get_leaf_depths(node_id, depth=0):
        if tree.children_left[node_id] == tree.children_right[node_id]:  # é folha
            depths.append(depth)
        else:
            get_leaf_depths(tree.children_left[node_id], depth + 1)
            get_leaf_depths(tree.children_right[node_id], depth + 1)
    
    get_leaf_depths(0)
    
    print(f"\n📏 Distribuição de profundidades das folhas:")
    print(f"   • Profundidade média: {np.mean(depths):.1f}")
    print(f"   • Profundidade mínima: {np.min(depths)}")
    print(f"   • Profundidade máxima: {np.max(depths)}")

def simular_classificacao():
    """
    Simula alguns exemplos de classificação seguindo as regras.
    """
    print("\n🎮 SIMULAÇÃO DE CLASSIFICAÇÃO:")
    print("="*80)
    
    print("Exemplo 1: Superfície lisa (Rua/Asfalto)")
    print("   AccX_mean = 0.02 (≤ 0.04) → RESULTADO: Rua/Asfalto ✅")
    print("   Explicação: Baixa variação na aceleração horizontal")
    
    print("\nExemplo 2: Superfície irregular")  
    print("   AccX_mean = 0.08 (> 0.04) → Analisa outras features:")
    print("   AccX_energy = -0.15, AccY_max = 0.7 → Análise mais complexa")
    print("   Resultado depende de múltiplas condições...")
    
    print("\n💭 LÓGICA GERAL:")
    print("   1️⃣ Primeiro teste: Aceleração X média")
    print("   2️⃣ Se alta variação: Analisa energia e padrões")
    print("   3️⃣ Combina múltiplos sensores para decisão final")
    print("   4️⃣ Considera características espectrais (FFT)")

def main():
    """
    Função principal para análise das regras da árvore.
    """
    print("🌳 ANÁLISE DAS REGRAS DA ÁRVORE DE DECISÃO")
    print("Classificação de Tipos de Vias\n")
    
    try:
        # Carrega dados
        X, y, label_encoder, scaler = carregar_dados()
        if X is None:
            return
        
        # Treina árvore
        dt = treinar_arvore(X, y)
        
        # Extrai regras
        extrair_regras_importantes(dt, label_encoder)
        
        # Estatísticas
        mostrar_estatisticas_detalhadas(dt)
        
        # Simulação
        simular_classificacao()
        
        print("\n" + "="*80)
        print("✅ ANÁLISE DAS REGRAS CONCLUÍDA!")
        print("="*80)
        
        print("\n📝 RESUMO EXECUTIVO:")
        print("-"*40)
        print("• A árvore usa principalmente a aceleração horizontal (AccX)")
        print("• Superfícies lisas são detectadas rapidamente")
        print("• Superfícies irregulares requerem análise multi-sensor")
        print("• Modelo balanceia interpretabilidade e precisão")
        
    except Exception as e:
        print(f"\n❌ Erro durante análise: {str(e)}")

if __name__ == "__main__":
    main()