"""
Classificação de Tipos de Vias Através de Dados de Acelerômetro
================================================================

Autor: Trabalho de Mestrado
Data: Novembro 2025

Descrição:
----------
Este script realiza o pré-processamento de dados coletados por sensores de 
acelerômetro durante passeios de bicicleta em três tipos diferentes de vias:
- Rua/Asfalto
- Cimento Pavimentado
- Terra Batida

Os dados foram coletados utilizando um smartphone Xiaomi Redmi Note 13 Pro
através do aplicativo Arduino Science Journal, capturando três sensores:
- LinearAccelerometerSensor
- AccX (Aceleração no eixo X)
- AccY (Aceleração no eixo Y)

O script implementa:
1. Leitura e pré-processamento dos dados brutos
2. Organização em formato S1, S2, Classe
3. Extração de features (estatísticas e no domínio da frequência)
4. Normalização e padronização dos dados
5. Treinamento de múltiplos modelos de classificação
6. Avaliação e comparação dos modelos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.fft import fft
from scipy.signal import welch

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix, 
                             accuracy_score, f1_score, precision_score, 
                             recall_score, roc_auc_score, roc_curve)

# Modelos de classificação
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings('ignore')

# Configuração de estilo para gráficos
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)


class DataProcessor:
    """
    Classe responsável pelo processamento e organização dos dados dos sensores.
    """
    
    def __init__(self, window_size=100, overlap=50):
        """
        Inicializa o processador de dados.
        
        Parâmetros:
        -----------
        window_size : int
            Tamanho da janela para segmentação dos dados (número de amostras)
        overlap : int
            Sobreposição entre janelas consecutivas
        """
        self.window_size = window_size
        self.overlap = overlap
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def load_data(self, file_path, class_label):
        """
        Carrega dados de um arquivo CSV e adiciona a classe correspondente.
        
        Parâmetros:
        -----------
        file_path : str
            Caminho para o arquivo CSV
        class_label : str
            Rótulo da classe (tipo de via)
            
        Retorna:
        --------
        pd.DataFrame
            DataFrame com os dados carregados e a classe
        """
        print(f"Carregando dados de: {file_path}")
        df = pd.read_csv(file_path)
        
        # Remove linhas completamente vazias
        df = df.dropna(how='all')
        
        # Preenche valores faltantes usando interpolação linear
        df['LinearAccelerometerSensor'] = df['LinearAccelerometerSensor'].interpolate(method='linear')
        df['AccX'] = df['AccX'].interpolate(method='linear')
        df['AccY'] = df['AccY'].interpolate(method='linear')
        
        # Remove quaisquer NaN restantes
        df = df.dropna()
        
        # Adiciona a classe
        df['Classe'] = class_label
        
        print(f"  -> {len(df)} amostras carregadas para classe '{class_label}'")
        return df
    
    def extract_features(self, window_data):
        """
        Extrai features estatísticas e no domínio da frequência de uma janela de dados.
        
        Parâmetros:
        -----------
        window_data : pd.DataFrame
            Janela de dados contendo as colunas dos sensores
            
        Retorna:
        --------
        dict
            Dicionário com todas as features extraídas
        """
        features = {}
        
        # Lista de sensores para extrair features
        sensors = ['LinearAccelerometerSensor', 'AccX', 'AccY']
        
        for sensor in sensors:
            data = window_data[sensor].values
            
            # Features estatísticas no domínio do tempo
            features[f'{sensor}_mean'] = np.mean(data)
            features[f'{sensor}_std'] = np.std(data)
            features[f'{sensor}_var'] = np.var(data)
            features[f'{sensor}_min'] = np.min(data)
            features[f'{sensor}_max'] = np.max(data)
            features[f'{sensor}_range'] = np.max(data) - np.min(data)
            features[f'{sensor}_median'] = np.median(data)
            features[f'{sensor}_q25'] = np.percentile(data, 25)
            features[f'{sensor}_q75'] = np.percentile(data, 75)
            features[f'{sensor}_iqr'] = features[f'{sensor}_q75'] - features[f'{sensor}_q25']
            
            # Features adicionais
            features[f'{sensor}_skewness'] = stats.skew(data)
            features[f'{sensor}_kurtosis'] = stats.kurtosis(data)
            features[f'{sensor}_rms'] = np.sqrt(np.mean(data**2))
            features[f'{sensor}_energy'] = np.sum(data**2)
            
            # Features no domínio da frequência (usando FFT)
            fft_vals = np.abs(fft(data))
            fft_vals = fft_vals[:len(fft_vals)//2]  # Apenas metade positiva
            
            features[f'{sensor}_fft_mean'] = np.mean(fft_vals)
            features[f'{sensor}_fft_std'] = np.std(fft_vals)
            features[f'{sensor}_fft_max'] = np.max(fft_vals)
            features[f'{sensor}_dominant_freq'] = np.argmax(fft_vals)
            
            # Densidade espectral de potência
            freqs, psd = welch(data, nperseg=min(len(data), 256))
            features[f'{sensor}_psd_mean'] = np.mean(psd)
            features[f'{sensor}_psd_max'] = np.max(psd)
            
        # Features combinadas entre sensores
        features['acc_magnitude'] = np.mean(np.sqrt(
            window_data['AccX']**2 + window_data['AccY']**2
        ))
        
        features['acc_x_y_correlation'] = np.corrcoef(
            window_data['AccX'].values, 
            window_data['AccY'].values
        )[0, 1]
        
        return features
    
    def create_sliding_windows(self, df):
        """
        Cria janelas deslizantes dos dados para extração de features.
        
        Parâmetros:
        -----------
        df : pd.DataFrame
            DataFrame com os dados completos
            
        Retorna:
        --------
        pd.DataFrame
            DataFrame com features extraídas (S1, S2, ..., Classe)
        """
        print(f"Criando janelas deslizantes (tamanho={self.window_size}, overlap={self.overlap})...")
        
        windows_features = []
        step_size = self.window_size - self.overlap
        
        for i in range(0, len(df) - self.window_size + 1, step_size):
            window = df.iloc[i:i + self.window_size]
            features = self.extract_features(window)
            features['Classe'] = window['Classe'].iloc[0]
            windows_features.append(features)
        
        print(f"  -> {len(windows_features)} janelas criadas")
        return pd.DataFrame(windows_features)
    
    def organize_data(self, file_paths_and_labels):
        """
        Organiza todos os dados no formato S1, S2, ..., Sn, Classe.
        
        Parâmetros:
        -----------
        file_paths_and_labels : list of tuples
            Lista de tuplas (caminho_arquivo, rótulo_classe)
            
        Retorna:
        --------
        pd.DataFrame
            DataFrame organizado com todas as features e classes
        """
        print("\n" + "="*70)
        print("INICIANDO ORGANIZAÇÃO DOS DADOS")
        print("="*70 + "\n")
        
        all_data = []
        
        # Carrega e processa cada arquivo
        for file_path, label in file_paths_and_labels:
            df = self.load_data(file_path, label)
            windowed_df = self.create_sliding_windows(df)
            all_data.append(windowed_df)
        
        # Concatena todos os dados
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Reorganiza colunas: features (S1, S2, ...) + Classe
        cols = [col for col in combined_data.columns if col != 'Classe'] + ['Classe']
        combined_data = combined_data[cols]
        
        # Renomeia colunas de features para S1, S2, ..., Sn
        feature_cols = [col for col in combined_data.columns if col != 'Classe']
        rename_dict = {old: f'S{i+1}' for i, old in enumerate(feature_cols)}
        combined_data = combined_data.rename(columns=rename_dict)
        
        # Salva mapeamento de features
        self.feature_mapping = {f'S{i+1}': old for i, old in enumerate(feature_cols)}
        
        print(f"\n{'='*70}")
        print(f"DADOS ORGANIZADOS COM SUCESSO")
        print(f"{'='*70}")
        print(f"Total de amostras: {len(combined_data)}")
        print(f"Total de features: {len(feature_cols)}")
        print(f"Classes: {combined_data['Classe'].unique()}")
        print(f"Distribuição das classes:\n{combined_data['Classe'].value_counts()}")
        
        return combined_data


class ModelTrainer:
    """
    Classe responsável pelo treinamento e avaliação dos modelos de classificação.
    """
    
    def __init__(self, random_state=42):
        """
        Inicializa o treinador de modelos.
        
        Parâmetros:
        -----------
        random_state : int
            Seed para reprodutibilidade
        """
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self, df, test_size=0.3):
        """
        Prepara os dados para treinamento (divisão treino/teste e normalização).
        
        Parâmetros:
        -----------
        df : pd.DataFrame
            DataFrame com features e classe
        test_size : float
            Proporção dos dados para teste
            
        Retorna:
        --------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        print("\n" + "="*70)
        print("PREPARANDO DADOS PARA TREINAMENTO")
        print("="*70 + "\n")
        
        # Separa features e target
        X = df.drop('Classe', axis=1)
        y = df['Classe']
        
        # Codifica labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Divisão treino/teste estratificada
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, 
            test_size=test_size, 
            random_state=self.random_state,
            stratify=y_encoded
        )
        
        # Normalização dos dados
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"Conjunto de treino: {X_train_scaled.shape[0]} amostras")
        print(f"Conjunto de teste: {X_test_scaled.shape[0]} amostras")
        print(f"Número de features: {X_train_scaled.shape[1]}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def initialize_models(self):
        """
        Inicializa os modelos de classificação a serem testados.
        """
        self.models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100, 
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                random_state=self.random_state
            ),
            'SVM (RBF)': SVC(
                kernel='rbf',
                random_state=self.random_state,
                probability=True
            ),
            'SVM (Linear)': SVC(
                kernel='linear',
                random_state=self.random_state,
                probability=True
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(
                n_neighbors=5
            ),
            'Decision Tree': DecisionTreeClassifier(
                random_state=self.random_state
            ),
            'Naive Bayes': GaussianNB(),
            'Logistic Regression': LogisticRegression(
                random_state=self.random_state,
                max_iter=1000
            )
        }
        
        print(f"\n{len(self.models)} modelos inicializados para treinamento\n")
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Treina e avalia todos os modelos.
        
        Parâmetros:
        -----------
        X_train, X_test : np.array
            Dados de treino e teste (features)
        y_train, y_test : np.array
            Labels de treino e teste
        """
        print("\n" + "="*70)
        print("TREINAMENTO E AVALIAÇÃO DOS MODELOS")
        print("="*70 + "\n")
        
        for name, model in self.models.items():
            print(f"Treinando {name}...")
            
            # Treinamento
            model.fit(X_train, y_train)
            
            # Predições
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
            
            # Validação cruzada
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, n_jobs=-1)
            
            # Métricas
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Armazena resultados
            self.results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'confusion_matrix': confusion_matrix(y_test, y_pred)
            }
            
            print(f"  -> Acurácia: {accuracy:.4f}")
            print(f"  -> F1-Score: {f1:.4f}")
            print(f"  -> CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            print()
        
        # Identifica melhor modelo
        best_model_name = max(self.results, key=lambda x: self.results[x]['f1_score'])
        self.best_model = best_model_name
        
        print("="*70)
        print(f"MELHOR MODELO: {best_model_name}")
        print(f"F1-Score: {self.results[best_model_name]['f1_score']:.4f}")
        print("="*70)
    
    def generate_report(self, y_test):
        """
        Gera relatório detalhado de todos os modelos.
        
        Parâmetros:
        -----------
        y_test : np.array
            Labels verdadeiros do conjunto de teste
        """
        print("\n\n" + "="*70)
        print("RELATÓRIO DETALHADO DE CLASSIFICAÇÃO")
        print("="*70 + "\n")
        
        # Tabela comparativa
        comparison_df = pd.DataFrame({
            'Modelo': list(self.results.keys()),
            'Acurácia': [self.results[m]['accuracy'] for m in self.results],
            'Precisão': [self.results[m]['precision'] for m in self.results],
            'Recall': [self.results[m]['recall'] for m in self.results],
            'F1-Score': [self.results[m]['f1_score'] for m in self.results],
            'CV Mean': [self.results[m]['cv_mean'] for m in self.results],
            'CV Std': [self.results[m]['cv_std'] for m in self.results]
        })
        
        comparison_df = comparison_df.sort_values('F1-Score', ascending=False)
        print(comparison_df.to_string(index=False))
        
        # Relatório detalhado do melhor modelo
        print(f"\n\n{'='*70}")
        print(f"RELATÓRIO DETALHADO - {self.best_model}")
        print("="*70 + "\n")
        
        y_pred = self.results[self.best_model]['y_pred']
        print(classification_report(
            y_test, 
            y_pred, 
            target_names=self.label_encoder.classes_
        ))
        
        return comparison_df
    
    def plot_results(self, y_test, save_path='./'):
        """
        Gera visualizações dos resultados.
        
        Parâmetros:
        -----------
        y_test : np.array
            Labels verdadeiros do conjunto de teste
        save_path : str
            Caminho para salvar as figuras
        """
        print("\nGerando visualizações...")
        
        # 1. Comparação de métricas
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        models = list(self.results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        metric_names = ['Acurácia', 'Precisão', 'Recall', 'F1-Score']
        
        for idx, (metric, name) in enumerate(zip(metrics, metric_names)):
            ax = axes[idx // 2, idx % 2]
            values = [self.results[m][metric] for m in models]
            
            bars = ax.barh(models, values, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(models))))
            ax.set_xlabel(name, fontsize=12, fontweight='bold')
            ax.set_xlim(0, 1)
            ax.grid(axis='x', alpha=0.3)
            
            # Adiciona valores nas barras
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{width:.3f}', 
                       ha='left', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{save_path}/comparacao_modelos.png', dpi=300, bbox_inches='tight')
        print(f"  -> Salvo: {save_path}/comparacao_modelos.png")
        
        # 2. Matriz de confusão do melhor modelo
        cm = self.results[self.best_model]['confusion_matrix']
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.label_encoder.classes_,
                   yticklabels=self.label_encoder.classes_,
                   cbar_kws={'label': 'Contagem'})
        plt.title(f'Matriz de Confusão - {self.best_model}', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.ylabel('Classe Verdadeira', fontsize=12, fontweight='bold')
        plt.xlabel('Classe Predita', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{save_path}/matriz_confusao.png', dpi=300, bbox_inches='tight')
        print(f"  -> Salvo: {save_path}/matriz_confusao.png")
        
        # 3. Curvas ROC (se aplicável)
        if len(self.label_encoder.classes_) <= 10:  # Limite para visualização
            fig, axes = plt.subplots(2, 4, figsize=(20, 10))
            axes = axes.flatten()
            
            for idx, (name, result) in enumerate(self.results.items()):
                if result['y_pred_proba'] is not None:
                    ax = axes[idx]
                    
                    # ROC para cada classe (One-vs-Rest)
                    for i, class_name in enumerate(self.label_encoder.classes_):
                        y_test_binary = (y_test == i).astype(int)
                        y_score = result['y_pred_proba'][:, i]
                        
                        fpr, tpr, _ = roc_curve(y_test_binary, y_score)
                        roc_auc = roc_auc_score(y_test_binary, y_score)
                        
                        ax.plot(fpr, tpr, label=f'{class_name} (AUC={roc_auc:.2f})')
                    
                    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Chance')
                    ax.set_xlabel('Taxa de Falsos Positivos', fontsize=10)
                    ax.set_ylabel('Taxa de Verdadeiros Positivos', fontsize=10)
                    ax.set_title(f'{name}', fontsize=11, fontweight='bold')
                    ax.legend(loc='lower right', fontsize=8)
                    ax.grid(alpha=0.3)
            
            # Remove subplots não utilizados
            for idx in range(len(self.results), len(axes)):
                fig.delaxes(axes[idx])
            
            plt.tight_layout()
            plt.savefig(f'{save_path}/curvas_roc.png', dpi=300, bbox_inches='tight')
            print(f"  -> Salvo: {save_path}/curvas_roc.png")
        
        plt.close('all')
        print("\nVisualizações geradas com sucesso!")


def main():
    """
    Função principal que executa todo o pipeline de processamento e classificação.
    """
    print("\n" + "="*70)
    print("CLASSIFICAÇÃO DE TIPOS DE VIAS - ANÁLISE DE ACELERÔMETRO")
    print("="*70 + "\n")
    
    # Configuração dos caminhos e classes
    base_path = '/home/augustomotta/Documentos/mestrado/Trabalho 2'
    dados_path = f'{base_path}/dados'
    resultados_path = f'{base_path}/resultados'
    
    files_and_labels = [
        (f'{dados_path}/rua_asfalto.csv', 'Rua/Asfalto'),
        (f'{dados_path}/cimento_utinga.csv', 'Cimento Pavimentado'),
        (f'{dados_path}/terra_batida.csv', 'Terra Batida')
    ]
    
    # Etapa 1: Processamento e Organização dos Dados
    processor = DataProcessor(window_size=100, overlap=50)
    organized_data = processor.organize_data(files_and_labels)
    
    # Salva dados organizados
    output_file = f'{resultados_path}/dados_processados/dados_organizados.csv'
    organized_data.to_csv(output_file, index=False)
    print(f"\nDados organizados salvos em: {output_file}\n")
    
    # Etapa 2: Treinamento dos Modelos
    trainer = ModelTrainer(random_state=42)
    X_train, X_test, y_train, y_test = trainer.prepare_data(organized_data, test_size=0.3)
    
    trainer.initialize_models()
    trainer.train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Etapa 3: Geração de Relatórios
    comparison_df = trainer.generate_report(y_test)
    
    # Salva relatório
    comparison_df.to_csv(f'{resultados_path}/modelos/comparacao_modelos.csv', index=False)
    print(f"\nRelatório salvo em: {resultados_path}/modelos/comparacao_modelos.csv")
    
    # Etapa 4: Visualizações
    trainer.plot_results(y_test, save_path=f'{resultados_path}/visualizacoes')
    
    print("\n" + "="*70)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*70 + "\n")
    
    print("Arquivos gerados:")
    print(f"\n📊 Dados Processados:")
    print(f"  → {resultados_path}/dados_processados/dados_organizados.csv")
    print(f"\n📈 Modelos:")
    print(f"  → {resultados_path}/modelos/comparacao_modelos.csv")
    print(f"\n📉 Visualizações:")
    print(f"  → {resultados_path}/visualizacoes/comparacao_modelos.png")
    print(f"  → {resultados_path}/visualizacoes/matriz_confusao.png")
    print(f"  → {resultados_path}/visualizacoes/curvas_roc.png")
    print()


if __name__ == "__main__":
    main()
