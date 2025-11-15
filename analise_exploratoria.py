"""
Análise Exploratória dos Dados - Classificação de Vias
========================================================

Script complementar para análise e visualização dos dados brutos coletados
dos sensores de acelerômetro.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuração de estilo
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (15, 10)


def load_and_analyze(file_path, label, color):
    """
    Carrega e analisa um arquivo de dados.
    """
    print(f"\n{'='*70}")
    print(f"Análise: {label}")
    print('='*70)
    
    # Carrega dados
    df = pd.read_csv(file_path)
    
    # Informações básicas
    print(f"\nNúmero de amostras: {len(df)}")
    print(f"Duração (ms): {df['relative_time'].max() - df['relative_time'].min()}")
    
    # Remove NaN para análise
    df_clean = df.dropna()
    
    # Estatísticas descritivas
    print(f"\nEstatísticas Descritivas:")
    print(df_clean[['LinearAccelerometerSensor', 'AccX', 'AccY']].describe())
    
    # Correlação entre sensores
    print(f"\nCorrelação entre sensores:")
    corr = df_clean[['LinearAccelerometerSensor', 'AccX', 'AccY']].corr()
    print(corr)
    
    return df_clean, label, color


def plot_time_series(data_list, save_path):
    """
    Plota séries temporais dos sensores para todas as vias.
    """
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    
    sensors = ['LinearAccelerometerSensor', 'AccX', 'AccY']
    sensor_names = ['Aceleração Linear', 'Aceleração X', 'Aceleração Y']
    
    for idx, (df, label, color) in enumerate(data_list):
        # Usa apenas as primeiras 1000 amostras para visualização
        df_sample = df.head(1000)
        
        for i, (sensor, name) in enumerate(zip(sensors, sensor_names)):
            ax = axes[i, idx]
            ax.plot(df_sample['relative_time'], df_sample[sensor], 
                   color=color, alpha=0.7, linewidth=0.5)
            ax.set_title(f'{name} - {label}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Tempo (ms)', fontsize=10)
            ax.set_ylabel('Aceleração (m/s²)', fontsize=10)
            ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/analise_series_temporais.png', dpi=300, bbox_inches='tight')
    print(f"\n-> Gráfico salvo: {save_path}/analise_series_temporais.png")


def plot_distributions(data_list, save_path):
    """
    Plota distribuições dos valores dos sensores.
    """
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    
    sensors = ['LinearAccelerometerSensor', 'AccX', 'AccY']
    sensor_names = ['Aceleração Linear', 'Aceleração X', 'Aceleração Y']
    
    for i, (sensor, name) in enumerate(zip(sensors, sensor_names)):
        # Histograma
        ax = axes[i, 0]
        for df, label, color in data_list:
            ax.hist(df[sensor], bins=50, alpha=0.5, label=label, color=color, density=True)
        ax.set_title(f'Distribuição - {name}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Aceleração (m/s²)', fontsize=10)
        ax.set_ylabel('Densidade', fontsize=10)
        ax.legend()
        ax.grid(alpha=0.3)
        
        # Boxplot
        ax = axes[i, 1]
        data_to_plot = [df[sensor] for df, _, _ in data_list]
        labels_plot = [label for _, label, _ in data_list]
        colors_plot = [color for _, _, color in data_list]
        
        bp = ax.boxplot(data_to_plot, labels=labels_plot, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors_plot):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax.set_title(f'Boxplot - {name}', fontsize=12, fontweight='bold')
        ax.set_ylabel('Aceleração (m/s²)', fontsize=10)
        ax.grid(alpha=0.3)
        
        # Violin plot
        ax = axes[i, 2]
        df_combined = pd.DataFrame({
            label: df[sensor] for df, label, _ in data_list
        })
        parts = ax.violinplot([df_combined[col].dropna() for col in df_combined.columns],
                              positions=range(len(data_list)),
                              showmeans=True, showmedians=True)
        
        for idx, pc in enumerate(parts['bodies']):
            pc.set_facecolor(data_list[idx][2])
            pc.set_alpha(0.6)
        
        ax.set_xticks(range(len(data_list)))
        ax.set_xticklabels([label for _, label, _ in data_list])
        ax.set_title(f'Violin Plot - {name}', fontsize=12, fontweight='bold')
        ax.set_ylabel('Aceleração (m/s²)', fontsize=10)
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/analise_distribuicoes.png', dpi=300, bbox_inches='tight')
    print(f"-> Gráfico salvo: {save_path}/analise_distribuicoes.png")


def plot_statistics_comparison(data_list, save_path):
    """
    Compara estatísticas entre as três vias.
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    sensors = ['LinearAccelerometerSensor', 'AccX', 'AccY']
    sensor_names = ['Aceleração Linear', 'Aceleração X', 'Aceleração Y']
    
    # Calcula estatísticas
    stats_data = {
        'Via': [],
        'Sensor': [],
        'Média': [],
        'Desvio Padrão': [],
        'Variância': [],
        'Mínimo': [],
        'Máximo': [],
        'Range': []
    }
    
    for df, label, _ in data_list:
        for sensor, name in zip(sensors, sensor_names):
            stats_data['Via'].append(label)
            stats_data['Sensor'].append(name)
            stats_data['Média'].append(df[sensor].mean())
            stats_data['Desvio Padrão'].append(df[sensor].std())
            stats_data['Variância'].append(df[sensor].var())
            stats_data['Mínimo'].append(df[sensor].min())
            stats_data['Máximo'].append(df[sensor].max())
            stats_data['Range'].append(df[sensor].max() - df[sensor].min())
    
    stats_df = pd.DataFrame(stats_data)
    
    # Plota comparações
    metrics = ['Média', 'Desvio Padrão', 'Variância', 'Mínimo', 'Máximo', 'Range']
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        
        pivot_data = stats_df.pivot(index='Via', columns='Sensor', values=metric)
        pivot_data.plot(kind='bar', ax=ax, rot=45)
        
        ax.set_title(f'{metric} por Via e Sensor', fontsize=12, fontweight='bold')
        ax.set_ylabel(metric, fontsize=10)
        ax.set_xlabel('Via', fontsize=10)
        ax.legend(title='Sensor', fontsize=8)
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/analise_estatisticas.png', dpi=300, bbox_inches='tight')
    print(f"-> Gráfico salvo: {save_path}/analise_estatisticas.png")
    
    # Salva tabela de estatísticas
    stats_df.to_csv(f'{save_path}/estatisticas_descritivas.csv', index=False)
    print(f"-> Tabela salva: {save_path}/estatisticas_descritivas.csv")


def plot_correlation_matrices(data_list, save_path):
    """
    Plota matrizes de correlação para cada via.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, (df, label, color) in enumerate(data_list):
        ax = axes[idx]
        
        corr = df[['LinearAccelerometerSensor', 'AccX', 'AccY']].corr()
        
        sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', 
                   center=0, vmin=-1, vmax=1, ax=ax, cbar_kws={'label': 'Correlação'})
        ax.set_title(f'Matriz de Correlação - {label}', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/analise_correlacoes.png', dpi=300, bbox_inches='tight')
    print(f"-> Gráfico salvo: {save_path}/analise_correlacoes.png")


def plot_spectral_analysis(data_list, save_path):
    """
    Análise espectral (FFT) dos sinais.
    """
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    
    sensors = ['LinearAccelerometerSensor', 'AccX', 'AccY']
    sensor_names = ['Aceleração Linear', 'Aceleração X', 'Aceleração Y']
    
    for idx, (df, label, color) in enumerate(data_list):
        # Usa uma janela de 1024 amostras
        window_size = 1024
        df_sample = df.head(window_size)
        
        for i, (sensor, name) in enumerate(zip(sensors, sensor_names)):
            ax = axes[i, idx]
            
            # FFT
            signal = df_sample[sensor].values
            fft_vals = np.fft.fft(signal)
            fft_freqs = np.fft.fftfreq(len(signal))
            
            # Apenas frequências positivas
            positive_freqs = fft_freqs[:len(fft_freqs)//2]
            positive_fft = np.abs(fft_vals[:len(fft_vals)//2])
            
            ax.plot(positive_freqs, positive_fft, color=color, linewidth=1.5)
            ax.set_title(f'{name} - {label}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Frequência Normalizada', fontsize=10)
            ax.set_ylabel('Magnitude', fontsize=10)
            ax.grid(alpha=0.3)
            ax.set_xlim(0, 0.5)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/analise_espectral.png', dpi=300, bbox_inches='tight')
    print(f"-> Gráfico salvo: {save_path}/analise_espectral.png")


def main():
    """
    Função principal da análise exploratória.
    """
    print("\n" + "="*70)
    print("ANÁLISE EXPLORATÓRIA DOS DADOS")
    print("="*70)
    
    # Caminhos dos arquivos
    base_path = '/home/augustomotta/Documentos/mestrado/Trabalho 2'
    dados_path = f'{base_path}/dados'
    resultados_path = f'{base_path}/resultados/analise_exploratoria'
    
    files = [
        (f'{dados_path}/rua_asfalto.csv', 'Rua/Asfalto', '#1f77b4'),
        (f'{dados_path}/cimento_utinga.csv', 'Cimento Pavimentado', '#ff7f0e'),
        (f'{dados_path}/terra_batida.csv', 'Terra Batida', '#2ca02c')
    ]
    
    # Carrega e analisa dados
    data_list = []
    for file_path, label, color in files:
        df, label, color = load_and_analyze(file_path, label, color)
        data_list.append((df, label, color))
    
    print("\n" + "="*70)
    print("GERANDO VISUALIZAÇÕES")
    print("="*70 + "\n")
    
    # Gera visualizações
    plot_time_series(data_list, resultados_path)
    plot_distributions(data_list, resultados_path)
    plot_statistics_comparison(data_list, resultados_path)
    plot_correlation_matrices(data_list, resultados_path)
    plot_spectral_analysis(data_list, resultados_path)
    
    print("\n" + "="*70)
    print("ANÁLISE EXPLORATÓRIA CONCLUÍDA!")
    print("="*70)
    
    print("\nArquivos gerados em: resultados/analise_exploratoria/")
    print("  1. analise_series_temporais.png")
    print("  2. analise_distribuicoes.png")
    print("  3. analise_estatisticas.png")
    print("  4. analise_correlacoes.png")
    print("  5. analise_espectral.png")
    print("  6. estatisticas_descritivas.csv")
    print()


if __name__ == "__main__":
    main()
