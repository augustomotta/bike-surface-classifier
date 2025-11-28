# 🚴‍♂️ Bike Surface Classifier

## 📋 Visão Geral

Este projeto implementa um classificador de tipos de via para ciclistas usando dados de acelerômetro. O sistema identifica automaticamente se o ciclista está pedalando em **cimento**, **asfalto** ou **terra batida** através da análise de padrões de vibração captados pelos sensores de aceleração.

## 🎯 Objetivos

- **Classificação automática** de tipos de superfície de vias urbanas
- **Análise de desempenho** de algoritmos de Machine Learning
- **Otimização de memória** e tempo de execução
- **Visualização interativa** dos resultados

## 🏗️ Arquitetura do Projeto

```text
bike-surface-classifier/
├── 📂 dados/                    # Datasets de acelerometria
│   ├── cimento_utinga.csv      # Dados coletados em via de cimento
│   ├── rua_asfalto.csv         # Dados coletados em asfalto
│   └── terra_batida.csv        # Dados coletados em terra batida
├── 📂 resultados/              # Outputs e análises geradas
│   ├── analise_exploratoria/   # Estatísticas descritivas
│   ├── comparacoes/            # Comparações de modelos
│   ├── dados_processados/      # Dados limpos e organizados
│   ├── modelos/                # Modelos treinados e métricas
│   └── visualizacoes/          # Gráficos e plots
├── 📄 classificacao_vias.py    # Script principal de classificação
├── 📄 medir_memoria_modelo.py  # Análise de uso de memória
├── 📄 medir_tempo_classificador.py # Análise de performance
├── 📄 comparar_metodos_memoria.py  # Comparação de métodos
├── 📄 demonstracao_final_metodos.py # Demo dos 4 métodos
├── 📄 analise_exploratoria.py  # Análise estatística dos dados
├── 📄 analise_interativa.ipynb # Notebook Jupyter interativo
├── 📄 visualizar_comparacoes.py # Visualizações comparativas
├── 📄 requirements.txt         # Dependências Python
├── 📄 DIFERENCIAS_METODOS_MEMORIA.md # Documentação técnica
├── 📄 RELATORIO_TRABALHO.md    # Relatório completo
└── 📄 README.md               # Este arquivo
```

## 🚀 Início Rápido

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/augustomotta/bike-surface-classifier.git
cd bike-surface-classifier

# Instale as dependências
pip install -r requirements.txt
```

### 2. Execução Principal

```bash
# Executar classificação completa
python classificacao_vias.py

# Análise de memória
python medir_memoria_modelo.py

# Análise de tempo
python medir_tempo_classificador.py

# Comparação de métodos de memória
python demonstracao_final_metodos.py
```

### 3. Análise Interativa

```bash
# Abrir notebook Jupyter
jupyter notebook analise_interativa.ipynb
```

## 📊 Resultados Principais

### 🎯 Performance do Modelo

- **Algoritmo**: Decision Tree Classifier otimizada
- **Acurácia**: ~92.08% em dados de teste
- **Tempo de predição**: ~0.1ms por amostra
- **Uso de memória**: ~2KB para o modelo completo

### 📈 Métricas por Classe

| **Tipo de Via** | **Precision** | **Recall** | **F1-Score** |
|-----------------|---------------|------------|--------------|
| Asfalto         | 0.94          | 0.95       | 0.95         |
| Cimento         | 0.89          | 0.88       | 0.88         |
| Terra Batida    | 0.93          | 0.93       | 0.93         |

### 🔧 Otimizações Implementadas

- **Balanceamento de classes** com `class_weight='balanced'`
- **Poda da árvore** com `max_depth=10`, `min_samples_split=5`
- **Normalização** dos features com StandardScaler
- **Validação cruzada** estratificada

## 🛠️ Tecnologias Utilizadas

### Core ML & Data Science

- **Python 3.8+** - Linguagem de programação
- **Scikit-learn** - Machine Learning
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica

### Visualização & Interface

- **Matplotlib** - Gráficos estáticos
- **Seaborn** - Visualização estatística
- **Plotly** - Gráficos interativos
- **Jupyter** - Notebooks interativos

### Performance & Monitoramento

- **Pympler** - Análise precisa de memória
- **Memory-profiler** - Profiling dinâmico
- **Psutil** - Monitoramento de sistema
- **Time** - Medição de performance

## 📁 Descrição dos Módulos

### 🎯 Módulos Principais

#### `classificacao_vias.py`

- **Função**: Script principal de classificação
- **Características**:
  - Carregamento e limpeza automática dos dados
  - Treinamento de Decision Tree otimizada
  - Análise completa de performance
  - Geração de visualizações e relatórios
  - Export de resultados para CSV/PNG

#### `medir_memoria_modelo.py`

- **Função**: Análise precisa de uso de memória
- **Características**:
  - Utiliza `pympler.asizeof` para medição completa
  - Análise de componentes individuais (modelo, scaler, dados)
  - Comparação com baseline
  - Relatório detalhado de otimização

#### `medir_tempo_classificador.py`

- **Função**: Benchmarking de performance temporal
- **Características**:
  - Medição de tempo de treinamento e predição
  - Análise de escalabilidade
  - Comparação entre diferentes configurações
  - Profiling detalhado por operação

### 🔬 Módulos de Análise

#### `analise_exploratoria.py`

- **Função**: Análise estatística exploratória
- **Características**:
  - Estatísticas descritivas por tipo de via
  - Detecção de outliers e missing values
  - Análise de distribuições
  - Correlações entre features

#### `comparar_metodos_memoria.py`

- **Função**: Comparação de métodos de medição
- **Características**:
  - Demonstração de 4 métodos diferentes
  - Análise comparativa de precisão
  - Recomendações de uso por contexto

#### `visualizar_comparacoes.py`

- **Função**: Dashboard de comparações visuais
- **Características**:
  - Gráficos interativos com Plotly
  - Comparação de múltiplos modelos
  - Matriz de confusão interativa
  - Export para HTML

### 📓 Interface Interativa

#### `analise_interativa.ipynb`

- **Função**: Notebook Jupyter para exploração
- **Características**:
  - Análise passo a passo documentada
  - Visualizações inline
  - Experimentação interativa
  - Possibilidade de modificação em tempo real

## 📈 Fluxo de Execução

### 1. Preparação dos Dados

```python
# Carregamento automático dos 3 datasets
dados = carregar_dados_completos()

# Limpeza e normalização
dados_limpos = preprocessar_dados(dados)

# Split estratificado
X_train, X_test, y_train, y_test = split_estratificado(dados_limpos)
```

### 2. Treinamento do Modelo

```python
# Configuração otimizada
modelo = DecisionTreeClassifier(
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=3,
    class_weight='balanced',
    random_state=42
)

# Treinamento com features normalizados
modelo.fit(X_train_scaled, y_train)
```

### 3. Avaliação e Análise

```python
# Métricas completas
accuracy, classification_report, confusion_matrix = avaliar_modelo(modelo)

# Análise de performance
tempo_predicao = medir_tempo_classificacao()
uso_memoria = medir_memoria_modelo()
```

### 4. Visualização e Relatórios

```python
# Gráficos automáticos
gerar_visualizacoes_completas()
gerar_relatorio_performance()
export_resultados_csv()
```

## 🔍 Metodologia de Desenvolvimento

### Coleta de Dados

- **Sensores**: Acelerômetro de smartphone
- **Locais**: Vias urbanas de Belém/PA
- **Frequência**: Amostragem contínua durante pedaladas
- **Tipos**: 3 superfícies distintas (cimento, asfalto, terra)

### Preprocessamento

- **Limpeza**: Remoção de valores nulos e outliers
- **Normalização**: StandardScaler para features de aceleração
- **Balanceamento**: Estratificação por tipo de via
- **Validação**: Split 70/30 com reprodutibilidade

### Seleção do Algoritmo

- **Justificativa**: Decision Trees são interpretáveis e eficientes
- **Otimização**: Grid search para hiperparâmetros
- **Validação**: Cross-validation estratificada
- **Regularização**: Poda para evitar overfitting

### Avaliação de Performance

- **Métricas**: Accuracy, Precision, Recall, F1-Score
- **Análise temporal**: Tempo de treinamento e predição
- **Análise espacial**: Uso de memória detalhado
- **Interpretabilidade**: Análise da árvore de decisão

## 📊 Análise de Resultados

### Eficácia do Modelo

- ✅ **Alta acurácia** (~92%) demonstra viabilidade
- ✅ **Balanceamento** entre classes bem equilibrado
- ✅ **Generalização** adequada sem overfitting
- ✅ **Interpretabilidade** através da árvore de decisão

### Eficiência Computacional

- ⚡ **Tempo real**: Predições em ~0.1ms
- 💾 **Baixo consumo**: Modelo com apenas ~2KB
- 🔋 **Mobile-friendly**: Adequado para dispositivos móveis
- ⚙️ **Escalável**: Linear com número de amostras

### Aplicabilidade Prática

- 🚴‍♂️ **Integração mobile**: Pode ser embarcado em apps
- 📱 **Tempo real**: Classificação instantânea durante pedalada
- 🗺️ **Mapeamento**: Base para mapeamento colaborativo de vias
- 🏙️ **Gestão urbana**: Ferramenta para planejamento cicloviário

## 🔧 Configuração Avançada

### Personalização de Parâmetros

```python
# Exemplo de configuração customizada
config = {
    'modelo': {
        'max_depth': 15,
        'min_samples_split': 3,
        'criterion': 'gini'
    },
    'preprocessamento': {
        'scaler': 'StandardScaler',
        'outlier_method': 'IQR'
    },
    'validacao': {
        'test_size': 0.25,
        'cv_folds': 5
    }
}
```

### Extensões Possíveis

1. **Novos tipos de via**: Adicionar paralelepípedo, trilha, etc.
2. **Features adicionais**: GPS, giroscópio, magnetômetro
3. **Modelos ensemble**: Random Forest, XGBoost
4. **Deep Learning**: CNN para análise de séries temporais
5. **Tempo real**: Pipeline de streaming com Apache Kafka

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o repositório
2. **Clone** sua fork localmente
3. **Crie** uma branch para sua feature
4. **Implemente** suas modificações
5. **Teste** thoroughly
6. **Submeta** um Pull Request

### Áreas de Contribuição

- 📊 **Novos algoritmos**: Implementação de outros classificadores
- 📱 **Interface mobile**: App React Native/Flutter
- 🗺️ **Geolocalização**: Integração com mapas
- 🔬 **Análise avançada**: Feature engineering mais sofisticado
- 📈 **Visualizações**: Dashboards interativos
- 🧪 **Testing**: Cobertura de testes automatizados

## 📞 Contato

- **Autor**: Augusto Motta
- **Email**: augusto.motta@example.com
- **GitHub**: [@augustomotta](https://github.com/augustomotta)
- **LinkedIn**: [Augusto Motta](https://linkedin.com/in/augustomotta)

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- **UFPA** - Universidade Federal do Pará
- **PPGCC** - Programa de Pós-Graduação em Ciência da Computação
- **Orientadores** e **colegas** pelas valiosas contribuições
- **Comunidade open-source** pelas ferramentas utilizadas

---

<div align="center">

**🚴‍♂️ Pedalando rumo à tecnologia urbana inteligente! 🏙️**

</div>