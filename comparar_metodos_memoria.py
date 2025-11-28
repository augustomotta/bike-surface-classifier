"""
Comparação de Métodos de Medição de Memória
==========================================

Este script demonstra as diferenças entre os principais métodos
de medição de memória em Python: asizeof, sys.getsizeof, 
memory-profiler e psutil.
"""

import sys
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Importa bibliotecas conforme disponibilidade
try:
    from pympler import asizeof
    ASIZEOF_DISPONIVEL = True
    print("✅ pympler.asizeof disponível")
except ImportError:
    ASIZEOF_DISPONIVEL = False
    print("❌ pympler.asizeof não disponível")

try:
    from memory_profiler import profile, memory_usage
    MEMORY_PROFILER_DISPONIVEL = True
    print("✅ memory-profiler disponível")
except ImportError:
    MEMORY_PROFILER_DISPONIVEL = False
    print("❌ memory-profiler não disponível")

try:
    import psutil
    PSUTIL_DISPONIVEL = True
    print("✅ psutil disponível")
except ImportError:
    PSUTIL_DISPONIVEL = False
    print("❌ psutil não disponível")

def criar_objetos_teste():
    """
    Cria diferentes tipos de objetos para testar os métodos.
    """
    # Objetos simples
    numero = 42
    string = "Teste de string"
    lista_pequena = [1, 2, 3, 4, 5]
    lista_grande = list(range(10000))
    
    # Arrays NumPy
    array_pequeno = np.array([1, 2, 3, 4, 5])
    array_grande = np.random.rand(10000)
    
    # DataFrame
    df = pd.DataFrame({
        'A': np.random.rand(1000),
        'B': np.random.rand(1000),
        'C': np.random.randint(0, 100, 1000)
    })
    
    # Modelo de Machine Learning
    X = np.random.rand(1000, 10)
    y = np.random.randint(0, 3, 1000)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_scaled, y)
    
    return {
        'numero': numero,
        'string': string,
        'lista_pequena': lista_pequena,
        'lista_grande': lista_grande,
        'array_pequeno': array_pequeno,
        'array_grande': array_grande,
        'dataframe': df,
        'scaler': scaler,
        'modelo_ml': model
    }

def comparar_sys_getsizeof_vs_asizeof():
    """
    Compara sys.getsizeof com pympler.asizeof
    """
    print("\n" + "="*70)
    print("1. COMPARAÇÃO: sys.getsizeof vs pympler.asizeof")
    print("="*70)
    
    objetos = criar_objetos_teste()
    
    print(f"{'Objeto':<15} | {'sys.getsizeof':<15} | {'asizeof':<15} | {'Diferença':<15} | {'Razão'}")
    print("-" * 80)
    
    for nome, obj in objetos.items():
        size_sys = sys.getsizeof(obj)
        
        if ASIZEOF_DISPONIVEL:
            size_asizeof = asizeof.asizeof(obj)
            diferenca = size_asizeof - size_sys
            razao = size_asizeof / size_sys if size_sys > 0 else 0
            print(f"{nome:<15} | {size_sys:>12} B | {size_asizeof:>12} B | {diferenca:>12} B | {razao:>6.1f}x")
        else:
            print(f"{nome:<15} | {size_sys:>12} B | {'N/A':<15} | {'N/A':<15} | {'N/A'}")
    
    print("\n📊 CARACTERÍSTICAS:")
    print("🔸 sys.getsizeof:")
    print("   • Mede apenas o tamanho do OBJETO em si")
    print("   • NÃO inclui objetos referenciados")
    print("   • Rápido e eficiente")
    print("   • Pode subestimar tamanhos reais")
    print("   • Exemplo: lista [1,2,3] → tamanho da estrutura da lista, não dos elementos")
    
    if ASIZEOF_DISPONIVEL:
        print("\n🔸 pympler.asizeof:")
        print("   • Mede o tamanho TOTAL incluindo referências")
        print("   • Percorre recursivamente todos os objetos")
        print("   • Mais lento mas mais preciso")
        print("   • Mostra o uso real de memória")
        print("   • Exemplo: lista [1,2,3] → estrutura + elementos + overhead")

def demonstrar_memory_profiler():
    """
    Demonstra o uso do memory-profiler
    """
    print("\n" + "="*70)
    print("2. MEMORY-PROFILER: Profiling de Funções")
    print("="*70)
    
    if not MEMORY_PROFILER_DISPONIVEL:
        print("❌ memory-profiler não disponível")
        print("   Instale com: pip install memory-profiler")
        return
    
    def funcao_intensiva_memoria():
        """Função que usa muita memória para demonstração"""
        # Cria arrays grandes
        array1 = np.random.rand(100000)
        array2 = np.random.rand(100000) 
        array3 = array1 + array2
        
        # Cria DataFrame grande
        df = pd.DataFrame({
            'col1': array1,
            'col2': array2,
            'col3': array3
        })
        
        return df.sum().sum()
    
    print("🔄 Medindo uso de memória durante execução da função...")
    
    # Mede o uso de memória da função
    mem_usage = memory_usage((funcao_intensiva_memoria, ()))
    
    print(f"📈 Uso de memória:")
    print(f"   • Máximo: {max(mem_usage):.2f} MB")
    print(f"   • Mínimo: {min(mem_usage):.2f} MB")
    print(f"   • Diferença: {max(mem_usage) - min(mem_usage):.2f} MB")
    print(f"   • Amostras: {len(mem_usage)} medições")
    
    print("\n📊 CARACTERÍSTICAS do memory-profiler:")
    print("🔸 Funcionalidades:")
    print("   • Monitora uso de memória ao longo do TEMPO")
    print("   • Pode fazer profiling linha por linha (@profile)")
    print("   • Mede memória RSS (Resident Set Size)")
    print("   • Ideal para detectar vazamentos de memória")
    print("   • Mostra picos de uso durante execução")
    
    print("\n🔸 Limitações:")
    print("   • Overhead de monitoramento")
    print("   • Não mede objetos específicos")
    print("   • Dependente do sistema operacional")

def demonstrar_psutil():
    """
    Demonstra o uso do psutil para monitoramento de sistema
    """
    print("\n" + "="*70)
    print("3. PSUTIL: Monitoramento de Sistema")
    print("="*70)
    
    if not PSUTIL_DISPONIVEL:
        print("❌ psutil não disponível")
        print("   Instale com: pip install psutil")
        return
    
    import os
    
    # Informações do processo atual
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    mem_percent = process.memory_percent()
    
    print(f"💻 INFORMAÇÕES DO PROCESSO ATUAL:")
    print(f"   • PID: {process.pid}")
    print(f"   • RSS (Resident Set Size): {mem_info.rss / (1024*1024):.2f} MB")
    print(f"   • VMS (Virtual Memory Size): {mem_info.vms / (1024*1024):.2f} MB")
    print(f"   • Percentual da RAM: {mem_percent:.2f}%")
    
    # Informações do sistema
    virtual_mem = psutil.virtual_memory()
    
    print(f"\n🖥️  INFORMAÇÕES DO SISTEMA:")
    print(f"   • RAM Total: {virtual_mem.total / (1024**3):.2f} GB")
    print(f"   • RAM Disponível: {virtual_mem.available / (1024**3):.2f} GB")
    print(f"   • RAM Usada: {virtual_mem.used / (1024**3):.2f} GB")
    print(f"   • Percentual usado: {virtual_mem.percent:.1f}%")
    
    # Teste de criação de objeto e monitoramento
    print(f"\n🔄 Teste: Criando objeto grande...")
    mem_antes = process.memory_info().rss / (1024*1024)
    
    # Cria objeto que consome memória
    objeto_grande = np.random.rand(1000000)  # ~8MB
    
    mem_depois = process.memory_info().rss / (1024*1024)
    incremento = mem_depois - mem_antes
    
    print(f"   • Memória antes: {mem_antes:.2f} MB")
    print(f"   • Memória depois: {mem_depois:.2f} MB")
    print(f"   • Incremento: {incremento:.2f} MB")
    
    # Libera memória
    del objeto_grande
    
    print("\n📊 CARACTERÍSTICAS do psutil:")
    print("🔸 Funcionalidades:")
    print("   • Monitora PROCESSOS e SISTEMA inteiro")
    print("   • Informações em tempo real")
    print("   • Cross-platform (Windows, Linux, macOS)")
    print("   • Monitora CPU, memória, disco, rede")
    print("   • Útil para análise de performance geral")
    
    print("\n🔸 Métricas de Memória:")
    print("   • RSS: Memória física realmente usada")
    print("   • VMS: Memória virtual total do processo")
    print("   • Percentual: Quanto do total de RAM está sendo usado")

def comparacao_pratica_modelos():
    """
    Comparação prática com modelos de ML usando todos os métodos
    """
    print("\n" + "="*70)
    print("4. COMPARAÇÃO PRÁTICA: Modelo de ML")
    print("="*70)
    
    # Cria modelo similar ao do projeto
    dados_path = "./resultados/dados_processados/dados_organizados.csv"
    
    try:
        df = pd.read_csv(dados_path)
        X = df.drop('Classe', axis=1).iloc[:1000]  # Amostra menor para teste
        y = df['Classe'].iloc[:1000]
        
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = DecisionTreeClassifier(max_depth=10, random_state=42)
        model.fit(X_scaled, y_encoded)
        
        print("📊 RESULTADOS PARA O MODELO DE CLASSIFICAÇÃO:")
        
        # 1. sys.getsizeof
        size_sys = sys.getsizeof(model)
        print(f"\n🔸 sys.getsizeof:")
        print(f"   Modelo: {size_sys} bytes")
        
        # 2. asizeof
        if ASIZEOF_DISPONIVEL:
            size_asizeof = asizeof.asizeof(model)
            print(f"\n🔸 pympler.asizeof:")
            print(f"   Modelo: {size_asizeof:,} bytes ({size_asizeof/(1024*1024):.6f} MB)")
            print(f"   Diferença vs sys: {size_asizeof/size_sys:.1f}x maior")
        
        # 3. psutil
        if PSUTIL_DISPONIVEL:
            process = psutil.Process()
            mem_info = process.memory_info()
            print(f"\n🔸 psutil (processo completo):")
            print(f"   RSS: {mem_info.rss/(1024*1024):.2f} MB")
            print(f"   VMS: {mem_info.vms/(1024*1024):.2f} MB")
        
        # 4. memory-profiler (simulado)
        if MEMORY_PROFILER_DISPONIVEL:
            def treinar_modelo():
                model_temp = DecisionTreeClassifier(max_depth=10, random_state=42)
                model_temp.fit(X_scaled, y_encoded)
                return model_temp
            
            mem_usage = memory_usage((treinar_modelo, ()))
            print(f"\n🔸 memory-profiler (durante treinamento):")
            print(f"   Pico de memória: {max(mem_usage):.2f} MB")
            print(f"   Memória base: {min(mem_usage):.2f} MB")
        
    except FileNotFoundError:
        print("❌ Arquivo de dados não encontrado")
        print("   Execute primeiro: python classificacao_vias.py")

def resumo_comparativo():
    """
    Resumo das diferenças entre os métodos
    """
    print("\n" + "="*70)
    print("5. RESUMO COMPARATIVO DOS MÉTODOS")
    print("="*70)
    
    print(f"{'Método':<18} | {'Foco':<20} | {'Precisão':<10} | {'Performance':<12} | {'Uso Principal'}")
    print("-" * 95)
    print(f"{'sys.getsizeof':<18} | {'Objeto específico':<20} | {'Básica':<10} | {'Muito alta':<12} | {'Debug rápido'}")
    print(f"{'asizeof':<18} | {'Objeto + referências':<20} | {'Alta':<10} | {'Média':<12} | {'Análise precisa'}")
    print(f"{'memory-profiler':<18} | {'Execução/tempo':<20} | {'Alta':<10} | {'Baixa':<12} | {'Profiling'}")
    print(f"{'psutil':<18} | {'Sistema/processo':<20} | {'Alta':<10} | {'Alta':<12} | {'Monitoramento'}")
    
    print(f"\n💡 QUANDO USAR CADA MÉTODO:")
    print(f"🔸 sys.getsizeof:")
    print(f"   • Comparar tamanhos básicos entre objetos")
    print(f"   • Debug rápido e simples")
    print(f"   • Quando performance é crítica")
    print(f"   • Exemplo: Escolher entre list vs tuple")
    
    print(f"\n🔸 pympler.asizeof:")
    print(f"   • Análise precisa de uso de memória")
    print(f"   • Otimização de estruturas de dados complexas")
    print(f"   • Medição de modelos de ML")
    print(f"   • Exemplo: Tamanho real de um DataFrame")
    
    print(f"\n🔸 memory-profiler:")
    print(f"   • Detectar vazamentos de memória")
    print(f"   • Otimizar algoritmos")
    print(f"   • Profiling linha por linha")
    print(f"   • Exemplo: Analisar crescimento de memória em loops")
    
    print(f"\n🔸 psutil:")
    print(f"   • Monitoramento de aplicações em produção")
    print(f"   • Análise de performance do sistema")
    print(f"   • Alertas de uso de recursos")
    print(f"   • Exemplo: Dashboard de monitoramento")
    
    print(f"\n🎯 RECOMENDAÇÃO PARA O PROJETO:")
    print(f"   • Use asizeof para medir modelos ML (mais preciso)")
    print(f"   • Use sys.getsizeof para comparações rápidas")
    print(f"   • Use memory-profiler para otimizar treinamento")
    print(f"   • Use psutil para monitorar aplicação completa")

def main():
    """
    Função principal que executa todas as comparações
    """
    print("🔍 COMPARAÇÃO DE MÉTODOS DE MEDIÇÃO DE MEMÓRIA")
    print("sys.getsizeof vs asizeof vs memory-profiler vs psutil")
    print("="*70)
    
    # Executa todas as comparações
    comparar_sys_getsizeof_vs_asizeof()
    demonstrar_memory_profiler()
    demonstrar_psutil()
    comparacao_pratica_modelos()
    resumo_comparativo()
    
    print(f"\n✅ ANÁLISE COMPARATIVA CONCLUÍDA!")
    print(f"💡 Cada método tem seu propósito específico - escolha baseado na necessidade")

if __name__ == "__main__":
    main()