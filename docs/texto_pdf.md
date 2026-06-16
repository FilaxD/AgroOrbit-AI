# AgroOrbit AI
## Assistente Inteligente para Previsão de Estresse Agrícola com Dados Espaciais

**Nome completo:** Guilherme Filartiga
**RM:**  Rm568034
**Curso:** Inteligência Artificial — FIAP
**Entrega:** SUB Global Solution 2026.1

---

## 1. Introdução

A exploração espacial deixou de ser exclusivamente científica e passou a representar uma das maiores oportunidades tecnológicas da atualidade. Satélites de observação terrestre monitoram o clima, a vegetação, o uso do solo e eventos climáticos extremos em tempo real, gerando grandes volumes de dados que são utilizados por governos, empresas e centros de pesquisa ao redor do mundo.

No setor agrícola, o sensoriamento remoto via satélite viabilizou o desenvolvimento de índices como o NDVI (Índice de Vegetação por Diferença Normalizada), capaz de indicar a saúde da vegetação de uma lavoura sem que nenhum técnico precise ir ao campo. Esse tipo de dado, combinado com leituras de sensores em solo, abre caminho para soluções inteligentes de monitoramento agrícola que antes eram inacessíveis para a maior parte dos produtores rurais.

O AgroOrbit AI surge nesse contexto como uma prova de conceito que une dados espaciais simulados, sensores IoT, Machine Learning e visão computacional para prever o risco de estresse agrícola em lavouras, respondendo à pergunta central da SUB Global Solution 2026.1: como a Inteligência Artificial e as tecnologias digitais podem transformar a nova economia espacial e gerar impacto positivo na Terra?

---

## 2. Problema

Pequenos e médios produtores rurais muitas vezes não têm acesso a ferramentas inteligentes para monitorar a saúde das lavouras em tempo real. As principais dificuldades são:

- Falta de integração entre dados climáticos, de solo e de vegetação
- Tomada de decisão tardia sobre irrigação, adubação e manejo
- Ausência de alertas automáticos para situações críticas
- Custo elevado de tecnologias de monitoramento profissional

A falta de análise integrada pode resultar em perdas de produtividade, desperdício de recursos hídricos e atraso na identificação de áreas com risco de seca ou estresse hídrico.

---

## 3. Solução Proposta

O AgroOrbit AI é uma POC que transforma dados ambientais e visuais em informação acionável para o produtor ou gestor agrícola.

A solução classifica cada talhão da fazenda em uma das três categorias:
- **saudavel:** condições dentro do esperado
- **atencao:** risco moderado, monitoramento recomendado
- **critico:** ação imediata recomendada

O sistema integra:
- Sensores simulados (ESP32) coletando temperatura, umidade, chuva, pH, vento, luminosidade e índice de vegetação inspirado em NDVI
- Machine Learning com RandomForestClassifier para classificação de risco
- Visão computacional com OpenCV para análise visual de imagens de lavoura
- Dashboard interativo com Streamlit e Plotly
- Alertas automáticos
- Arquitetura AWS documentada

---

## 4. Arquitetura da Solução

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

**ESP32/Sensores:** coletam leituras em campo e enviam via Wi-Fi.
**API Gateway:** recebe os dados e roteia para processamento.
**AWS Lambda:** processa, classifica e gera alertas.
**DynamoDB/S3:** armazena histórico e modelos.
**Dashboard:** visualização em tempo real para o gestor.

---

## 5. Desenvolvimento

### 5.1 Geração de Dados Simulados

O script `gerar_dados_agricolas.py` gera 500 registros simulando leituras de sensores entre 01/06/2026 e 10/06/2026 para cinco talhões: Norte, Sul, Leste, Oeste e Central.

O risco é calculado por sistema de pontuação com indicadores críticos (2 pontos cada) e de atenção (1 ponto cada). Pontuação ≥ 8 = crítico; ≥ 4 = atenção; < 4 = saudável.

### 5.2 Machine Learning

O script `modelo_agricola.py` treina um RandomForestClassifier com 100 estimadores usando divisão 80/20 treino/teste. As features utilizadas são temperatura, umidade do ar, umidade do solo, luminosidade, velocidade do vento, chuva, pH do solo e índice de vegetação.

O modelo é avaliado com acurácia, matriz de confusão e classification report, e serializado com Joblib.

### 5.3 Visão Computacional

O script `visao_computacional.py` analisa uma imagem de lavoura usando máscaras de cor em espaço HSV do OpenCV para detectar vegetação saudável (tons verdes), vegetação seca (tons amarelos/laranjas) e solo exposto. Gera imagem marcada e CSV com resultado.

### 5.4 Dashboard

O `dashboard.py` em Streamlit exibe métricas, filtros, seis gráficos interativos com Plotly, tabela de previsões, alertas automáticos, imagem processada e arquitetura AWS.

### 5.5 Alertas Automáticos

Se `alerta_previsto == acao_recomendada`, o sistema exibe alerta crítico e salva o registro em `data/alertas_agricolas.csv`.

---

## 6. Códigos Principais

### gerar_dados_agricolas.py (trecho principal)

```python
def calcular_risco(temp, umid_ar, umid_solo, chuva, idx_veg, ph, vento):
    pontos = 0
    if temp >= 35:            pontos += 2
    if umid_solo <= 25:       pontos += 2
    if umid_ar <= 30:         pontos += 2
    if chuva <= 2:            pontos += 2
    if idx_veg <= 0.35:       pontos += 2
    if ph < 5.5 or ph > 7.5: pontos += 2
    if vento >= 25:           pontos += 2
    if 29 <= temp <= 34.99:   pontos += 1
    if 26 <= umid_solo <= 45: pontos += 1
    if pontos >= 8:   return 'critico'
    elif pontos >= 4: return 'atencao'
    else:             return 'saudavel'
```

### modelo_agricola.py (trecho principal)

```python
modelo = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)
print(f"Acuracia: {acuracia:.4f}")
joblib.dump(modelo, 'models/modelo_agricola.pkl')
```

### visao_computacional.py (trecho principal)

```python
hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
mascara_verde = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
mascara_seca  = cv2.inRange(hsv, np.array([15, 40, 40]), np.array([34, 255, 255]))
pct_verde = round(cv2.countNonZero(mascara_verde) / total_pixels * 100, 2)
pct_seca  = round(cv2.countNonZero(mascara_seca)  / total_pixels * 100, 2)
```

### dashboard.py (trecho de alerta)

```python
if (df['alerta_previsto'] == 'acao_recomendada').any():
    st.error("ALERTA: talhao em condicao critica. Acao imediata recomendada.")
elif (df['alerta_previsto'] == 'monitorar').any():
    st.warning("ATENCAO: ha talhoes que precisam de monitoramento preventivo.")
else:
    st.success("Situacao geral controlada: nenhum alerta critico identificado.")
```

### validar_projeto.py (trecho principal)

```python
for arq in ARQUIVOS:
    if os.path.exists(arq):
        ok(arq)
    else:
        erro(f"Arquivo nao encontrado: {arq}")
```

---

## 7. Resultados Esperados

O sistema deve:
- Identificar talhões em risco crítico para ação imediata
- Reduzir perdas por estresse hídrico e nutricional
- Otimizar uso de irrigação com base em dados reais
- Demonstrar o uso de IA e tecnologias espaciais no campo
- Apoiar a tomada de decisão do produtor rural

---

## 8. Conclusão

O AgroOrbit AI demonstra como Inteligência Artificial, visão computacional e dados inspirados em tecnologias espaciais podem gerar impacto positivo na Terra. A POC combina sensores simulados, Machine Learning, análise visual e dashboard interativo para transformar dados ambientais em informação acionável para produtores rurais.

A solução é escalável e pode ser evoluída com dados reais de satélite, integração AWS em produção e modelos YOLO para análise visual avançada de lavouras.

---

## 9. Links

- **Repositório GitHub:** [PREENCHER]
- **Vídeo demonstrativo (YouTube — Não Listado):** [PREENCHER]
