# Guia Rápido de Uso

## 🚀 Início Rápido

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

Ou:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

### 2. Executar o Pipeline Completo

```bash
python classificacao_vias.py
```

**Tempo estimado**: 2-3 minutos

**Arquivos gerados**:
- `dados_organizados.csv` - Dataset processado
- `comparacao_modelos.csv` - Métricas dos modelos
- `comparacao_modelos.png` - Gráficos comparativos
- `matriz_confusao.png` - Matriz de confusão
- `curvas_roc.png` - Curvas ROC

### 3. Análise Exploratória (Opcional)

```bash
python analise_exploratoria.py
```

**Tempo estimado**: 1-2 minutos

**Arquivos gerados**:
- `analise_series_temporais.png`
- `analise_distribuicoes.png`
- `analise_estatisticas.png`
- `analise_correlacoes.png`
- `analise_espectral.png`
- `estatisticas_descritivas.csv`

### 4. Notebook Interativo (Opcional)

```bash
jupyter notebook analise_interativa.ipynb
```

---

## 📊 Resultados Esperados

### Melhor Modelo: Random Forest
- **Acurácia**: ~94.6%
- **F1-Score**: ~94.6%
- **Tempo de treinamento**: < 30 segundos

### Performance por Classe:
- **Rua/Asfalto**: 100% de acurácia
- **Cimento Pavimentado**: ~87% de acurácia
- **Terra Batida**: ~88% de acurácia

---

## 🔧 Personalização

### Alterar Tamanho da Janela

No arquivo `classificacao_vias.py`, linha ~468:

```python
processor = DataProcessor(window_size=100, overlap=50)
```

**Valores recomendados**:
- `window_size`: 50-200 amostras
- `overlap`: 25-75% do window_size

### Alterar Proporção Treino/Teste

Na linha ~478:

```python
X_train, X_test, y_train, y_test = trainer.prepare_data(organized_data, test_size=0.3)
```

**Valores comuns**:
- `test_size=0.2` → 80% treino, 20% teste
- `test_size=0.3` → 70% treino, 30% teste (padrão)
- `test_size=0.4` → 60% treino, 40% teste

### Adicionar Novos Modelos

No método `initialize_models()` da classe `ModelTrainer`:

```python
self.models['Seu Modelo'] = SeuClassificador(
    parametros=valores
)
```

---

## 📁 Estrutura de Arquivos

```
Trabalho 2/
│
├── 📊 Dados Brutos
│   ├── rua_asfalto.csv
│   ├── cimento_utinga.csv
│   └── terra_batida.csv
│
├── 🐍 Scripts Python
│   ├── classificacao_vias.py        (Principal - Execute este!)
│   ├── analise_exploratoria.py      (Opcional)
│   └── analise_interativa.ipynb     (Notebook)
│
├── 📖 Documentação
│   ├── README.md                     (Documentação completa)
│   ├── RELATORIO_TRABALHO.md         (Relatório técnico)
│   ├── GUIA_RAPIDO.md               (Este arquivo)
│   └── requirements.txt              (Dependências)
│
└── 📈 Resultados (gerados após execução)
    ├── dados_organizados.csv
    ├── comparacao_modelos.csv
    ├── comparacao_modelos.png
    ├── matriz_confusao.png
    ├── curvas_roc.png
    ├── analise_*.png (se executar análise exploratória)
    └── estatisticas_descritivas.csv
```

---

## ❓ Resolução de Problemas

### Erro: "ModuleNotFoundError"

**Solução**: Instale as dependências
```bash
pip install -r requirements.txt
```

### Erro: "FileNotFoundError"

**Solução**: Verifique se os arquivos CSV estão no diretório correto
```bash
ls *.csv
```

Devem aparecer:
- `rua_asfalto.csv`
- `cimento_utinga.csv`
- `terra_batida.csv`

### Erro: Falta de memória

**Solução 1**: Reduza o window_size
```python
processor = DataProcessor(window_size=50, overlap=25)
```

**Solução 2**: Use menos modelos (comente alguns no método `initialize_models()`)

### Warnings do matplotlib

**Solução**: São apenas avisos, não afetam os resultados. Para suprimir:
```python
import warnings
warnings.filterwarnings('ignore')
```

---

## 💡 Dicas

### 1. Primeiro Uso
- Execute primeiro `classificacao_vias.py`
- Depois explore com `analise_exploratoria.py`
- Use o notebook para experimentação

### 2. Análise dos Resultados
- Verifique o arquivo `comparacao_modelos.csv` para métricas numéricas
- Abra os arquivos PNG para visualizações
- Consulte `RELATORIO_TRABALHO.md` para interpretação detalhada

### 3. Experimentação
- Use o notebook `analise_interativa.ipynb` para testar ideias
- Modifique parâmetros no script principal
- Salve versões diferentes para comparação

---

## 📞 Ajuda Adicional

### Documentação Detalhada
Consulte `README.md` para documentação completa

### Relatório Técnico
Veja `RELATORIO_TRABALHO.md` para análise aprofundada

### Código Fonte
Todos os scripts estão bem comentados - leia os comentários no código!

---

## ⏱️ Checklist de Execução

- [ ] Instalei as dependências (`pip install -r requirements.txt`)
- [ ] Verifiquei que os 3 arquivos CSV estão presentes
- [ ] Executei `python classificacao_vias.py`
- [ ] Verifiquei os arquivos gerados
- [ ] (Opcional) Executei `python analise_exploratoria.py`
- [ ] (Opcional) Abri o notebook Jupyter
- [ ] Li o relatório em `RELATORIO_TRABALHO.md`

---

## 🎯 Próximos Passos

Após executar o pipeline básico:

1. **Analise os Resultados**
   - Abra as imagens PNG geradas
   - Leia o relatório de classificação no terminal
   - Compare os modelos em `comparacao_modelos.csv`

2. **Experimente Modificações**
   - Altere o tamanho da janela
   - Teste diferentes proporções treino/teste
   - Adicione novos modelos

3. **Aprofunde a Análise**
   - Use o notebook interativo
   - Visualize a importância das features
   - Analise casos de erro

4. **Documente Seus Achados**
   - Anote os resultados das suas modificações
   - Compare com os resultados baseline
   - Tire conclusões sobre o que funciona melhor
