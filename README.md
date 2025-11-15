# Classificação de Tipos de Vias através de Dados de Acelerômetro

## Descrição do Projeto

Este projeto implementa um sistema de classificação automática de tipos de vias (Rua/Asfalto, Cimento Pavimentado e Terra Batida) utilizando dados de acelerômetro coletados durante passeios de bicicleta.

## Problema

O objetivo é identificar automaticamente o tipo de via em que uma bicicleta está trafegando através da análise dos padrões de vibração capturados pelos sensores de acelerômetro de um smartphone.

### Cenário
- **Atividade**: Passeio de bicicleta
- **Vias analisadas**: 
  - Rua/Asfalto
  - Cimento Pavimentado
  - Terra Batida

### Equipamento Utilizado
- **Bicicleta**: HardTail Aro 29
- **Pneus**: Calibrados com 38 PSI
- **Dispositivo**: Xiaomi Redmi Note 13 Pro
- **Aplicativo**: Arduino Science Journal

### Coleta de Dados
- **Sensores capturados**:
  - LinearAccelerometerSensor (Aceleração linear total)
  - AccX (Aceleração no eixo X)
  - AccY (Aceleração no eixo Y)
- **Total de amostras coletadas**: 507.413 registros
  - Rua/Asfalto: 289.928 amostras
  - Cimento Pavimentado: 108.153 amostras
  - Terra Batida: 109.332 amostras

## Estrutura do Projeto

```
Trabalho 2/
│
├── dados/                           # Dados brutos coletados
│   ├── rua_asfalto.csv             # 289.928 amostras (~40 MB)
│   ├── cimento_utinga.csv          # 108.153 amostras (~15 MB)
│   └── terra_batida.csv            # 109.332 amostras (~15 MB)
│
├── resultados/                      # Resultados gerados
│   ├── dados_processados/          # Dados após feature extraction
│   │   └── dados_organizados.csv   # 10.144 janelas com 62 features
│   ├── modelos/                    # Modelos e métricas
│   │   ├── comparacao_modelos.csv  # 8 modelos × 7 métricas
│   │   └── *.pkl                   # Modelos treinados
│   ├── visualizacoes/              # Gráficos principais
│   │   ├── comparacao_modelos.png  # Comparação de performance
│   │   ├── matriz_confusao.png     # Matriz de confusão
│   │   └── curvas_roc.png          # Curvas ROC multiclasse
│   └── comparacoes/                # Análises comparativas
│       └── *.png                   # 11 gráficos comparativos
│
├── classificacao_vias.py           # Script principal de ML
├── analise_exploratoria.py         # Análise exploratória dos dados
├── visualizar_comparacoes.py       # Geração de gráficos comparativos
├── analise_interativa.ipynb        # Notebook Jupyter interativo
│
├── README.md                       # Este arquivo
├── RELATORIO_TRABALHO.md           # Relatório técnico completo
├── ANALISE_COMPARATIVA_VIAS.md     # Análise prática para ciclistas
├── SUMARIO_PROJETO.md              # Resumo executivo
├── GUIA_RAPIDO.md                  # Quick start guide
├── ORGANIZACAO_FINAL.md            # Documentação da estrutura
├── INDICE_NAVEGACAO.md             # Índice de navegação
│
└── requirements.txt                # Dependências do projeto
```

## Metodologia

### 1. Pré-processamento dos Dados
- **Interpolação linear** para preencher valores faltantes
- **Segmentação por janelas deslizantes** (window size = 100, overlap = 50)
- **Tratamento de dados ausentes** e inconsistências

### 2. Extração de Features (S1, S2, ..., Sn)

Para cada janela de dados, são extraídas 67 features divididas em:

#### Features Estatísticas no Domínio do Tempo (por sensor):
- Média, Desvio Padrão, Variância
- Mínimo, Máximo, Range
- Mediana, Quartis (Q25, Q75)
- Intervalo Interquartil (IQR)
- Assimetria (Skewness)
- Curtose (Kurtosis)
- RMS (Root Mean Square)
- Energia do sinal

#### Features no Domínio da Frequência (por sensor):
- Transformada Rápida de Fourier (FFT)
- Média e desvio padrão do espectro
- Frequência dominante
- Densidade espectral de potência (PSD)

#### Features Combinadas:
- Magnitude da aceleração
- Correlação entre eixos X e Y

### 3. Organização dos Dados
Os dados são organizados no formato:
```
S1, S2, S3, ..., S67, Classe
```
Onde:
- **S1 a S67**: Features extraídas
- **Classe**: Tipo de via (Rua/Asfalto, Cimento Pavimentado, Terra Batida)

### 4. Modelos de Classificação

Oito modelos de machine learning são treinados e avaliados:

1. **Random Forest** - Ensemble de árvores de decisão
2. **Gradient Boosting** - Boosting de árvores
3. **SVM (RBF)** - Support Vector Machine com kernel RBF
4. **SVM (Linear)** - Support Vector Machine linear
5. **K-Nearest Neighbors** - Classificação por vizinhança
6. **Decision Tree** - Árvore de decisão simples
7. **Naive Bayes** - Classificador probabilístico
8. **Logistic Regression** - Regressão logística

### 5. Avaliação

Os modelos são avaliados usando:
- **Acurácia** (Accuracy)
- **Precisão** (Precision)
- **Recall** (Sensibilidade)
- **F1-Score** (Média harmônica entre Precision e Recall)
- **Validação Cruzada** (5-fold Cross Validation)
- **Matriz de Confusão**
- **Curvas ROC** e AUC

## Instalação

### Pré-requisitos
- Python 3.8 ou superior

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

## Como Executar

### 1. Script Principal de Classificação

```bash
python classificacao_vias.py
```

### 2. Análise Exploratória dos Dados

```bash
python analise_exploratoria.py
```

Gera análises estatísticas detalhadas e 5 visualizações exploratórias.

### 3. Visualizações Comparativas

```bash
python visualizar_comparacoes.py
```

Cria 11 gráficos comparativos sobre as características de cada superfície.

### 4. Notebook Interativo

```bash
jupyter notebook analise_interativa.ipynb
```

Exploração interativa com 13 seções de análise.

### O que o script principal faz:

1. **Carrega os dados** dos três arquivos CSV
2. **Pré-processa** e limpa os dados
3. **Extrai features** usando janelas deslizantes
4. **Organiza** os dados no formato S1, S2, ..., Classe
5. **Treina** 8 modelos de classificação
6. **Avalia** todos os modelos
7. **Gera visualizações** e relatórios
8. **Salva resultados** em arquivos CSV e PNG

### Arquivos Gerados

Após a execução, os seguintes arquivos são criados na pasta `resultados/`:

#### Dados Processados (`resultados/dados_processados/`)
1. **dados_organizados.csv** - Dataset com 10.144 janelas e 62 features

#### Modelos e Métricas (`resultados/modelos/`)
2. **comparacao_modelos.csv** - Métricas de 8 modelos treinados
3. **random_forest_model.pkl** - Melhor modelo (94.58% acurácia)
4. Outros arquivos .pkl dos modelos treinados

#### Visualizações (`resultados/visualizacoes/`)
5. **comparacao_modelos.png** - 4 gráficos comparativos de desempenho
6. **matriz_confusao.png** - Matriz de confusão do Random Forest
7. **curvas_roc.png** - 24 curvas ROC (8 modelos × 3 classes)

#### Análises Comparativas (`resultados/comparacoes/`)
8. **11 gráficos PNG** - Análises detalhadas das superfícies

## Personalização

### Ajustar Tamanho da Janela

No arquivo `classificacao_vias.py`, modifique:

```python
processor = DataProcessor(window_size=100, overlap=50)
```

- **window_size**: Número de amostras por janela
- **overlap**: Sobreposição entre janelas consecutivas

### Alterar Proporção Treino/Teste

```python
X_train, X_test, y_train, y_test = trainer.prepare_data(organized_data, test_size=0.3)
```

- **test_size**: Proporção de dados para teste (0.3 = 30%)

### Adicionar Novos Modelos

Na classe `ModelTrainer`, método `initialize_models()`:

```python
self.models['Novo Modelo'] = NovoClassificador(parametros)
```

## Resultados Alcançados

### 🏆 Melhor Modelo: Random Forest
- **Acurácia**: 94.58%
- **F1-Score**: 94.59%
- **Tempo de Treinamento**: 5.37s
- **Tempo de Inferência**: 0.08s

### 📊 Performance por Classe
| Classe              | Precision | Recall | F1-Score |
|---------------------|-----------|--------|----------|
| Rua/Asfalto         | 100%      | 100%   | 100%     |
| Terra Batida        | 88%       | 88%    | 88%      |
| Cimento Pavimentado | 87%       | 88%    | 88%      |

### 🥇 Ranking dos Modelos (Top 3)
1. **Random Forest** - 94.58%
2. **Gradient Boosting** - 94.09%
3. **Decision Tree** - 91.43%

## Resultados Fornecidos pelo Script

O script fornece:

### 1. Relatório Comparativo
Tabela CSV com todas as métricas de desempenho dos 8 modelos

### 2. Identificação do Melhor Modelo
Automaticamente selecionado com base no F1-Score

### 3. Relatório Detalhado por Classe
Precision, Recall e F1-Score para cada tipo de via

### 4. Visualizações Completas
- Comparação visual de 7 métricas (4 gráficos)
- Matriz de confusão detalhada
- 24 curvas ROC multiclasse (8 modelos × 3 classes)
- 11 gráficos de análise comparativa das superfícies

## Interpretação dos Resultados

### Métricas Importantes:

- **Acurácia**: Percentual de predições corretas
- **F1-Score**: Equilíbrio entre precision e recall (melhor para classes desbalanceadas)
- **Matriz de Confusão**: Mostra onde o modelo erra e acerta
- **CV Score**: Valida a generalização do modelo

### Como Interpretar a Matriz de Confusão:

```
                 Predito
              A    B    C
Real    A   [TP   FN   FN]
        B   [FP   TP   FN]
        C   [FP   FP   TP]
```

- **Diagonal principal**: Predições corretas
- **Fora da diagonal**: Erros de classificação

## 📚 Documentação Disponível

O projeto possui documentação completa em múltiplos arquivos:

1. **README.md** (este arquivo) - Visão geral e instruções de uso
2. **RELATORIO_TRABALHO.md** - Relatório técnico completo (~15 seções)
3. **ANALISE_COMPARATIVA_VIAS.md** - Análise prática para ciclistas
4. **SUMARIO_PROJETO.md** - Resumo executivo com principais resultados
5. **GUIA_RAPIDO.md** - Quick start de 1 página
6. **ORGANIZACAO_FINAL.md** - Documentação da estrutura de arquivos
7. **INDICE_NAVEGACAO.md** - Índice navegável de toda documentação

## Referências Técnicas

Este trabalho foi desenvolvido como parte de um projeto de mestrado, utilizando técnicas de:

- **Processamento de Sinais**: Análise no domínio do tempo e frequência
- **Aprendizado de Máquina**: Classificação supervisionada multi-classe
- **Extração de Features**: 62 features estatísticas e espectrais
- **Validação**: Cross-validation 5-fold e métricas robustas

## Autor

Augusto Motta   
Mestrando   PPGCC   UFPa   Novembro/2025

## Licença

Este projeto é desenvolvido para fins acadêmicos.
