# Roteiro do Vídeo — AgroOrbit AI

**Duração máxima:** 5 minutos

---

## 0:00 a 0:20 — Apresentação

"Olá, meu nome é [SEU NOME], RM [SEU RM], e este é o AgroOrbit AI, meu projeto para a SUB Global Solution 2026.1 da FIAP."

---

## 0:20 a 1:00 — Problema e conexão com economia espacial

"Satélites monitoram o clima, a vegetação e o solo em tempo real ao redor do planeta. Esses dados são usados por governos e empresas para tomar decisões agrícolas mais inteligentes.

O problema que o AgroOrbit AI resolve é que pequenos e médios produtores rurais não têm acesso a ferramentas inteligentes para monitorar a saúde das lavouras. A falta de análise integrada pode atrasar a identificação de áreas com risco de seca, estresse hídrico ou baixa produtividade."

---

## 1:00 a 1:50 — Solução e arquitetura

"O AgroOrbit AI é uma POC que combina dados simulados de sensores ESP32, índice de vegetação inspirado em NDVI de satélite, Machine Learning e visão computacional para classificar talhões agrícolas como saudável, atenção ou crítico.

A arquitetura proposta conecta sensores via API Gateway, processa os dados com AWS Lambda, armazena no DynamoDB e S3, e entrega os resultados em um dashboard Streamlit com alertas automáticos."

---

## 1:50 a 3:20 — Demonstração prática

Mostrar na tela:

1. Abrir o terminal e mostrar o resultado de `python src/gerar_dados_agricolas.py`
2. Mostrar o arquivo `data/dados_agricolas.csv` aberto
3. Rodar `python src/modelo_agricola.py` e mostrar as métricas no terminal
4. Rodar `python src/prever_risco_agricola.py` e mostrar a previsão crítica
5. Rodar `python src/visao_computacional.py` e mostrar a imagem processada
6. Abrir o dashboard com `streamlit run src/dashboard.py` e navegar pelas seções:
   - métricas
   - alertas
   - gráficos
   - imagem processada
   - arquitetura AWS

---

## 3:20 a 4:20 — Tecnologias utilizadas

"O projeto usa Python com Pandas e NumPy para manipulação de dados, Scikit-learn com RandomForest para Machine Learning, OpenCV para análise visual da lavoura, Streamlit e Plotly para o dashboard interativo, sensores simulados representando ESP32 e a arquitetura AWS documentada como POC."

---

## 4:20 a 5:00 — Conclusão e impacto

"O AgroOrbit AI demonstra como Inteligência Artificial, visão computacional e dados inspirados em tecnologias espaciais podem gerar impacto positivo na Terra, ajudando produtores rurais a tomar decisões mais rápidas e inteligentes para proteger suas lavouras e otimizar recursos."
