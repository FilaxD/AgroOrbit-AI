"""
gerar_dados_agricolas.py
Gera dados agrícolas simulados para o AgroOrbit AI.
Simula leituras de sensores ESP32 e índice de vegetação inspirado em satélite/NDVI.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Semente para reprodutibilidade
np.random.seed(42)

# Criar pasta data/ se não existir
os.makedirs('data', exist_ok=True)

print("Gerando dados agrícolas simulados...")

# Configurações gerais
NUM_REGISTROS = 500
REGIOES = ['Talhao_Norte', 'Talhao_Sul', 'Talhao_Leste', 'Talhao_Oeste', 'Talhao_Central']

# Coordenadas simuladas por talhão
COORDS = {
    'Talhao_Norte':   (-15.50, -47.80),
    'Talhao_Sul':     (-15.55, -47.80),
    'Talhao_Leste':   (-15.52, -47.75),
    'Talhao_Oeste':   (-15.52, -47.85),
    'Talhao_Central': (-15.52, -47.80),
}

# Gerar datas entre 2026-06-01 e 2026-06-10
data_inicio = datetime(2026, 6, 1)
datas = [data_inicio + timedelta(minutes=i * 29) for i in range(NUM_REGISTROS)]

# Gerar regiões aleatórias
regioes = np.random.choice(REGIOES, size=NUM_REGISTROS)

# Gerar variáveis climáticas e do solo
temperatura_c            = np.round(np.random.uniform(20, 42, NUM_REGISTROS), 1)
umidade_ar_percentual    = np.round(np.random.uniform(15, 90, NUM_REGISTROS), 1)
umidade_solo_percentual  = np.round(np.random.uniform(5, 80, NUM_REGISTROS), 1)
luminosidade_lux         = np.round(np.random.uniform(10000, 95000, NUM_REGISTROS), 0)
velocidade_vento_kmh     = np.round(np.random.uniform(0, 35, NUM_REGISTROS), 1)
chuva_mm                 = np.round(np.random.uniform(0, 25, NUM_REGISTROS), 1)
ph_solo                  = np.round(np.random.uniform(4.5, 8.5, NUM_REGISTROS), 2)
indice_vegetacao         = np.round(np.random.uniform(0.15, 0.95, NUM_REGISTROS), 3)


def calcular_risco(temp, umid_ar, umid_solo, chuva, idx_veg, ph, vento):
    """
    Calcula o risco agrícola com base em pontuação de indicadores críticos e de atenção.
    Retorna: saudavel, atencao ou critico
    """
    pontos = 0

    # Indicadores críticos (soma 2 pontos cada)
    if temp >= 35:               pontos += 2
    if umid_solo <= 25:          pontos += 2
    if umid_ar <= 30:            pontos += 2
    if chuva <= 2:               pontos += 2
    if idx_veg <= 0.35:          pontos += 2
    if ph < 5.5 or ph > 7.5:    pontos += 2
    if vento >= 25:              pontos += 2

    # Indicadores de atenção (soma 1 ponto cada)
    if 29 <= temp <= 34.99:                     pontos += 1
    if 26 <= umid_solo <= 45:                   pontos += 1
    if 31 <= umid_ar <= 50:                     pontos += 1
    if 2.1 <= chuva <= 8:                       pontos += 1
    if 0.36 <= idx_veg <= 0.60:                 pontos += 1
    if (5.5 <= ph <= 6.0) or (7.0 <= ph <= 7.5): pontos += 1
    if 15 <= vento <= 24.99:                    pontos += 1

    if pontos >= 8:   return 'critico'
    elif pontos >= 4: return 'atencao'
    else:             return 'saudavel'


# Calcular risco e alerta para cada registro
riscos = []
alertas = []
for i in range(NUM_REGISTROS):
    risco = calcular_risco(
        temperatura_c[i], umidade_ar_percentual[i], umidade_solo_percentual[i],
        chuva_mm[i], indice_vegetacao[i], ph_solo[i], velocidade_vento_kmh[i]
    )
    riscos.append(risco)
    alertas.append({'saudavel': 'sem_alerta', 'atencao': 'monitorar', 'critico': 'acao_recomendada'}[risco])

# Montar latitude e longitude por talhão
latitudes  = [COORDS[r][0] + np.random.uniform(-0.01, 0.01) for r in regioes]
longitudes = [COORDS[r][1] + np.random.uniform(-0.01, 0.01) for r in regioes]

# Montar DataFrame
df = pd.DataFrame({
    'id_registro':             range(1, NUM_REGISTROS + 1),
    'data_hora':               [d.strftime('%Y-%m-%d %H:%M:%S') for d in datas],
    'regiao':                  regioes,
    'latitude':                np.round(latitudes, 5),
    'longitude':               np.round(longitudes, 5),
    'temperatura_c':           temperatura_c,
    'umidade_ar_percentual':   umidade_ar_percentual,
    'umidade_solo_percentual': umidade_solo_percentual,
    'luminosidade_lux':        luminosidade_lux,
    'velocidade_vento_kmh':    velocidade_vento_kmh,
    'chuva_mm':                chuva_mm,
    'ph_solo':                 ph_solo,
    'indice_vegetacao':        indice_vegetacao,
    'risco_agricola':          riscos,
    'alerta':                  alertas,
})

# Salvar CSV
df.to_csv('data/dados_agricolas.csv', index=False)

print(f"\nDados gerados: {len(df)} registros")
print(f"Arquivo salvo em: data/dados_agricolas.csv")
print(f"\nPrevia dos dados:")
print(df.head())
print(f"\nDistribuicao das classes de risco:")
print(df['risco_agricola'].value_counts())
print(f"\nDistribuicao dos alertas:")
print(df['alerta'].value_counts())
