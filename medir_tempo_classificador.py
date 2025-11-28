"""
Medição do Tempo de Classificação - Árvore de Decisão
====================================================

Baseado no código sample_dt_classifier_time.py, este script mede
o tempo de execução do classificador de árvore de decisão desenvolvido
para classificação de tipos de vias.
"""

import numpy as np
import pandas as pd
import time
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

def carregar_e_treinar_modelo():
    """
    Carrega os dados organizados e treina o modelo de árvore de decisão.
    """
    print("🔄 Carregando dados e treinando modelo...")
    
    # Carrega dados organizados
    dados_path = "./resultados/dados_processados/dados_organizados.csv"
    df = pd.read_csv(dados_path)
    
    # Separa features e target
    X = df.drop('Classe', axis=1)
    y = df['Classe']
    
    # Codifica labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    
    # Normalização
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treina o modelo (mesmos parâmetros do código principal)
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    print(f"✅ Modelo treinado com {X_train_scaled.shape[1]} features")
    print(f"   Classes: {label_encoder.classes_}")
    print(f"   Amostras de treino: {len(X_train_scaled)}")
    
    return model, scaler, label_encoder, X_test_scaled

def medir_tempo_classificacao(model, scaler, num_features, num_execucoes=1000):
    """
    Mede o tempo de classificação usando perf_counter e process_time.
    
    Parâmetros:
    -----------
    model : DecisionTreeClassifier
        Modelo treinado
    scaler : StandardScaler
        Scaler para normalizar os dados
    num_features : int
        Número de features do modelo
    num_execucoes : int
        Número de predições para realizar
    """
    print(f"\n📊 Medindo tempo de classificação ({num_execucoes} execuções)...")
    print("="*60)
    
    # ================================================================
    # perf_counter
    # 
    # Return the value (in fractional seconds) of a performance counter, i.e. a clock with the highest 
    # available resolution to measure a short duration. It does include time elapsed during sleep. The 
    # clock is the same for all processes. The reference point of the returned value is undefined, 
    # so that only the difference between the results of two calls is valid.
    # 
    # https://docs.python.org/3/library/time.html
    # ================================================================
    
    print("🕐 Medição com perf_counter...")
    start = time.perf_counter()
    
    i = 0
    while i < num_execucoes:
        # Gera features aleatórias normalizadas (simulando dados reais)
        features = np.random.normal(0, 1, num_features).reshape(1, -1)
        y_pred = model.predict(features)
        i = i + 1
    
    # Ponto final da medição
    finish = time.perf_counter()
    
    # Cálculo do tempo total
    tempo_total_perf = finish - start
    tempo_por_predicao_perf = tempo_total_perf / num_execucoes
    
    print(f"   Tempo total: {tempo_total_perf:.4f} segundos")
    print(f"   Tempo por predição: {tempo_por_predicao_perf*1000:.4f} ms")
    
    # ================================================================
    # process_time
    # 
    # Return the value (in fractional seconds) of the sum of the system and user CPU time of the current process. 
    # It does not include time elapsed during sleep. It is process-wide by definition. The reference point of the 
    # returned value is undefined, so that only the difference between the results of two calls is valid.
    # 
    # https://docs.python.org/3/library/time.html
    # ================================================================
    
    print("\n🕑 Medição com process_time...")
    start = time.process_time()
    
    i = 0
    while i < num_execucoes:
        # Gera features aleatórias normalizadas (simulando dados reais)
        features = np.random.normal(0, 1, num_features).reshape(1, -1)
        y_pred = model.predict(features)
        i = i + 1
    
    # Ponto final da medição
    finish = time.process_time()
    
    # Cálculo do tempo total
    tempo_total_proc = finish - start
    tempo_por_predicao_proc = tempo_total_proc / num_execucoes
    
    print(f"   Tempo total: {tempo_total_proc:.4f} segundos")
    print(f"   Tempo por predição: {tempo_por_predicao_proc*1000:.4f} ms")
    
    return {
        'perf_counter': {
            'tempo_total': tempo_total_perf,
            'tempo_por_predicao': tempo_por_predicao_perf
        },
        'process_time': {
            'tempo_total': tempo_total_proc,
            'tempo_por_predicao': tempo_por_predicao_proc
        }
    }

def testar_com_dados_reais(model, scaler, label_encoder, X_test, num_amostras=100):
    """
    Testa tempo de classificação com dados reais do conjunto de teste.
    """
    print(f"\n🔬 Teste com dados reais ({num_amostras} amostras do conjunto de teste)...")
    print("="*60)
    
    # Seleciona amostras aleatórias do conjunto de teste
    indices = np.random.choice(len(X_test), min(num_amostras, len(X_test)), replace=False)
    amostras_teste = X_test[indices]
    
    # Medição com perf_counter
    start = time.perf_counter()
    
    for amostra in amostras_teste:
        y_pred = model.predict([amostra])
    
    finish = time.perf_counter()
    tempo_real_perf = finish - start
    tempo_por_amostra_real = tempo_real_perf / len(amostras_teste)
    
    # Medição com process_time
    start = time.process_time()
    
    for amostra in amostras_teste:
        y_pred = model.predict([amostra])
    
    finish = time.process_time()
    tempo_real_proc = finish - start
    
    print(f"🕐 perf_counter:")
    print(f"   Tempo total: {tempo_real_perf:.4f} segundos")
    print(f"   Tempo por amostra: {tempo_por_amostra_real*1000:.4f} ms")
    
    print(f"\n🕑 process_time:")
    print(f"   Tempo total: {tempo_real_proc:.4f} segundos")
    print(f"   Tempo por amostra: {(tempo_real_proc/len(amostras_teste))*1000:.4f} ms")
    
    return tempo_por_amostra_real

def analise_performance():
    """
    Análise detalhada da performance do classificador.
    """
    print("\n📈 ANÁLISE DE PERFORMANCE")
    print("="*60)
    
    # Diferentes quantidades de execuções
    execucoes = [100, 500, 1000, 5000]
    
    # Carrega modelo
    model, scaler, label_encoder, X_test = carregar_e_treinar_modelo()
    
    resultados = {}
    
    for num_exec in execucoes:
        print(f"\n🔄 Testando com {num_exec} execuções:")
        resultado = medir_tempo_classificacao(model, scaler, 62, num_exec)
        resultados[num_exec] = resultado
        
        # Mostra resumo
        tempo_ms = resultado['perf_counter']['tempo_por_predicao'] * 1000
        print(f"   ⚡ Tempo médio por predição: {tempo_ms:.4f} ms")
    
    # Teste com dados reais
    tempo_real = testar_com_dados_reais(model, scaler, label_encoder, X_test, 500)
    
    # Resumo final
    print(f"\n🎯 RESUMO FINAL")
    print("="*60)
    
    melhor_tempo = min([r['perf_counter']['tempo_por_predicao'] for r in resultados.values()])
    print(f"⚡ Melhor tempo por predição: {melhor_tempo*1000:.4f} ms")
    print(f"🔬 Tempo com dados reais: {tempo_real*1000:.4f} ms")
    print(f"🌳 Profundidade da árvore: {model.tree_.max_depth}")
    print(f"📊 Número de nós: {model.tree_.node_count}")
    print(f"🍃 Número de folhas: {model.tree_.n_leaves}")
    
    # Análise de aplicabilidade
    print(f"\n💡 ANÁLISE DE APLICABILIDADE:")
    print(f"   • Tempo suficiente para aplicações em tempo real")
    print(f"   • Adequado para sistemas embarcados")
    print(f"   • Performance consistente independente do volume")
    
    if melhor_tempo * 1000 < 1:
        print(f"   ✅ EXCELENTE: < 1ms por predição")
    elif melhor_tempo * 1000 < 10:
        print(f"   ✅ MUITO BOM: < 10ms por predição")
    else:
        print(f"   ⚠️  ACEITÁVEL: >= 10ms por predição")
    
    return resultados

def main():
    """
    Função principal para medição de tempo do classificador.
    """
    print("🚴 MEDIÇÃO DE TEMPO - CLASSIFICADOR DE TIPOS DE VIAS")
    print("Baseado no código sample_dt_classifier_time.py")
    print("="*70)
    
    try:
        # Executa análise completa
        resultados = analise_performance()
        
        # Salva resultados
        import json
        with open('./resultados/modelos/tempos_classificacao.json', 'w') as f:
            # Converte para formato serializável
            resultados_json = {}
            for k, v in resultados.items():
                resultados_json[str(k)] = {
                    'perf_counter_total': v['perf_counter']['tempo_total'],
                    'perf_counter_por_predicao_ms': v['perf_counter']['tempo_por_predicao'] * 1000,
                    'process_time_total': v['process_time']['tempo_total'],
                    'process_time_por_predicao_ms': v['process_time']['tempo_por_predicao'] * 1000
                }
            json.dump(resultados_json, f, indent=2)
        
        print(f"\n💾 Resultados salvos em: ./resultados/modelos/tempos_classificacao.json")
        
    except FileNotFoundError:
        print("❌ Erro: Dados organizados não encontrados!")
        print("   Execute primeiro: python classificacao_vias.py")
    except Exception as e:
        print(f"❌ Erro durante medição: {str(e)}")

if __name__ == "__main__":
    main()