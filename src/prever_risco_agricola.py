"""
prever_risco_agricola.py
Carrega o modelo treinado e realiza a previsao de risco para uma nova leitura agricola.
"""

import os
import joblib
import pandas as pd
import numpy as np

CAMINHO_MODELO = 'models/modelo_agricola.pkl'

# Verificar se o modelo existe
if not os.path.exists(CAMINHO_MODELO):
    print("Modelo nao encontrado.")
    print("Execute primeiro:")
    print("  python src/modelo_agricola.py")
    exit(1)

# Carregar modelo
modelo = joblib.load(CAMINHO_MODELO)

# Nova leitura critica para teste
nova_leitura = {
    'temperatura_c':            38.0,
    'umidade_ar_percentual':    24.0,
    'umidade_solo_percentual':  18.0,
    'luminosidade_lux':         89000.0,
    'velocidade_vento_kmh':     28.0,
    'chuva_mm':                 0.8,
    'ph_solo':                  8.0,
    'indice_vegetacao':         0.28,
}

FEATURES = [
    'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
    'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm',
    'ph_solo', 'indice_vegetacao'
]

# Montar DataFrame de entrada
X_novo = pd.DataFrame([nova_leitura])[FEATURES]

# Realizar previsao
risco_previsto   = modelo.predict(X_novo)[0]
proba            = modelo.predict_proba(X_novo)[0]
confianca        = round(float(np.max(proba)) * 100, 2)

# Mapear alerta
mapa_alerta = {'saudavel': 'sem_alerta', 'atencao': 'monitorar', 'critico': 'acao_recomendada'}
alerta_previsto = mapa_alerta[risco_previsto]

# Exibir resultado
print("=" * 50)
print("  AGROORBIT AI — PREVISAO DE RISCO AGRICOLA")
print("=" * 50)
print("\nValores de entrada:")
for chave, valor in nova_leitura.items():
    print(f"  {chave}: {valor}")
print(f"\nRisco previsto:   {risco_previsto.upper()}")
print(f"Confianca:        {confianca}%")
print(f"Alerta previsto:  {alerta_previsto}")

if risco_previsto == 'critico':
    print("\nACIONAR ACAO IMEDIATA: irrigacao, analise do solo ou inspecao da lavoura.")
elif risco_previsto == 'atencao':
    print("\nMonitorar o talhao com frequencia. Risco moderado identificado.")
else:
    print("\nCondicoes dentro do esperado. Nenhuma acao urgente necessaria.")

print("=" * 50)
