# AgroOrbit AI

**Assistente Inteligente para Previsão de Estresse Agrícola com Dados Espaciais**

SUB Global Solution 2026.1 — FIAP — Inteligência Artificial

---

## Descrição

O AgroOrbit AI é uma prova de conceito (POC) que utiliza Inteligência Artificial, Machine Learning, visão computacional e dados simulados de sensores para prever o risco de estresse agrícola em lavouras.

A solução simula o uso de dados ambientais e agrícolas, como temperatura, umidade do ar, umidade do solo, chuva, luminosidade, vento, pH do solo e índice de vegetação inspirado em satélite/NDVI, e classifica cada talhão como saudavel, atencao ou critico.

---

## Problema

Pequenos e médios produtores rurais muitas vezes não têm acesso a ferramentas inteligentes para monitorar a saúde das lavouras em tempo real. A falta de análise integrada entre clima, solo, vegetação e imagem pode dificultar a identificação rápida de áreas com risco de seca, estresse hídrico, baixa produtividade ou degradação da vegetação.

---

## Solução Proposta

O AgroOrbit AI transforma dados ambientais e visuais em informação acionável, ajudando o produtor ou gestor agrícola a identificar se uma região está saudável, em atenção ou crítica, com geração automática de alertas e dashboard interativo.

---

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn (RandomForestClassifier)
- Joblib
- OpenCV
- Streamlit
- Plotly
- Pillow
- CSV (armazenamento local)
- Arquitetura AWS documentada/simulada

---

## Arquitetura Resumida

```
ESP32 / Sensores Simulados
        ↓
   API Gateway
        ↓
   AWS Lambda
        ↓
DynamoDB / RDS + S3
        ↓
Modelo de Machine Learning
        ↓
     Dashboard
        ↓
  Alerta Automático
```

---

## Estrutura de Pastas

```
AgroOrbit-AI/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── dados_agricolas.csv
│   ├── previsoes_agricolas.csv
│   ├── resultado_visao.csv
│   └── alertas_agricolas.csv
│
├── src/
│   ├── gerar_dados_agricolas.py
│   ├── modelo_agricola.py
│   ├── prever_risco_agricola.py
│   ├── visao_computacional.py
│   ├── dashboard.py
│   └── validar_projeto.py
│
├── images/
│   ├── imagem_lavoura.jpg
│   └── resultado_visao.jpg
│
├── models/
│   └── modelo_agricola.pkl
│
└── docs/
    ├── arquitetura_aws.md
    ├── roteiro_video.md
    └── texto_pdf.md
```

---

## Como Executar

**1. Instalar dependências:**
```
python -m pip install -r requirements.txt
```

**2. Gerar dados simulados:**
```
python src/gerar_dados_agricolas.py
```

**3. Treinar o modelo:**
```
python src/modelo_agricola.py
```

**4. Testar previsão com nova leitura:**
```
python src/prever_risco_agricola.py
```

**5. Analisar imagem com visão computacional:**
```
python src/visao_computacional.py
```

**6. Iniciar dashboard:**
```
streamlit run src/dashboard.py
```

**7. Validar projeto:**
```
python src/validar_projeto.py
```

---

## Explicação dos Principais Arquivos

| Arquivo | Descrição |
|---|---|
| `src/gerar_dados_agricolas.py` | Gera 500 registros simulados de sensores agrícolas |
| `src/modelo_agricola.py` | Treina o RandomForestClassifier e salva o modelo |
| `src/prever_risco_agricola.py` | Carrega o modelo e prevê risco para nova leitura |
| `src/visao_computacional.py` | Analisa imagem de lavoura com OpenCV |
| `src/dashboard.py` | Dashboard interativo com Streamlit e Plotly |
| `src/validar_projeto.py` | Valida todos os arquivos e colunas do projeto |

---

## Resultados Gerados

- `data/dados_agricolas.csv` — 500 leituras simuladas de sensores
- `data/previsoes_agricolas.csv` — previsões do modelo para todo o dataset
- `data/resultado_visao.csv` — resultado da análise visual por OpenCV
- `data/alertas_agricolas.csv` — registros com alertas ativos
- `images/resultado_visao.jpg` — imagem processada com marcações
- `models/modelo_agricola.pkl` — modelo treinado serializado

---

## Observação sobre POC

Este projeto é uma Prova de Conceito acadêmica. A arquitetura AWS é documentada/simulada e não foi implantada em produção. A etapa de visão computacional usa OpenCV como POC; em uma versão futura, poderia ser substituída por YOLO treinado com imagens reais de lavouras.

---

## Autor

- **Nome completo:** Guilherme Filartiga
- **RM:** 568034
- **Curso:** Inteligência Artificial — FIAP
- **Entrega:** SUB Global Solution 2026.1
