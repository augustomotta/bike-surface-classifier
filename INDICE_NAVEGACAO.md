# 🗂️ ÍNDICE DE NAVEGAÇÃO RÁPIDA

## 📍 Acesso Rápido aos Arquivos Principais

---

## 🎯 Para Começar

### ▶️ Executar o Projeto
```bash
# Script principal (gera modelos e visualizações)
python classificacao_vias.py

# Análise exploratória (opcional)
python analise_exploratoria.py
```

### 📖 Ler Documentação
1. **Início Rápido**: `GUIA_RAPIDO.md` ← Comece aqui!
2. **Documentação Completa**: `README.md`
3. **Relatório Técnico**: `RELATORIO_TRABALHO.md`
4. **Organização**: `ORGANIZACAO_FINAL.md`

---

## 📊 Visualizar Resultados

### 🏆 Resultados Principais (Melhor Performance)

#### Ver Comparação de Modelos
📁 `resultados/visualizacoes/comparacao_modelos.png`
- 4 gráficos de barras
- Compara 8 modelos
- Métricas: Acurácia, Precisão, Recall, F1-Score

#### Ver Matriz de Confusão
📁 `resultados/visualizacoes/matriz_confusao.png`
- Random Forest (94.58%)
- Mostra acertos e erros por classe
- Formato: Heatmap

#### Ver Curvas ROC
📁 `resultados/visualizacoes/curvas_roc.png`
- 8 modelos × 3 classes = 24 curvas
- Inclui valores de AUC
- Análise multiclasse

---

### 📈 Análise Exploratória

#### Ver Séries Temporais
📁 `resultados/analise_exploratoria/analise_series_temporais.png`
- Sinais dos 3 sensores
- 3 tipos de vias
- Primeiras 1000 amostras

#### Ver Distribuições
📁 `resultados/analise_exploratoria/analise_distribuicoes.png`
- Histogramas
- Boxplots
- Violin plots

#### Ver Estatísticas
📁 `resultados/analise_exploratoria/analise_estatisticas.png`
- Comparação entre vias
- 6 métricas estatísticas
- Gráficos de barras

#### Ver Correlações
📁 `resultados/analise_exploratoria/analise_correlacoes.png`
- 3 matrizes (uma por via)
- Correlação entre sensores
- Formato: Heatmap

#### Ver Análise Espectral
📁 `resultados/analise_exploratoria/analise_espectral.png`
- Transformada de Fourier (FFT)
- Domínio da frequência
- 3 sensores × 3 vias

---

## 📋 Acessar Dados e Tabelas

### 📊 Dados Processados
📁 `resultados/dados_processados/dados_organizados.csv`
- 10.144 linhas (janelas)
- 63 colunas (62 features + classe)
- Pronto para machine learning

### 🤖 Métricas dos Modelos
📁 `resultados/modelos/comparacao_modelos.csv`
- 8 linhas (modelos)
- 7 colunas (métricas)
- Formato: CSV (abrir no Excel/LibreOffice)

### 📈 Estatísticas Descritivas
📁 `resultados/analise_exploratoria/estatisticas_descritivas.csv`
- Estatísticas por via e sensor
- Média, desvio, variância, etc.
- Formato: CSV

---

## 🔍 Busca Rápida

### Por Tipo de Arquivo

#### 🖼️ Todas as Imagens PNG
```
resultados/visualizacoes/
├── comparacao_modelos.png
├── matriz_confusao.png
└── curvas_roc.png

resultados/analise_exploratoria/
├── analise_series_temporais.png
├── analise_distribuicoes.png
├── analise_estatisticas.png
├── analise_correlacoes.png
└── analise_espectral.png
```

#### 📄 Todos os CSV
```
dados/
├── rua_asfalto.csv
├── cimento_utinga.csv
└── terra_batida.csv

resultados/dados_processados/
└── dados_organizados.csv

resultados/modelos/
└── comparacao_modelos.csv

resultados/analise_exploratoria/
└── estatisticas_descritivas.csv
```

#### 🐍 Scripts Python
```
./
├── classificacao_vias.py       (PRINCIPAL)
├── analise_exploratoria.py
└── analise_interativa.ipynb
```

#### 📚 Documentação
```
./
├── README.md
├── RELATORIO_TRABALHO.md
├── GUIA_RAPIDO.md
├── SUMARIO_PROJETO.md
├── FLUXO_PROJETO.txt
├── ORGANIZACAO_FINAL.md
├── INDICE_NAVEGACAO.md         (Este arquivo)
└── requirements.txt
```

---

## 🎓 Para Apresentação

### Slides Recomendados

#### Slide 1: Introdução
- **Documento**: `RELATORIO_TRABALHO.md` (seção 1)
- **Imagem**: -

#### Slide 2: Metodologia
- **Documento**: `RELATORIO_TRABALHO.md` (seção 2)
- **Imagem**: `FLUXO_PROJETO.txt` (screenshot)

#### Slide 3: Dados Coletados
- **Documento**: `RELATORIO_TRABALHO.md` (seção 2.1)
- **Imagem**: `analise_series_temporais.png`

#### Slide 4: Análise dos Dados
- **Documento**: -
- **Imagem**: `analise_distribuicoes.png`

#### Slide 5: Extração de Features
- **Documento**: `RELATORIO_TRABALHO.md` (seção 2.3)
- **Imagem**: `analise_espectral.png`

#### Slide 6: Modelos Testados
- **Documento**: `RELATORIO_TRABALHO.md` (seção 3)
- **Imagem**: `comparacao_modelos.png`

#### Slide 7: Resultados
- **Documento**: `RELATORIO_TRABALHO.md` (seção 4)
- **Imagem**: `matriz_confusao.png`

#### Slide 8: Avaliação Detalhada
- **Documento**: Tabela em `comparacao_modelos.csv`
- **Imagem**: `curvas_roc.png`

#### Slide 9: Conclusões
- **Documento**: `RELATORIO_TRABALHO.md` (seção 6)
- **Imagem**: -

---

## 📱 Atalhos de Terminal

### Abrir Pasta de Visualizações
```bash
cd resultados/visualizacoes/
xdg-open .  # Linux
```

### Abrir Pasta de Análise
```bash
cd resultados/analise_exploratoria/
xdg-open .  # Linux
```

### Ver Todos os Resultados
```bash
cd resultados/
find . -name "*.png" -o -name "*.csv"
```

### Estatísticas do Projeto
```bash
# Contar linhas de código
wc -l *.py

# Contar arquivos gerados
find resultados/ -type f | wc -l

# Ver tamanho dos arquivos
du -sh resultados/*/
```

---

## 🔗 Links Internos

### Documentos Relacionados

- **Visão Geral**: [`SUMARIO_PROJETO.md`](SUMARIO_PROJETO.md)
- **Organização**: [`ORGANIZACAO_FINAL.md`](ORGANIZACAO_FINAL.md)
- **Fluxo**: [`FLUXO_PROJETO.txt`](FLUXO_PROJETO.txt)
- **Guia Rápido**: [`GUIA_RAPIDO.md`](GUIA_RAPIDO.md)
- **README**: [`README.md`](README.md)
- **Relatório**: [`RELATORIO_TRABALHO.md`](RELATORIO_TRABALHO.md)

### Scripts

- **Principal**: [`classificacao_vias.py`](classificacao_vias.py)
- **Análise**: [`analise_exploratoria.py`](analise_exploratoria.py)
- **Notebook**: [`analise_interativa.ipynb`](analise_interativa.ipynb)

---

## 📞 FAQ - Onde Encontro...?

### "Onde está o melhor resultado?"
📁 `resultados/visualizacoes/matriz_confusao.png`
📄 `resultados/modelos/comparacao_modelos.csv` (primeira linha)

### "Onde estão os dados originais?"
📁 `dados/` (3 arquivos CSV)

### "Onde estão as imagens para slides?"
📁 `resultados/visualizacoes/` (modelos)
📁 `resultados/analise_exploratoria/` (análises)

### "Onde está a tabela de resultados?"
📁 `resultados/modelos/comparacao_modelos.csv`

### "Onde estão os dados processados?"
📁 `resultados/dados_processados/dados_organizados.csv`

### "Como executar o projeto?"
📄 `GUIA_RAPIDO.md` ← Instruções completas

### "Como entender os resultados?"
📄 `RELATORIO_TRABALHO.md` (seções 4 e 5)

### "Qual a estrutura do projeto?"
📄 `ORGANIZACAO_FINAL.md` ← Estrutura completa

---

## ✅ Checklist de Navegação

Use este checklist para verificar se encontrou tudo:

- [ ] Li o guia rápido (`GUIA_RAPIDO.md`)
- [ ] Vi a matriz de confusão
- [ ] Vi a comparação de modelos
- [ ] Explorei as análises visuais
- [ ] Abri a tabela de resultados
- [ ] Entendi a estrutura de pastas
- [ ] Sei onde estão os dados originais
- [ ] Sei onde estão os resultados
- [ ] Li o relatório técnico
- [ ] Estou pronto para apresentar

---

## 🎯 Navegação por Objetivo

### Quero entender o projeto
1. Ler `README.md`
2. Ler `SUMARIO_PROJETO.md`
3. Ver `FLUXO_PROJETO.txt`

### Quero executar o projeto
1. Ler `GUIA_RAPIDO.md`
2. Executar `python classificacao_vias.py`
3. Ver resultados em `resultados/`

### Quero ver os resultados
1. Abrir `resultados/visualizacoes/`
2. Ver todas as imagens PNG
3. Ler `resultados/modelos/comparacao_modelos.csv`

### Quero analisar os dados
1. Abrir `resultados/analise_exploratoria/`
2. Ver todas as análises visuais
3. Ler `estatisticas_descritivas.csv`

### Quero preparar apresentação
1. Ler `RELATORIO_TRABALHO.md` (estrutura)
2. Usar imagens de `resultados/visualizacoes/`
3. Usar tabela de `resultados/modelos/`
4. Adicionar análises de `analise_exploratoria/`

### Quero modificar o código
1. Abrir `classificacao_vias.py`
2. Ler comentários no código
3. Consultar `README.md` para detalhes

---

## 🌟 Principais Arquivos

### 🥇 Top 5 para Apresentação
1. `resultados/visualizacoes/comparacao_modelos.png`
2. `resultados/visualizacoes/matriz_confusao.png`
3. `resultados/modelos/comparacao_modelos.csv`
4. `resultados/analise_exploratoria/analise_series_temporais.png`
5. `RELATORIO_TRABALHO.md`

### 🥈 Top 5 para Análise
1. `resultados/dados_processados/dados_organizados.csv`
2. `resultados/analise_exploratoria/estatisticas_descritivas.csv`
3. `resultados/analise_exploratoria/analise_distribuicoes.png`
4. `resultados/analise_exploratoria/analise_correlacoes.png`
5. `analise_interativa.ipynb`

### 🥉 Top 5 para Documentação
1. `README.md`
2. `RELATORIO_TRABALHO.md`
3. `GUIA_RAPIDO.md`
4. `ORGANIZACAO_FINAL.md`
5. `FLUXO_PROJETO.txt`

---

**Última atualização**: 15 de novembro de 2025  
**Versão**: 1.0 - Projeto Completo  
**Status**: ✅ Todos os arquivos gerados e organizados
