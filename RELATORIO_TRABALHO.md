# Relatório do Trabalho: Classificação de Tipos de Vias

## Resumo Executivo

Este trabalho desenvolveu um sistema de classificação automática de tipos de vias (Rua/Asfalto, Cimento Pavimentado e Terra Batida) utilizando dados de acelerômetro coletados durante passeios de bicicleta. O melhor modelo alcançou **94.58% de acurácia** utilizando Random Forest.

---

## 1. Introdução

### 1.1 Contextualização
A identificação automática do tipo de superfície por onde um veículo trafega pode ter diversas aplicações práticas, como:
- Sistemas de navegação inteligentes
- Monitoramento de infraestrutura urbana
- Aplicativos de ciclismo e fitness
- Manutenção preditiva de veículos

### 1.2 Objetivos
- Desenvolver um sistema de classificação de vias usando dados de sensores
- Implementar técnicas de processamento de sinais e extração de features
- Comparar múltiplos algoritmos de machine learning
- Avaliar a viabilidade prática da solução

---

## 2. Metodologia

### 2.1 Coleta de Dados

**Equipamento:**
- Dispositivo: Xiaomi Redmi Note 13 Pro
- Aplicativo: Arduino Science Journal
- Atividade: Passeio de bicicleta

**Sensores Capturados:**
- LinearAccelerometerSensor (Aceleração linear total)
- AccX (Aceleração no eixo X - horizontal)
- AccY (Aceleração no eixo Y - vertical)

**Classes (Tipos de Via):**
1. **Rua/Asfalto**: Via pavimentada regular (289.928 amostras)
2. **Cimento Pavimentado**: Calçada de cimento (108.153 amostras)
3. **Terra Batida**: Via não pavimentada (109.332 amostras)

### 2.2 Pré-processamento

#### Limpeza de Dados
- Remoção de linhas completamente vazias
- Interpolação linear para valores faltantes
- Remoção de NaN residuais

#### Segmentação por Janelas
- **Tamanho da janela**: 100 amostras
- **Sobreposição**: 50 amostras (50%)
- **Total de janelas geradas**: 10.144
  - Rua/Asfalto: 5.797 janelas
  - Terra Batida: 2.185 janelas
  - Cimento Pavimentado: 2.162 janelas

### 2.3 Extração de Features

Para cada janela de 100 amostras, foram extraídas **62 features** divididas em:

#### Features Estatísticas (por sensor):
- Medidas de tendência central: média, mediana
- Medidas de dispersão: desvio padrão, variância, IQR
- Valores extremos: mínimo, máximo, range
- Forma da distribuição: assimetria, curtose
- Energia do sinal: RMS, energia total

#### Features no Domínio da Frequência (por sensor):
- Transformada Rápida de Fourier (FFT)
- Estatísticas do espectro de frequência
- Frequência dominante
- Densidade espectral de potência (PSD)

#### Features Combinadas:
- Magnitude da aceleração vetorial
- Correlação entre eixos X e Y

### 2.4 Organização dos Dados

Os dados foram organizados no formato:

```
S1, S2, S3, ..., S62, Classe
```

Onde cada S_i representa uma feature extraída.

**Divisão dos Dados:**
- Conjunto de treino: 70% (7.100 amostras)
- Conjunto de teste: 30% (3.044 amostras)
- Estratificação por classe mantida

---

## 3. Modelos de Classificação

### 3.1 Algoritmos Testados

Oito algoritmos de machine learning foram implementados e avaliados:

1. **Random Forest**: Ensemble de 100 árvores de decisão
2. **Gradient Boosting**: Boosting sequencial de árvores
3. **SVM (RBF)**: Support Vector Machine com kernel radial
4. **SVM (Linear)**: Support Vector Machine linear
5. **K-Nearest Neighbors**: Classificação por k=5 vizinhos
6. **Decision Tree**: Árvore de decisão simples
7. **Naive Bayes**: Classificador Gaussiano
8. **Logistic Regression**: Regressão logística multiclasse

### 3.2 Técnicas Aplicadas

- **Normalização**: StandardScaler (média=0, desvio=1)
- **Validação Cruzada**: 5-fold cross-validation
- **Estratificação**: Mantida na divisão treino/teste

---

## 4. Resultados

### 4.1 Comparação de Modelos

| Modelo               | Acurácia   | Precisão   | Recall     | F1-Score   | CV Mean | CV Std |
|----------------------|------------|------------|------------|------------|---------|--------|
| **Random Forest**    | **94.58%** | **94.61%** | **94.58%** | **94.59%** | 94.35%  | 0.25%  |
| Gradient Boosting    | 94.09%     | 94.13%     | 94.09%     | 94.09%     | 93.85%  | 0.33%  |
| Decision Tree        | 91.43%     | 91.45%     | 91.43%     | 91.44%     | 90.63%  | 0.96%  |
| SVM (Linear)         | 91.39%     | 91.60%     | 91.39%     | 91.41%     | 90.45%  | 0.71%  |
| Logistic Regression  | 91.20%     | 91.31%     | 91.20%     | 91.21%     | 90.49%  | 0.69%  |
| SVM (RBF)            | 90.67%     | 90.78%     | 90.67%     | 90.67%     | 89.59%  | 0.37%  |
| K-Nearest Neighbors  | 89.16%     | 89.25%     | 89.16%     | 89.19%     | 88.18%  | 0.46%  |
| Naive Bayes          | 81.64%     | 84.39%     | 81.64%     | 79.43%     | 81.10%  | 0.57%  |

### 4.2 Melhor Modelo: Random Forest

**Métricas Gerais:**
- Acurácia: 94.58%
- F1-Score médio: 94.59%
- Validação cruzada: 94.35% (±0.25%)

**Desempenho por Classe:**

| Classe              | Precision | Recall | F1-Score | Suporte |
|---------------------|-----------|--------|----------|---------|
| Cimento Pavimentado | 87%       | 88%    | 88%      | 649     |
| Rua/Asfalto         | 100%      | 100%   | 100%     | 1.739   |
| Terra Batida        | 88%       | 88%    | 88%      | 656     |

**Média Ponderada:** 95% em todas as métricas

### 4.3 Análise da Matriz de Confusão

A matriz de confusão do Random Forest mostra:
- **Rua/Asfalto**: Perfeitamente classificada (100%)
- **Cimento Pavimentado**: Alta taxa de acerto (87-88%)
- **Terra Batida**: Alta taxa de acerto (88%)

As confusões ocasionais ocorrem entre Cimento Pavimentado e Terra Batida, o que é esperado devido às características similares de irregularidade dessas superfícies.

### 4.4 Curvas ROC

As curvas ROC-AUC demonstram excelente capacidade de discriminação para todas as classes, com AUC próximo a 1.0, especialmente para a classe Rua/Asfalto.

---

## 5. Discussão

### 5.1 Pontos Fortes

1. **Alta Acurácia**: 94.58% é um resultado excelente para classificação de 3 classes
2. **Robustez**: Baixo desvio padrão na validação cruzada indica estabilidade
3. **Generalização**: Boa performance em múltiplos algoritmos sugere features discriminativas
4. **Praticidade**: Usa apenas sensores de smartphone, facilitando implementação

### 5.2 Desafios Identificados

1. **Desbalanceamento**: Rua/Asfalto tem ~2.5x mais amostras que as outras classes
2. **Confusão entre Classes**: Cimento e Terra Batida têm características semelhantes
3. **Dependência do Contexto**: Velocidade e estilo de pilotagem podem afetar os dados

### 5.3 Limitações

- Dados coletados por um único dispositivo
- Condições ambientais não controladas
- Um único ciclista e bicicleta
- Não considerou fatores como velocidade ou condições climáticas

---

## 6. Conclusões

### 6.1 Principais Conclusões

1. **Viabilidade Técnica Confirmada**: É possível classificar tipos de vias com alta precisão usando apenas dados de acelerômetro de smartphones

2. **Random Forest como Melhor Modelo**: Superou outros algoritmos em todas as métricas, com 94.58% de acurácia

3. **Features Eficazes**: A combinação de features estatísticas e no domínio da frequência mostrou-se altamente discriminativa

4. **Aplicabilidade Prática**: O sistema pode ser implementado em aplicativos móveis para ciclistas e navegação

### 6.2 Contribuições

- Implementação completa de pipeline de ML para classificação de vias
- Extração abrangente de 62 features relevantes
- Comparação sistemática de 8 algoritmos diferentes
- Código bem documentado e reutilizável

### 6.3 Trabalhos Futuros

1. **Expansão do Dataset**: Coletar dados de múltiplos dispositivos e ciclistas
2. **Novas Features**: Incluir dados de GPS, velocidade e condições meteorológicas
3. **Deep Learning**: Testar redes neurais convolucionais (CNN) e recorrentes (LSTM)
4. **Aplicação em Tempo Real**: Desenvolver app mobile para classificação em tempo real
5. **Outras Modalidades**: Adaptar para outros veículos (carros, motos)
6. **Detecção de Anomalias**: Identificar buracos e irregularidades específicas

---

## 7. Referências

### Bibliotecas e Frameworks Utilizados

- **pandas**: Manipulação de dados tabulares
- **numpy**: Computação científica e álgebra linear
- **scipy**: Processamento de sinais e estatística
- **scikit-learn**: Algoritmos de machine learning
- **matplotlib/seaborn**: Visualização de dados

### Técnicas Aplicadas

- Janelas deslizantes (Sliding Windows)
- Transformada Rápida de Fourier (FFT)
- Densidade Espectral de Potência (PSD)
- Validação Cruzada Estratificada
- Normalização Z-score

---

## 8. Apêndices

### 8.1 Estrutura do Código

```
classificacao_vias.py
├── DataProcessor (Classe)
│   ├── load_data()
│   ├── extract_features()
│   ├── create_sliding_windows()
│   └── organize_data()
│
└── ModelTrainer (Classe)
    ├── prepare_data()
    ├── initialize_models()
    ├── train_and_evaluate()
    ├── generate_report()
    └── plot_results()
```

### 8.2 Arquivos Gerados

1. `dados_organizados.csv` - Dataset processado (10.144 × 63)
2. `comparacao_modelos.csv` - Métricas de todos os modelos
3. `comparacao_modelos.png` - Gráficos comparativos
4. `matriz_confusao.png` - Matriz de confusão do melhor modelo
5. `curvas_roc.png` - Curvas ROC multiclasse

### 8.3 Requisitos do Sistema

```
Python >= 3.8
pandas >= 1.5.0
numpy >= 1.23.0
matplotlib >= 3.6.0
seaborn >= 0.12.0
scipy >= 1.9.0
scikit-learn >= 1.2.0
```

---

## Observações Finais

Este trabalho demonstra a viabilidade e eficácia de sistemas de classificação de vias baseados em sensores de smartphones. Os resultados obtidos são promissores e abrem caminho para aplicações práticas em navegação, monitoramento urbano e análise de infraestrutura.

A abordagem metodológica rigorosa, incluindo pré-processamento adequado, extração criteriosa de features e comparação sistemática de modelos, resultou em um sistema robusto e de alta performance.

---

**Data de Conclusão**: Novembro de 2025  
**Nível**: Mestrado  
**Área**: Aprendizado de Máquina e Processamento de Sinais
