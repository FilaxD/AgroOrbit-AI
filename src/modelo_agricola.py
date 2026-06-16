"""
modelo_agricola.py
Treina um modelo de Machine Learning (RandomForestClassifier) para classificar
o risco agricola com base em variaveis ambientais e de solo.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Criar pasta models/ se nao existir
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

print("Carregando dados...")

# Carregar dataset
CAMINHO_DADOS = 'data/dados_agricolas.csv'
if not os.path.exists(CAMINHO_DADOS):
    print("Arquivo de dados nao encontrado. Execute primeiro:")
    print("  python src/gerar_dados_agricolas.py")
    exit(1)

df = pd.read_csv(CAMINHO_DADOS)

# Validar colunas obrigatorias
COLUNAS_OBRIGATORIAS = [
    'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
    'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm',
    'ph_solo', 'indice_vegetacao', 'risco_agricola'
]
for col in COLUNAS_OBRIGATORIAS:
    if col not in df.columns:
        print(f"Coluna obrigatoria ausente: {col}")
        exit(1)

# Remover linhas com valores ausentes nas colunas importantes
df = df.dropna(subset=COLUNAS_OBRIGATORIAS)
print(f"Registros validos: {len(df)}")

# Separar features e target
FEATURES = [
    'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
    'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm',
    'ph_solo', 'indice_vegetacao'
]
TARGET = 'risco_agricola'

X = df[FEATURES]
y = df[TARGET]

# Divisao treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTreino: {len(X_train)} registros | Teste: {len(X_test)} registros")

# Treinar modelo
print("\nTreinando RandomForestClassifier...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)

# Avaliar modelo
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)

print(f"\nAcuracia no conjunto de teste: {acuracia:.4f}")
print("\nMatriz de Confusao:")
print(confusion_matrix(y_test, y_pred))
print("\nRelatorio de Classificacao:")
print(classification_report(y_test, y_pred))

# Salvar modelo
joblib.dump(modelo, 'models/modelo_agricola.pkl')
print("\nModelo salvo em: models/modelo_agricola.pkl")

# Gerar previsoes para todo o dataset
print("\nGerando previsoes para todo o dataset...")
X_full = df[FEATURES]
df['risco_previsto']   = modelo.predict(X_full)
proba                  = modelo.predict_proba(X_full)
df['confianca_modelo'] = np.round(np.max(proba, axis=1), 4)

# Mapear alerta_previsto
mapa_alerta = {'saudavel': 'sem_alerta', 'atencao': 'monitorar', 'critico': 'acao_recomendada'}
df['alerta_previsto'] = df['risco_previsto'].map(mapa_alerta)

# Salvar previsoes
COLUNAS_PREVISAO = [
    'id_registro', 'data_hora', 'regiao', 'latitude', 'longitude',
    'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
    'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm',
    'ph_solo', 'indice_vegetacao', 'risco_agricola',
    'risco_previsto', 'confianca_modelo', 'alerta_previsto'
]
df[COLUNAS_PREVISAO].to_csv('data/previsoes_agricolas.csv', index=False)

print("Previsoes salvas em: data/previsoes_agricolas.csv")
print("\nPrevia das previsoes:")
print(df[['regiao', 'risco_agricola', 'risco_previsto', 'confianca_modelo', 'alerta_previsto']].head(10))
print("\nDistribuicao das previsoes:")
print(df['risco_previsto'].value_counts())
