# Implementação da Árvore de Decisão - Classificação de Vias
## Resumo Executivo da Implementação

### 🎯 **Objetivo Alcançado**
Implementação bem-sucedida da **árvore de decisão** no sistema de classificação de tipos de vias, com análise completa e visualizações detalhadas dos resultados.

---

## 📊 **Resultados da Árvore de Decisão**

### 🏆 **Performance Obtida**
- **Acurácia**: 92.08% (3ª posição entre 8 modelos)
- **F1-Score**: 0.9209
- **Validação Cruzada**: 91.63% (±0.32%)
- **Posição no Ranking**: 3º lugar (atrás de Random Forest e Gradient Boosting)

### 🌳 **Características da Árvore**
- **Profundidade máxima**: 10 níveis
- **Total de nós**: 265
- **Folhas (decisões finais)**: 133
- **Features utilizadas**: 45 de 62 disponíveis (72.6%)
- **Parâmetros otimizados**: `max_depth=10`, `min_samples_split=5`, `min_samples_leaf=3`, `class_weight='balanced'`

---

## 🔍 **Análise das Regras de Decisão**

### 🎯 **Regra Principal (Raiz)**
```
SE AccX_mean (S21) ≤ 0.04
    ENTÃO → Rua/Asfalto
    SENÃO → Análise complexa para superfícies irregulares
```

### 💡 **Interpretação da Lógica**
1. **Primeiro teste**: Média da aceleração horizontal (AccX_mean)
2. **Superfícies lisas**: Detectadas rapidamente pela baixa variação
3. **Superfícies irregulares**: Análise multi-sensor com energia, máximos e FFT
4. **Decisão final**: Combinação de características temporais e espectrais

---

## 📈 **Features Mais Importantes**

| Rank | Feature | Importância | Descrição |
|------|---------|-------------|-----------|
| 1 | S21 | 57.90% | AccX_mean - Média da Aceleração X |
| 2 | S33 | 13.63% | AccX_energy - Energia da Aceleração X |
| 3 | S45 | 4.70% | AccY_max - Máximo da Aceleração Y |
| 4 | S10 | 3.81% | LinearAccel_kurtosis - Curtose do Acelerômetro |
| 5 | S2 | 2.81% | LinearAccel_std - Desvio Padrão do Acelerômetro |

**Insight Principal**: A aceleração horizontal (AccX) é **decisiva** para classificação, representando quase 60% da importância total.

---

## 🎨 **Visualizações Geradas**

### 📁 **Arquivos Criados**
```
📉 Gráficos da Árvore de Decisão:
├── arvore_decisao_completa.png        # Estrutura completa da árvore
├── arvore_decisao_simplificada.png    # Primeiros 4 níveis (visualização clara)
├── importancia_features_arvore.png    # Top 20 features mais importantes
├── estatisticas_arvore.csv           # Métricas da árvore
└── importancia_features.csv          # Ranking completo de features

📊 Gráficos Gerais:
├── comparacao_modelos.png            # Performance de todos os modelos
├── matriz_confusao.png               # Matriz de confusão do melhor modelo
└── curvas_roc.png                    # Curvas ROC de todos os modelos
```

---

## 🛠️ **Implementação Técnica**

### 🔧 **Melhorias Implementadas**
1. **Importações adicionadas**:
   ```python
   from sklearn.tree import plot_tree, export_text
   ```

2. **Otimização dos parâmetros**:
   ```python
   DecisionTreeClassifier(
       max_depth=10,
       min_samples_split=5,
       min_samples_leaf=3,
       class_weight='balanced'
   )
   ```

3. **Novo método de análise**:
   ```python
   def analyze_decision_tree(self, X_train, feature_mapping, save_path):
       # Visualização da estrutura completa
       # Visualização simplificada (4 níveis)
       # Análise de importância das features
       # Estatísticas da árvore
       # Exportação de regras textuais
   ```

### 📋 **Scripts Auxiliares Criados**
1. **`visualizar_arvore_decisao.py`**: Visualização interativa e análise numérica
2. **`analisar_regras_arvore.py`**: Extração e interpretação das regras de decisão

---

## 🔬 **Insights e Descobertas**

### 🌟 **Principais Achados**
1. **Aceleração horizontal é crucial**: A média da AccX determina 58% das decisões
2. **Superfícies lisas são fáceis de detectar**: Rua/asfalto identificada rapidamente
3. **Superfícies irregulares são complexas**: Requerem análise de múltiplos sensores
4. **Modelo interpretável**: Regras claras e compreensíveis para implementação

### 💼 **Aplicações Práticas**
- **Sistemas embarcados**: Modelo leve e interpretável
- **Detecção em tempo real**: Regras simples para implementação rápida
- **Manutenção de vias**: Identificação automática de superfícies problemáticas
- **Ciclismo inteligente**: Sistema de alerta para mudanças de superfície

---

## 🎯 **Conclusão**

A **árvore de decisão foi implementada com sucesso** no sistema de classificação, oferecendo:

✅ **Alta precisão** (92.08% de acurácia)  
✅ **Interpretabilidade total** (regras claras)  
✅ **Performance estável** (baixa variação no CV)  
✅ **Visualizações completas** (estrutura, importância, regras)  
✅ **Documentação detalhada** (análise e scripts)  

**Resultado**: Um modelo robusto, interpretável e bem documentado para classificação automática de tipos de vias através de dados de acelerômetro, ideal para aplicações práticas em sistemas embarcados e análise urbana.

---

## 🚀 **Como Executar**

```bash
# 1. Execução completa do pipeline
python classificacao_vias.py

# 2. Visualização interativa
python visualizar_arvore_decisao.py

# 3. Análise das regras
python analisar_regras_arvore.py
```

**Data**: 28 de novembro de 2025  
**Status**: ✅ Implementação Concluída com Sucesso