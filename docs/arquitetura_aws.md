# Arquitetura AWS — AgroOrbit AI

## Visão Geral

A arquitetura proposta para o AgroOrbit AI foi projetada para escalar em produção utilizando serviços gerenciados da AWS. Por se tratar de uma POC acadêmica, a arquitetura é documentada e simulada, não implantada em produção.

---

## Fluxo da Arquitetura

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

## Componentes

### ESP32 / Sensores Simulados
Dispositivos IoT instalados nos talhões da fazenda. Coletam temperatura, umidade do ar, umidade do solo, luminosidade, velocidade do vento, chuva, pH do solo e índice de vegetação. Na POC, esses dados são simulados pelo script `gerar_dados_agricolas.py`.

### API Gateway
Recebe as leituras dos sensores via requisições HTTP POST. Roteia as requisições para o AWS Lambda para processamento.

### AWS Lambda
Função serverless que processa os dados recebidos, aciona o modelo de Machine Learning, gera a classificação de risco e dispara alertas automáticos quando necessário.

### DynamoDB / RDS
Banco de dados para persistência do histórico de leituras e previsões. DynamoDB para dados não-relacionais de alta velocidade; RDS para consultas estruturadas.

### Amazon S3
Armazena imagens das lavouras para análise por visão computacional, modelos treinados serializados e arquivos CSV de resultado.

### Modelo de Machine Learning
RandomForestClassifier treinado com dados históricos. Classifica o risco agrícola em saudavel, atencao ou critico com base nas variáveis ambientais e de solo.

### Dashboard
Interface Streamlit acessível pelo navegador. Exibe métricas, gráficos, alertas e resultado da análise visual em tempo real.

### Alerta Automático
Quando o Lambda identifica risco crítico, dispara uma notificação automática via Amazon SNS para o gestor agrícola.

---

## Justificativa

Esta arquitetura é documentada como POC acadêmica. Em um ambiente de produção real, todos os componentes seriam provisionados na AWS, garantindo escalabilidade, disponibilidade e segurança dos dados agrícolas.
