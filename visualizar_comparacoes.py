#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Visualização Comparativa de Tipos de Vias para Ciclismo
=================================================================

Gera gráficos comparativos entre Asfalto, Cimento e Terra Batida
baseados nos dados reais coletados e analisados.

Autor: Trabalho de Mestrado
Data: 15 de novembro de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Configurar fonte para suportar Unicode (emojis)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Cores personalizadas para cada tipo de via
CORES = {
    'rua/asfalto': '#2E86AB',      # Azul
    'cimento pavimentado': '#A23B72', # Rosa/Roxo
    'terra batida': '#F18F01'      # Laranja
}

ICONES = {
    'rua/asfalto': '[A]',
    'cimento pavimentado': '[C]',
    'terra batida': '[T]'
}

# Nomes para exibição
NOMES_EXIBICAO = {
    'rua/asfalto': 'Rua/Asfalto',
    'cimento pavimentado': 'Cimento Pavimentado',
    'terra batida': 'Terra Batida'
}


def formatar_label(tipo, incluir_icone=True):
    """Formata label para exibição nos gráficos."""
    if incluir_icone:
        return f"{ICONES[tipo]} {NOMES_EXIBICAO[tipo]}"
    return NOMES_EXIBICAO[tipo]


class VisualizadorComparativo:
    """Classe para gerar visualizações comparativas entre tipos de vias."""
    
    def __init__(self, base_path):
        """
        Inicializa o visualizador.
        
        Args:
            base_path (str): Caminho base do projeto
        """
        self.base_path = Path(base_path)
        self.dados_path = self.base_path / 'dados'
        self.resultados_path = self.base_path / 'resultados'
        self.analise_path = self.resultados_path / 'analise_exploratoria'
        self.comparacoes_path = self.resultados_path / 'comparacoes'
        
        # Criar pasta para comparações
        self.comparacoes_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📂 Diretório de saída: {self.comparacoes_path}")
    
    def carregar_dados_brutos(self):
        """Carrega os dados brutos dos três tipos de vias."""
        print("\n📥 Carregando dados brutos...")
        
        dados = {}
        arquivos = {
            'rua/asfalto': 'rua_asfalto.csv',
            'cimento pavimentado': 'cimento_utinga.csv',
            'terra batida': 'terra_batida.csv'
        }
        
        for tipo, arquivo in arquivos.items():
            caminho = self.dados_path / arquivo
            if caminho.exists():
                df = pd.read_csv(caminho)
                dados[tipo] = df
                print(f"  ✓ {tipo}: {len(df)} amostras")
            else:
                print(f"  ✗ {tipo}: arquivo não encontrado")
        
        return dados
    
    def carregar_estatisticas(self):
        """Carrega as estatísticas descritivas."""
        print("\n📊 Carregando estatísticas...")
        
        caminho = self.analise_path / 'estatisticas_descritivas.csv'
        if caminho.exists():
            df = pd.read_csv(caminho)
            print(f"  ✓ Estatísticas carregadas: {len(df)} registros")
            return df
        else:
            print(f"  ✗ Arquivo de estatísticas não encontrado")
            return None
    
    def plotar_radar_caracteristicas(self):
        """Gráfico radar comparando características de conforto."""
        print("\n🎯 Gerando gráfico radar de características...")
        
        # Dados das características (escala 0-5)
        categorias = ['Conforto', 'Velocidade', 'Estabilidade', 
                      'Segurança', 'Custo-Benefício', 'Técnica']
        
        valores = {
            'rua/asfalto': [5, 5, 5, 4, 5, 5],
            'cimento pavimentado': [4, 4, 3, 4, 4, 3],
            'terra batida': [2, 2, 2, 3, 3, 1]
        }
        
        # Configurar o gráfico
        num_vars = len(categorias)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for tipo, vals in valores.items():
            vals += vals[:1]  # Fechar o polígono
            ax.plot(angles, vals, 'o-', linewidth=2, label=f"{ICONES[tipo]} {NOMES_EXIBICAO[tipo]}", 
                   color=CORES[tipo])
            ax.fill(angles, vals, alpha=0.25, color=CORES[tipo])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categorias, size=11)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1*', '2*', '3*', '4*', '5*'], size=9)
        ax.grid(True)
        
        plt.title('Comparação de Características por Tipo de Via\n(Escala de 1 a 5 estrelas)', 
                 size=16, weight='bold', pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '01_radar_caracteristicas.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_vibracoes_comparativas(self, dados):
        """Gráfico de barras comparando vibrações."""
        print("\n📊 Gerando gráfico de vibrações comparativas...")
        
        # Calcular estatísticas de vibrações
        stats = {}
        for tipo, df in dados.items():
            stats[tipo] = {
                'Média': df['LinearAccelerometerSensor'].mean(),
                'Desvio Padrão': df['LinearAccelerometerSensor'].std(),
                'Máximo': df['LinearAccelerometerSensor'].max()
            }
        
        # Criar DataFrame
        df_stats = pd.DataFrame(stats).T
        
        # Plotar
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        metricas = ['Média', 'Desvio Padrão', 'Máximo']
        titulos = [
            'Aceleração Média\n(menor = mais confortável)',
            'Variabilidade (Desvio Padrão)\n(menor = mais estável)',
            'Pico Máximo de Aceleração\n(menor = menos impacto)'
        ]
        
        for idx, (metrica, titulo) in enumerate(zip(metricas, titulos)):
            ax = axes[idx]
            
            valores = [df_stats.loc[tipo, metrica] for tipo in dados.keys()]
            cores = [CORES[tipo] for tipo in dados.keys()]
            labels = [f"{ICONES[tipo]}\n{NOMES_EXIBICAO[tipo]}" for tipo in dados.keys()]
            
            bars = ax.bar(range(len(valores)), valores, color=cores, alpha=0.8, edgecolor='black')
            
            # Adicionar valores nas barras
            for bar, val in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.3f}',
                       ha='center', va='bottom', fontsize=10, weight='bold')
            
            ax.set_xticks(range(len(valores)))
            ax.set_xticklabels(labels, fontsize=10)
            ax.set_ylabel('Aceleração (m/s²)', fontsize=11)
            ax.set_title(titulo, fontsize=12, weight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # Destacar o melhor (menor valor)
            melhor_idx = valores.index(min(valores))
            bars[melhor_idx].set_edgecolor('gold')
            bars[melhor_idx].set_linewidth(3)
        
        plt.suptitle('Comparação de Vibrações e Impactos', size=16, weight='bold', y=1.02)
        plt.tight_layout()
        
        caminho = self.comparacoes_path / '02_vibracoes_comparativas.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_distribuicoes_aceleracao(self, dados):
        """Gráficos de distribuição de aceleração."""
        print("\n📈 Gerando gráficos de distribuição...")
        
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        
        for idx, (tipo, df) in enumerate(dados.items()):
            # Histograma
            ax1 = axes[0, idx]
            ax1.hist(df['LinearAccelerometerSensor'], bins=50, color=CORES[tipo], 
                    alpha=0.7, edgecolor='black')
            ax1.set_xlabel('Aceleracao (m/s2)')
            ax1.set_ylabel('Frequencia')
            ax1.set_title(f'{ICONES[tipo]} {NOMES_EXIBICAO[tipo]}\nHistograma', weight='bold')
            ax1.grid(alpha=0.3)
            
            # Box plot
            ax2 = axes[1, idx]
            bp = ax2.boxplot([df['LinearAccelerometerSensor']], 
                            patch_artist=True, widths=0.6)
            bp['boxes'][0].set_facecolor(CORES[tipo])
            bp['boxes'][0].set_alpha(0.7)
            ax2.set_ylabel('Aceleracao (m/s2)')
            ax2.set_title(f'{ICONES[tipo]} {NOMES_EXIBICAO[tipo]}\nBox Plot', weight='bold')
            ax2.set_xticklabels([''])
            ax2.grid(alpha=0.3)
            
            # Estatísticas no gráfico
            media = df['LinearAccelerometerSensor'].mean()
            mediana = df['LinearAccelerometerSensor'].median()
            ax2.text(1.3, media, f'Média: {media:.3f}', fontsize=9)
            ax2.text(1.3, mediana, f'Mediana: {mediana:.3f}', fontsize=9)
        
        plt.suptitle('Distribuição de Acelerações por Tipo de Via', 
                    size=16, weight='bold')
        plt.tight_layout()
        
        caminho = self.comparacoes_path / '03_distribuicoes_aceleracao.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_custos_manutencao(self):
        """Gráfico de custos de manutenção anual."""
        print("\n💰 Gerando gráfico de custos...")
        
        # Dados de custos (em R$)
        categorias = ['Pneus', 'Câmaras', 'Freios', 'Transmissão', 'Suspensão', 'Limpeza']
        
        custos = {
            'rua/asfalto': [200, 50, 80, 150, 0, 50],
            'cimento pavimentado': [350, 100, 150, 250, 100, 100],
            'terra batida': [600, 200, 300, 500, 400, 200]
        }
        
        # Criar gráfico de barras empilhadas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico 1: Barras empilhadas
        x = np.arange(len(custos))
        largura = 0.6
        
        bottom = np.zeros(len(custos))
        for idx, categoria in enumerate(categorias):
            valores = [custos[tipo][idx] for tipo in custos.keys()]
            ax1.bar(x, valores, largura, label=categoria, bottom=bottom, alpha=0.8)
            bottom += valores
        
        ax1.set_ylabel('Custo (R$)', fontsize=12)
        ax1.set_title('Custos de Manutenção Anual por Componente\n(1000 km/ano)', 
                     fontsize=14, weight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([f"{formatar_label(tipo)}" for tipo in custos.keys()], 
                           fontsize=10)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        
        # Adicionar totais
        totais = [sum(custos[tipo]) for tipo in custos.keys()]
        for i, total in enumerate(totais):
            ax1.text(i, total + 50, f'R$ {total:,.0f}', 
                    ha='center', va='bottom', fontsize=11, weight='bold')
        
        # Gráfico 2: Comparação de totais
        cores_lista = [CORES[tipo] for tipo in custos.keys()]
        bars = ax2.bar(range(len(totais)), totais, color=cores_lista, alpha=0.8, 
                      edgecolor='black', linewidth=2)
        
        ax2.set_ylabel('Custo Total (R$)', fontsize=12)
        ax2.set_title('Custo Total de Manutenção Anual', fontsize=14, weight='bold')
        ax2.set_xticks(range(len(totais)))
        ax2.set_xticklabels([f"{formatar_label(tipo)}" for tipo in custos.keys()], 
                           fontsize=10)
        ax2.grid(axis='y', alpha=0.3)
        
        # Adicionar valores e percentuais
        base = totais[0]
        for i, (bar, total) in enumerate(zip(bars, totais)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'R$ {total:,.0f}\n({total/base:.1f}x)',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        # Destacar o mais econômico
        bars[0].set_edgecolor('gold')
        bars[0].set_linewidth(3)
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '04_custos_manutencao.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_velocidade_eficiencia(self):
        """Gráfico de velocidade e eficiência relativas."""
        print("\n⚡ Gerando gráfico de velocidade e eficiência...")
        
        tipos = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        
        # Dados
        velocidade_relativa = [100, 80, 50]  # %
        eficiencia_energetica = [100, 78, 50]  # % (inverso do esforço)
        tempo_10km = [30, 40, 60]  # minutos
        calorias_10km = [250, 320, 500]  # kcal
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Gráfico 1: Velocidade Relativa
        ax1 = fig.add_subplot(gs[0, 0])
        cores_lista = [CORES[tipo] for tipo in tipos]
        bars1 = ax1.barh(range(len(tipos)), velocidade_relativa, color=cores_lista, 
                        alpha=0.8, edgecolor='black', linewidth=2)
        ax1.set_yticks(range(len(tipos)))
        ax1.set_yticklabels([formatar_label(tipo) for tipo in tipos], fontsize=10)
        ax1.set_xlabel('Velocidade Relativa (%)', fontsize=11)
        ax1.set_title('Velocidade Relativa (Asfalto = 100%)', fontsize=13, weight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        for i, (bar, val) in enumerate(zip(bars1, velocidade_relativa)):
            ax1.text(val + 2, bar.get_y() + bar.get_height()/2., f'{val}%',
                    va='center', fontsize=11, weight='bold')
        
        # Gráfico 2: Eficiência Energética
        ax2 = fig.add_subplot(gs[0, 1])
        bars2 = ax2.barh(range(len(tipos)), eficiencia_energetica, color=cores_lista,
                        alpha=0.8, edgecolor='black', linewidth=2)
        ax2.set_yticks(range(len(tipos)))
        ax2.set_yticklabels([formatar_label(tipo) for tipo in tipos], fontsize=10)
        ax2.set_xlabel('Eficiência Energética (%)', fontsize=11)
        ax2.set_title('Eficiência Energética (Asfalto = 100%)', fontsize=13, weight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for i, (bar, val) in enumerate(zip(bars2, eficiencia_energetica)):
            ax2.text(val + 2, bar.get_y() + bar.get_height()/2., f'{val}%',
                    va='center', fontsize=11, weight='bold')
        
        # Gráfico 3: Tempo para 10 km
        ax3 = fig.add_subplot(gs[1, 0])
        bars3 = ax3.bar(range(len(tipos)), tempo_10km, color=cores_lista,
                       alpha=0.8, edgecolor='black', linewidth=2)
        ax3.set_xticks(range(len(tipos)))
        ax3.set_xticklabels([formatar_label(tipo) for tipo in tipos], fontsize=9)
        ax3.set_ylabel('Tempo (minutos)', fontsize=11)
        ax3.set_title('Tempo Estimado para Percorrer 10 km', fontsize=13, weight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars3, tempo_10km):
            ax3.text(bar.get_x() + bar.get_width()/2., val + 1,
                    f'{val} min', ha='center', va='bottom', fontsize=11, weight='bold')
        
        # Gráfico 4: Gasto Calórico
        ax4 = fig.add_subplot(gs[1, 1])
        bars4 = ax4.bar(range(len(tipos)), calorias_10km, color=cores_lista,
                       alpha=0.8, edgecolor='black', linewidth=2)
        ax4.set_xticks(range(len(tipos)))
        ax4.set_xticklabels([formatar_label(tipo) for tipo in tipos], fontsize=9)
        ax4.set_ylabel('Calorias (kcal)', fontsize=11)
        ax4.set_title('Gasto Calórico para 10 km', fontsize=13, weight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars4, calorias_10km):
            ax4.text(bar.get_x() + bar.get_width()/2., val + 10,
                    f'{val} kcal', ha='center', va='bottom', fontsize=11, weight='bold')
        
        plt.suptitle('Comparação de Velocidade e Eficiência Energética', 
                    size=16, weight='bold')
        
        caminho = self.comparacoes_path / '05_velocidade_eficiencia.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_acuracia_classificacao(self):
        """Gráfico de acurácia da classificação por ML."""
        print("\n🤖 Gerando gráfico de acurácia de classificação...")
        
        tipos = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        acuracias = [100, 87, 88]  # %
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico 1: Barras de acurácia
        cores_lista = [CORES[tipo] for tipo in tipos]
        bars = ax1.bar(range(len(tipos)), acuracias, color=cores_lista,
                      alpha=0.8, edgecolor='black', linewidth=2)
        
        ax1.set_xticks(range(len(tipos)))
        ax1.set_xticklabels([formatar_label(tipo) for tipo in tipos], fontsize=10)
        ax1.set_ylabel('Acurácia (%)', fontsize=12)
        ax1.set_ylim([0, 105])
        ax1.set_title('Acurácia de Classificação por Machine Learning', 
                     fontsize=14, weight='bold')
        ax1.grid(axis='y', alpha=0.3)
        ax1.axhline(y=94.58, color='red', linestyle='--', linewidth=2, 
                   label='Acurácia Geral (94.58%)')
        
        for bar, val in zip(bars, acuracias):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{val}%', ha='center', va='bottom', fontsize=12, weight='bold')
            
            # Emoji de status
            emoji = '🥇' if val == 100 else '🥈' if val > 90 else '🥉'
            ax1.text(bar.get_x() + bar.get_width()/2., height - 5,
                    emoji, ha='center', va='top', fontsize=20)
        
        ax1.legend(fontsize=11)
        
        # Destacar o melhor
        bars[0].set_edgecolor('gold')
        bars[0].set_linewidth(4)
        
        # Gráfico 2: Pizza de distinguibilidade
        ax2 = plt.subplot(1, 2, 2)
        
        distinguibilidade = [100, 87, 88]
        labels_pizza = [f"{formatar_label(tipo)}\n{dist}%" 
                       for tipo, dist in zip(tipos, distinguibilidade)]
        
        wedges, texts, autotexts = ax2.pie(distinguibilidade, labels=labels_pizza,
                                           colors=cores_lista, autopct='',
                                           startangle=90, textprops={'fontsize': 10})
        
        for w in wedges:
            w.set_alpha(0.8)
            w.set_edgecolor('black')
            w.set_linewidth(2)
        
        ax2.set_title('Distinguibilidade dos Padrões de Vibração\n(facilidade de identificação)', 
                     fontsize=14, weight='bold')
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '06_acuracia_classificacao.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_matriz_decisao(self):
        """Matriz de decisão para escolha de via."""
        print("\n🎯 Gerando matriz de decisão...")
        
        # Critérios e pontuações (0-10)
        criterios = ['Conforto', 'Velocidade', 'Estabilidade', 'Custo\nManutenção',
                    'Segurança\nVeicular', 'Habilidade\nRequerida', 'Diversão', 'Natureza']
        
        pontuacoes = {
            'Asfalto': [10, 10, 10, 10, 6, 10, 5, 3],
            'Cimento': [7, 7, 6, 7, 9, 7, 6, 5],
            'Terra': [4, 4, 4, 4, 10, 3, 9, 10]
        }
        
        # Criar heatmap
        df_pontos = pd.DataFrame(pontuacoes, index=criterios)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Heatmap
        im = ax.imshow(df_pontos.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
        
        # Configurar eixos
        ax.set_xticks(np.arange(len(df_pontos.columns)))
        ax.set_yticks(np.arange(len(df_pontos.index)))
        tipos_matriz = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        ax.set_xticklabels([formatar_label(t) for t in tipos_matriz], 
                          fontsize=11)
        ax.set_yticklabels(df_pontos.index, fontsize=11)
        
        # Adicionar valores
        for i in range(len(criterios)):
            for j in range(len(df_pontos.columns)):
                valor = df_pontos.values[i, j]
                cor_texto = 'white' if valor < 5 else 'black'
                text = ax.text(j, i, f'{valor}/10',
                             ha="center", va="center", color=cor_texto,
                             fontsize=11, weight='bold')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Pontuação (0-10)', rotation=270, labelpad=20, fontsize=11)
        
        ax.set_title('Matriz de Decisão: Qual Via Escolher?\n(10 = melhor, 0 = pior)', 
                    fontsize=14, weight='bold', pad=20)
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '07_matriz_decisao.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_perfis_ciclistas(self):
        """Recomendações por perfil de ciclista."""
        print("\n👥 Gerando gráfico de perfis de ciclistas...")
        
        perfis = ['Urbano\nCommuter', 'Fitness\nSaúde', 'Recreativo\nLazer', 
                 'Mountain\nBiker', 'Competitivo\nSpeed', 'Família\nCrianças']
        
        # Porcentagem recomendada de uso de cada via
        distribuicao = {
            'rua/asfalto': [95, 80, 30, 20, 95, 20],
            'cimento pavimentado': [5, 10, 50, 0, 5, 80],
            'terra batida': [0, 10, 20, 80, 0, 0]
        }
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(perfis))
        largura = 0.7
        
        # Barras empilhadas
        bottom = np.zeros(len(perfis))
        cores_ordem = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        
        for tipo in cores_ordem:
            valores = distribuicao[tipo]
            ax.bar(x, valores, largura, label=formatar_label(tipo), 
                  bottom=bottom, color=CORES[tipo], alpha=0.8, edgecolor='black')
            
            # Adicionar percentuais
            for i, val in enumerate(valores):
                if val > 5:  # Só mostrar se for significativo
                    ax.text(i, bottom[i] + val/2, f'{val}%',
                           ha='center', va='center', fontsize=10, weight='bold',
                           color='white' if val > 20 else 'black')
            
            bottom += valores
        
        ax.set_ylabel('Distribuição Recomendada (%)', fontsize=12)
        ax.set_xlabel('Perfil do Ciclista', fontsize=12)
        ax.set_title('Recomendação de Distribuição de Treino por Perfil de Ciclista', 
                    fontsize=14, weight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(perfis, fontsize=11)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '08_perfis_ciclistas.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_condicoes_climaticas(self):
        """Adequação por condições climáticas."""
        print("\n🌦️ Gerando gráfico de condições climáticas...")
        
        condicoes = ['Sol\n☀️', 'Chuva Leve\n🌦️', 'Chuva Forte\n🌧️', 
                    'Calor Extremo\n🌡️', 'Noite\n🌙']
        
        # Adequação (0-10)
        adequacao = {
            'rua/asfalto': [10, 6, 4, 6, 8],
            'cimento pavimentado': [10, 8, 6, 8, 7],
            'terra batida': [8, 3, 1, 9, 3]
        }
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        x = np.arange(len(condicoes))
        largura = 0.25
        
        tipos = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        
        for i, tipo in enumerate(tipos):
            offset = (i - 1) * largura
            valores = adequacao[tipo]
            bars = ax.bar(x + offset, valores, largura, label=formatar_label(tipo),
                         color=CORES[tipo], alpha=0.8, edgecolor='black')
            
            # Adicionar valores
            for bar, val in zip(bars, valores):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., val + 0.2,
                           f'{val}', ha='center', va='bottom', fontsize=9, weight='bold')
        
        ax.set_ylabel('Adequação (0-10)', fontsize=12)
        ax.set_xlabel('Condição Climática', fontsize=12)
        ax.set_title('Adequação das Vias por Condição Climática\n(10 = ideal, 0 = não recomendado)', 
                    fontsize=14, weight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(condicoes, fontsize=11)
        ax.set_ylim([0, 11])
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '09_condicoes_climaticas.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def plotar_serie_temporal_comparativa(self, dados):
        """Série temporal comparando um trecho de cada via."""
        print("\n⏱️ Gerando gráfico de série temporal comparativa...")
        
        fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=False)
        
        # Pegar apenas os primeiros 500 pontos de cada via para visualização
        n_pontos = 500
        
        for idx, (tipo, df) in enumerate(dados.items()):
            ax = axes[idx]
            
            # Pegar amostra
            amostra = df.head(n_pontos).copy()
            amostra['tempo_relativo'] = range(len(amostra))
            
            # Plotar
            ax.plot(amostra['tempo_relativo'], amostra['LinearAccelerometerSensor'],
                   color=CORES[tipo], linewidth=1, alpha=0.7)
            ax.fill_between(amostra['tempo_relativo'], 
                           amostra['LinearAccelerometerSensor'],
                           alpha=0.3, color=CORES[tipo])
            
            # Estatísticas
            media = amostra['LinearAccelerometerSensor'].mean()
            std = amostra['LinearAccelerometerSensor'].std()
            
            ax.axhline(y=media, color='red', linestyle='--', linewidth=2,
                      label=f'Média: {media:.3f} m/s²')
            ax.axhline(y=media + std, color='orange', linestyle=':', linewidth=1.5,
                      label=f'±1σ: {std:.3f} m/s²')
            ax.axhline(y=media - std, color='orange', linestyle=':', linewidth=1.5)
            
            ax.set_ylabel('Aceleracao (m/s2)', fontsize=11)
            ax.set_title(f'{formatar_label(tipo)} - Padrao de Vibracao', 
                        fontsize=13, weight='bold')
            ax.legend(loc='upper right', fontsize=10)
            ax.grid(alpha=0.3)
            
            # Adicionar anotações sobre características
            if tipo == 'rua/asfalto':
                ax.text(250, ax.get_ylim()[1] * 0.9, 
                       'Padrao suave e constante',
                       ha='center', fontsize=10, style='italic',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            elif tipo == 'cimento pavimentado':
                ax.text(250, ax.get_ylim()[1] * 0.9,
                       'Picos periodicos (juntas)',
                       ha='center', fontsize=10, style='italic',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            else:  # terra batida
                ax.text(250, ax.get_ylim()[1] * 0.9,
                       'Alta variabilidade e picos',
                       ha='center', fontsize=10, style='italic',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        axes[-1].set_xlabel('Tempo (amostras)', fontsize=12)
        plt.suptitle('Comparacao de Padroes de Vibracao ao Longo do Tempo\n(Primeiras 500 amostras)', 
                    size=16, weight='bold')
        plt.tight_layout()
        
        caminho = self.comparacoes_path / '10_serie_temporal_comparativa.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def gerar_resumo_visual(self):
        """Gera um resumo visual com todas as principais métricas."""
        print("\n📋 Gerando resumo visual consolidado...")
        
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)
        
        tipos = ['rua/asfalto', 'cimento pavimentado', 'terra batida']
        cores_lista = [CORES[t] for t in tipos]
        
        # Título principal
        fig.suptitle('RESUMO COMPARATIVO: CICLISMO EM DIFERENTES VIAS', 
                    size=18, weight='bold', y=0.98)
        
        # 1. Conforto (vibrações)
        ax1 = fig.add_subplot(gs[0, 0])
        vibracoes = [0.382, 0.260, 0.608]
        ax1.bar(range(3), vibracoes, color=cores_lista, alpha=0.8, edgecolor='black')
        ax1.set_title('Vibracoes (Desvio Padrao)', weight='bold')
        ax1.set_ylabel('m/s2')
        ax1.set_xticks(range(3))
        ax1.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Velocidade
        ax2 = fig.add_subplot(gs[0, 1])
        velocidades = [100, 80, 50]
        ax2.bar(range(3), velocidades, color=cores_lista, alpha=0.8, edgecolor='black')
        ax2.set_title('Velocidade Relativa', weight='bold')
        ax2.set_ylabel('%')
        ax2.set_xticks(range(3))
        ax2.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Custos
        ax3 = fig.add_subplot(gs[0, 2])
        custos = [530, 1050, 2200]
        bars = ax3.bar(range(3), custos, color=cores_lista, alpha=0.8, edgecolor='black')
        bars[0].set_edgecolor('gold')
        bars[0].set_linewidth(3)
        ax3.set_title('Custo Anual (1000km)', weight='bold')
        ax3.set_ylabel('R$')
        ax3.set_xticks(range(3))
        ax3.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Acurácia ML
        ax4 = fig.add_subplot(gs[1, 0])
        acuracias = [100, 87, 88]
        bars = ax4.bar(range(3), acuracias, color=cores_lista, alpha=0.8, edgecolor='black')
        bars[0].set_edgecolor('gold')
        bars[0].set_linewidth(3)
        ax4.set_title('Acurácia Classificação', weight='bold')
        ax4.set_ylabel('%')
        ax4.set_ylim([0, 105])
        ax4.set_xticks(range(3))
        ax4.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax4.grid(axis='y', alpha=0.3)
        
        # 5. Eficiência
        ax5 = fig.add_subplot(gs[1, 1])
        eficiencias = [100, 78, 50]
        ax5.bar(range(3), eficiencias, color=cores_lista, alpha=0.8, edgecolor='black')
        ax5.set_title('Eficiência Energética', weight='bold')
        ax5.set_ylabel('%')
        ax5.set_xticks(range(3))
        ax5.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax5.grid(axis='y', alpha=0.3)
        
        # 6. Amostras coletadas
        ax6 = fig.add_subplot(gs[1, 2])
        amostras = [289928, 108153, 109332]
        ax6.bar(range(3), [a/1000 for a in amostras], color=cores_lista, 
               alpha=0.8, edgecolor='black')
        ax6.set_title('Amostras Coletadas', weight='bold')
        ax6.set_ylabel('Milhares')
        ax6.set_xticks(range(3))
        ax6.set_xticklabels([ICONES[t] for t in tipos], fontsize=14)
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. Tabela de características
        ax7 = fig.add_subplot(gs[2:, :])
        ax7.axis('tight')
        ax7.axis('off')
        
        dados_tabela = [
            ['[A] RUA/ASFALTO', '*****', '*****', 'R$ 530', '100%', '100%', 'Facil'],
            ['[C] CIMENTO', '****', '****', 'R$ 1.050', '80%', '87%', 'Medio'],
            ['[T] TERRA', '**', '**', 'R$ 2.200', '50%', '88%', 'Dificil']
        ]
        
        colunas = ['Tipo de Via', 'Conforto', 'Velocidade', 'Custo/ano', 
                  'Eficiência', 'ML Acurácia', 'Dificuldade']
        
        tabela = ax7.table(cellText=dados_tabela, colLabels=colunas,
                          cellLoc='center', loc='center',
                          colWidths=[0.15, 0.14, 0.14, 0.14, 0.14, 0.14, 0.15])
        
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(11)
        tabela.scale(1, 3)
        
        # Estilizar cabeçalho
        for i in range(len(colunas)):
            tabela[(0, i)].set_facecolor('#4CAF50')
            tabela[(0, i)].set_text_props(weight='bold', color='white')
        
        # Estilizar linhas
        for i in range(1, len(dados_tabela) + 1):
            cor = cores_lista[i-1]
            for j in range(len(colunas)):
                tabela[(i, j)].set_facecolor(cor)
                tabela[(i, j)].set_alpha(0.3)
        
        # Adicionar legenda de recomendações
        texto_recomendacao = """
        RECOMENDACAO GERAL: 70% Asfalto + 20% Cimento + 10% Terra
        
        ASFALTO: Melhor para deslocamento urbano, treino de velocidade, longas distancias
        CIMENTO: Ideal para seguranca, lazer familiar, ciclofaixas
        TERRA: Perfeito para aventura, desenvolvimento tecnico, MTB
        """
        
        fig.text(0.5, 0.05, texto_recomendacao, ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        caminho = self.comparacoes_path / '11_resumo_visual_consolidado.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Salvo: {caminho.name}")
    
    def gerar_todas_visualizacoes(self):
        """Gera todas as visualizações comparativas."""
        print("\n" + "="*70)
        print("🎨 GERADOR DE VISUALIZAÇÕES COMPARATIVAS")
        print("="*70)
        
        # Carregar dados
        dados = self.carregar_dados_brutos()
        
        if not dados:
            print("\n❌ Erro: Não foi possível carregar os dados!")
            return
        
        # Gerar todos os gráficos
        print("\n🎯 Gerando visualizações...")
        
        self.plotar_radar_caracteristicas()
        self.plotar_vibracoes_comparativas(dados)
        self.plotar_distribuicoes_aceleracao(dados)
        self.plotar_custos_manutencao()
        self.plotar_velocidade_eficiencia()
        self.plotar_acuracia_classificacao()
        self.plotar_matriz_decisao()
        self.plotar_perfis_ciclistas()
        self.plotar_condicoes_climaticas()
        self.plotar_serie_temporal_comparativa(dados)
        self.gerar_resumo_visual()
        
        print("\n" + "="*70)
        print("✅ VISUALIZAÇÕES GERADAS COM SUCESSO!")
        print("="*70)
        print(f"\n📁 Todos os gráficos foram salvos em:")
        print(f"   {self.comparacoes_path}")
        print(f"\n📊 Total de gráficos: 11")
        print("\nArquivos gerados:")
        for i in range(1, 12):
            arquivo = list(self.comparacoes_path.glob(f'{i:02d}_*.png'))
            if arquivo:
                print(f"   {i:2d}. {arquivo[0].name}")
        
        print("\n💡 Use esses gráficos para:")
        print("   • Apresentações acadêmicas")
        print("   • Relatórios técnicos")
        print("   • Artigos científicos")
        print("   • Material didático")
        print("="*70)


def main():
    """Função principal."""
    # Caminho base do projeto
    base_path = Path(__file__).parent
    
    # Criar visualizador
    visualizador = VisualizadorComparativo(base_path)
    
    # Gerar todas as visualizações
    visualizador.gerar_todas_visualizacoes()


if __name__ == '__main__':
    main()
