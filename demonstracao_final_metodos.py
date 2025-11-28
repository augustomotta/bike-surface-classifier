# DEMONSTRAÇÃO FINAL: Os 4 Métodos de Medição de Memória
# Versão compatível com Windows

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys
import psutil
from pympler.asizeof import asizeof

if __name__ == "__main__":
    print("=" * 80)
    print("  DEMONSTRAÇÃO DOS 4 MÉTODOS DE MEDIÇÃO DE MEMÓRIA")
    print("=" * 80)

    # Carregar dados reduzidos
    print("\n🔄 Carregando dados (amostra para demonstração)...")
    cimento = pd.read_csv('dados/cimento_utinga.csv').head(500)
    asfalto = pd.read_csv('dados/rua_asfalto.csv').head(500)
    terra = pd.read_csv('dados/terra_batida.csv').head(500)

    cimento['tipo_via'] = 'cimento'
    asfalto['tipo_via'] = 'asfalto'
    terra['tipo_via'] = 'terra'

    dados = pd.concat([cimento, asfalto, terra], ignore_index=True)
    features = ['AccX', 'AccY']
    dados_limpos = dados[features + ['tipo_via']].dropna()
    X = dados_limpos[features].values
    y = dados_limpos['tipo_via'].values

    print(f"✅ Dados carregados: {len(X)} amostras")

    # Preparar modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Treinar modelo
    modelo = DecisionTreeClassifier(max_depth=8, random_state=42)
    modelo.fit(X_train_scaled, y_train)
    y_pred = modelo.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"✅ Modelo treinado - Acurácia: {accuracy:.4f}")

    print("\n" + "=" * 80)
    print("  RESULTADOS DOS 4 MÉTODOS")
    print("=" * 80)

    # 1. SYS.GETSIZEOF
    print("\n🔸 MÉTODO 1: SYS.GETSIZEOF (Medição Superficial)")
    print("-" * 60)
    modelo_getsizeof = sys.getsizeof(modelo)
    scaler_getsizeof = sys.getsizeof(scaler)
    dados_getsizeof = sys.getsizeof(X)
    pred_getsizeof = sys.getsizeof(y_pred)

    print(f"Modelo:           {modelo_getsizeof:8,} bytes")
    print(f"Scaler:           {scaler_getsizeof:8,} bytes")
    print(f"Dados X:          {dados_getsizeof:8,} bytes")
    print(f"Predições:        {pred_getsizeof:8,} bytes")
    total_getsizeof = modelo_getsizeof + scaler_getsizeof + dados_getsizeof + pred_getsizeof
    print(f"TOTAL:            {total_getsizeof:8,} bytes")

    # 2. PYMPLER.ASIZEOF
    print("\n🔹 MÉTODO 2: PYMPLER.ASIZEOF (Medição Completa)")
    print("-" * 60)
    modelo_asizeof = asizeof(modelo)
    scaler_asizeof = asizeof(scaler)
    dados_asizeof = asizeof(X)
    pred_asizeof = asizeof(y_pred)

    print(f"Modelo:           {modelo_asizeof:8,} bytes")
    print(f"Scaler:           {scaler_asizeof:8,} bytes")
    print(f"Dados X:          {dados_asizeof:8,} bytes")
    print(f"Predições:        {pred_asizeof:8,} bytes")
    total_asizeof = modelo_asizeof + scaler_asizeof + dados_asizeof + pred_asizeof
    print(f"TOTAL:            {total_asizeof:8,} bytes")

    # 3. MEMORY-PROFILER (Resultado do programa anterior)
    print("\n🔸 MÉTODO 3: MEMORY-PROFILER (Do programa anterior)")
    print("-" * 60)
    print("Memória durante execução: ~170-220 MB")
    print("Pico de memória:          ~50 MB")
    print("Carregamento dados:       ~33.8 MB")
    print("Treinamento modelo:       ~7.0 MB")
    print("⚠️  Monitora processo completo, não objetos específicos")

    # 4. PSUTIL
    print("\n🔹 MÉTODO 4: PSUTIL (Monitoramento de Sistema)")
    print("-" * 60)
    processo = psutil.Process()
    mem_info = processo.memory_info()
    sistema = psutil.virtual_memory()

    print(f"RSS (Processo):   {mem_info.rss / 1024 / 1024:8.2f} MB")
    print(f"VMS (Virtual):    {mem_info.vms / 1024 / 1024:8.2f} MB")
    print(f"% RAM Processo:   {processo.memory_percent():8.2f}%")
    print(f"RAM Total:        {sistema.total / 1024**3:8.2f} GB")
    print(f"RAM Usada:        {sistema.percent:8.1f}%")

    print("\n" + "=" * 80)
    print("  ANÁLISE COMPARATIVA")
    print("=" * 80)

    print(f"\n📊 DIFERENÇA ENTRE MÉTODOS 1 e 2:")
    print(f"Modelo - sys.getsizeof:    {modelo_getsizeof:8,} bytes")
    print(f"Modelo - asizeof:          {modelo_asizeof:8,} bytes")
    print(f"Diferença:                 {modelo_asizeof/modelo_getsizeof:.1f}x maior")

    print(f"\nScaler - sys.getsizeof:    {scaler_getsizeof:8,} bytes")
    print(f"Scaler - asizeof:          {scaler_asizeof:8,} bytes") 
    print(f"Diferença:                 {scaler_asizeof/scaler_getsizeof:.1f}x maior")

    print(f"\nTOTAL - sys.getsizeof:     {total_getsizeof:8,} bytes")
    print(f"TOTAL - asizeof:           {total_asizeof:8,} bytes")
    print(f"Diferença:                 {total_asizeof/total_getsizeof:.1f}x maior")

    print("\n" + "=" * 80)
    print("  CONCLUSÕES E RECOMENDAÇÕES")
    print("=" * 80)

    print("""
🎯 RESUMO DOS 4 MÉTODOS:

1. SYS.GETSIZEOF:
   • Medição: SUPERFICIAL (apenas containers)
   • Velocidade: ⭐⭐⭐⭐⭐ (Muito rápida)
   • Precisão: ⭐⭐ (Baixa para ML)
   • Uso: Debug rápido, comparações básicas

2. PYMPLER.ASIZEOF:
   • Medição: COMPLETA (inclui referências)
   • Velocidade: ⭐⭐⭐ (Moderada)
   • Precisão: ⭐⭐⭐⭐⭐ (Alta)
   • Uso: Análise precisa de modelos ML ✅

3. MEMORY-PROFILER:
   • Medição: DINÂMICA (ao longo do tempo)
   • Velocidade: ⭐⭐ (Lenta, overhead)
   • Precisão: ⭐⭐⭐⭐ (Profiling)
   • Uso: Detectar vazamentos, otimização

4. PSUTIL:
   • Medição: SISTÊMICA (processo/sistema)
   • Velocidade: ⭐⭐⭐⭐ (Rápida)
   • Precisão: ⭐⭐⭐⭐ (Sistema)
   • Uso: Monitoramento produção, dashboards
""")

    print("🏆 RECOMENDAÇÃO FINAL:")
    print("   Use ASIZEOF para análise precisa de modelos ML")
    print("   (Como usado no código sample_dt_classifier_mem.py)")

    print("\n" + "=" * 80)
    print("✅ DEMONSTRAÇÃO COMPLETA FINALIZADA")
    print("=" * 80)