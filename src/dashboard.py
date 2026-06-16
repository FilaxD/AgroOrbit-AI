"""
dashboard.py
Dashboard interativo do AgroOrbit AI desenvolvido com Streamlit.
Visualiza previsoes de risco agricola, alertas e resultado da visao computacional.
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuracao da pagina
st.set_page_config(
    page_title="AgroOrbit AI",
    page_icon="🌱",
    layout="wide"
)

# Titulo e descricao
st.title("AgroOrbit AI — Previsao Inteligente de Estresse Agricola")
st.markdown("""
**POC com Machine Learning, visao computacional, dados simulados de sensores,
indice de vegetacao inspirado em satelite e arquitetura em nuvem.**
""")
st.markdown("---")

# Carregar dados de previsoes
CAMINHO_PREVISOES = 'data/previsoes_agricolas.csv'
CAMINHO_VISAO     = 'data/resultado_visao.csv'
CAMINHO_IMAGEM    = 'images/resultado_visao.jpg'

if not os.path.exists(CAMINHO_PREVISOES):
    st.error("Arquivo de previsoes nao encontrado. Execute primeiro:")
    st.code("python src/modelo_agricola.py")
    st.stop()

df = pd.read_csv(CAMINHO_PREVISOES)

# ============================================================
# METRICAS PRINCIPAIS
# ============================================================
st.subheader("Visao Geral")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.metric("Total de Registros",       len(df))
col2.metric("Talhoes Monitorados",      df['regiao'].nunique())
col3.metric("Casos Criticos",           int((df['risco_previsto'] == 'critico').sum()))
col4.metric("Risco Predominante",       df['risco_previsto'].mode()[0].capitalize())
col5.metric("Temp. Media (°C)",         f"{df['temperatura_c'].mean():.1f}")
col6.metric("Umidade Solo Media (%)",   f"{df['umidade_solo_percentual'].mean():.1f}")
col7.metric("Indice Vegetacao Medio",   f"{df['indice_vegetacao'].mean():.3f}")

st.markdown("---")

# ============================================================
# ALERTAS AUTOMATICOS
# ============================================================
st.subheader("Alertas do Sistema")

tem_critico  = (df['alerta_previsto'] == 'acao_recomendada').any()
tem_atencao  = (df['alerta_previsto'] == 'monitorar').any()

if tem_critico:
    st.error("ALERTA: talhao em condicao critica. Recomenda-se acao imediata de irrigacao, analise do solo ou inspecao da lavoura.")
if tem_atencao:
    st.warning("ATENCAO: ha talhoes que precisam de monitoramento preventivo.")
if not tem_critico and not tem_atencao:
    st.success("Situacao geral controlada: nenhum alerta critico identificado.")

# Gerar alertas_agricolas.csv
alertas_df = df[df['alerta_previsto'].isin(['acao_recomendada', 'monitorar'])][
    ['data_hora', 'regiao', 'risco_previsto', 'confianca_modelo', 'alerta_previsto']
].copy()
alertas_df['mensagem_alerta'] = alertas_df['alerta_previsto'].map({
    'acao_recomendada': 'Acao imediata recomendada: irrigacao, analise do solo ou inspecao.',
    'monitorar':        'Monitorar o talhao. Risco moderado identificado.'
})
os.makedirs('data', exist_ok=True)
alertas_df.to_csv('data/alertas_agricolas.csv', index=False)

st.markdown("---")

# ============================================================
# FILTROS
# ============================================================
st.subheader("Filtros")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    regioes_sel = st.multiselect("Regiao", options=sorted(df['regiao'].unique()), default=sorted(df['regiao'].unique()))
with col_f2:
    riscos_sel  = st.multiselect("Risco Previsto", options=['saudavel', 'atencao', 'critico'], default=['saudavel', 'atencao', 'critico'])
with col_f3:
    alertas_sel = st.multiselect("Alerta Previsto", options=['sem_alerta', 'monitorar', 'acao_recomendada'], default=['sem_alerta', 'monitorar', 'acao_recomendada'])

df_filtrado = df[
    df['regiao'].isin(regioes_sel) &
    df['risco_previsto'].isin(riscos_sel) &
    df['alerta_previsto'].isin(alertas_sel)
]

st.markdown("---")

# ============================================================
# GRAFICOS
# ============================================================
st.subheader("Graficos")

col_g1, col_g2 = st.columns(2)

with col_g1:
    # Quantidade por risco previsto
    contagem_risco = df_filtrado['risco_previsto'].value_counts().reset_index()
    contagem_risco.columns = ['risco_previsto', 'quantidade']
    fig1 = px.bar(contagem_risco, x='risco_previsto', y='quantidade',
                  color='risco_previsto',
                  color_discrete_map={'saudavel': '#2ecc71', 'atencao': '#f39c12', 'critico': '#e74c3c'},
                  title='Registros por Risco Previsto')
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    # Umidade do solo por regiao
    umidade_regiao = df_filtrado.groupby('regiao')['umidade_solo_percentual'].mean().reset_index()
    fig2 = px.bar(umidade_regiao, x='regiao', y='umidade_solo_percentual',
                  color='regiao', title='Umidade do Solo Media por Regiao (%)')
    st.plotly_chart(fig2, use_container_width=True)

col_g3, col_g4 = st.columns(2)

with col_g3:
    # Indice de vegetacao por regiao
    veg_regiao = df_filtrado.groupby('regiao')['indice_vegetacao'].mean().reset_index()
    fig3 = px.bar(veg_regiao, x='regiao', y='indice_vegetacao',
                  color='regiao', title='Indice de Vegetacao Medio por Regiao')
    st.plotly_chart(fig3, use_container_width=True)

with col_g4:
    # Temperatura media por regiao
    temp_regiao = df_filtrado.groupby('regiao')['temperatura_c'].mean().reset_index()
    fig4 = px.bar(temp_regiao, x='regiao', y='temperatura_c',
                  color='regiao', title='Temperatura Media por Regiao (°C)')
    st.plotly_chart(fig4, use_container_width=True)

col_g5, col_g6 = st.columns(2)

with col_g5:
    # Alertas por regiao
    alertas_regiao = df_filtrado.groupby(['regiao', 'alerta_previsto']).size().reset_index(name='quantidade')
    fig5 = px.bar(alertas_regiao, x='regiao', y='quantidade', color='alerta_previsto',
                  color_discrete_map={'sem_alerta': '#2ecc71', 'monitorar': '#f39c12', 'acao_recomendada': '#e74c3c'},
                  title='Alertas por Regiao', barmode='stack')
    st.plotly_chart(fig5, use_container_width=True)

with col_g6:
    # Chuva media por regiao
    chuva_regiao = df_filtrado.groupby('regiao')['chuva_mm'].mean().reset_index()
    fig6 = px.bar(chuva_regiao, x='regiao', y='chuva_mm',
                  color='regiao', title='Chuva Media por Regiao (mm)')
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============================================================
# TABELA DE PREVISOES
# ============================================================
st.subheader("Tabela de Previsoes")
colunas_tabela = ['id_registro', 'data_hora', 'regiao', 'temperatura_c',
                  'umidade_solo_percentual', 'indice_vegetacao',
                  'risco_previsto', 'confianca_modelo', 'alerta_previsto']
st.dataframe(df_filtrado[colunas_tabela].head(50), use_container_width=True)

st.markdown("---")

# ============================================================
# VISAO COMPUTACIONAL
# ============================================================
st.subheader("Resultado da Visao Computacional")

col_v1, col_v2 = st.columns(2)

with col_v1:
    if os.path.exists(CAMINHO_IMAGEM):
        st.image(CAMINHO_IMAGEM, caption="Imagem processada — AgroOrbit AI", use_column_width=True)
    else:
        st.info("Imagem processada nao encontrada. Execute: python src/visao_computacional.py")

with col_v2:
    if os.path.exists(CAMINHO_VISAO):
        df_visao = pd.read_csv(CAMINHO_VISAO)
        row = df_visao.iloc[0]
        st.metric("Vegetacao Saudavel",  f"{row['percentual_vegetacao_saudavel']:.1f}%")
        st.metric("Area Seca",           f"{row['percentual_area_seca']:.1f}%")
        st.metric("Solo Exposto",        f"{row['percentual_solo_exposto']:.1f}%")
        st.metric("Risco Visual",        row['risco_visual'].upper())
        st.info(row['observacao'])
    else:
        st.info("Resultado da visao computacional nao encontrado. Execute: python src/visao_computacional.py")

st.markdown("---")

# ============================================================
# ARQUITETURA AWS
# ============================================================
st.subheader("Arquitetura AWS — Documentada como POC")
st.markdown("""
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
  Alerta Automatico
```

**Componentes:**
- **ESP32/Sensores:** coletam temperatura, umidade, chuva, pH, vento, luminosidade e indice de vegetacao.
- **API Gateway:** recebe os dados dos sensores via requisicao HTTP.
- **AWS Lambda:** processa os dados, aciona o modelo de ML e gera alertas.
- **DynamoDB/S3:** armazena historico de leituras e previsoes.
- **Dashboard Streamlit:** visualiza alertas, graficos e resultado da visao computacional em tempo real.

*Esta arquitetura e documentada como POC academica. Nao foi implantada em producao.*
""")

st.markdown("---")
st.caption("AgroOrbit AI — SUB Global Solution 2026.1 — FIAP Inteligencia Artificial")
