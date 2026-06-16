"""
validar_projeto.py
Valida se todos os arquivos e colunas obrigatorias do AgroOrbit AI estao corretos.
"""

import os
import pandas as pd

VERDE   = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
RESET   = "\033[0m"

erros = []

def ok(msg):
    print(f"{VERDE}[OK]{RESET} {msg}")

def erro(msg):
    print(f"{VERMELHO}[ERRO]{RESET} {msg}")
    erros.append(msg)

def aviso(msg):
    print(f"{AMARELO}[AVISO]{RESET} {msg}")


print("=" * 55)
print("  VALIDANDO PROJETO AGROORBIT AI")
print("=" * 55)

# 1. Verificar arquivos obrigatorios
print("\nVerificando arquivos obrigatorios...")
ARQUIVOS = [
    'data/dados_agricolas.csv',
    'data/previsoes_agricolas.csv',
    'data/resultado_visao.csv',
    'data/alertas_agricolas.csv',
    'images/resultado_visao.jpg',
    'models/modelo_agricola.pkl',
    'README.md',
    'requirements.txt',
]
for arq in ARQUIVOS:
    if os.path.exists(arq):
        ok(arq)
    else:
        erro(f"Arquivo nao encontrado: {arq}")

# 2. Validar colunas dos CSVs
print("\nValidando colunas dos arquivos CSV...")

COLUNAS_ESPERADAS = {
    'data/dados_agricolas.csv': [
        'id_registro', 'data_hora', 'regiao', 'latitude', 'longitude',
        'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
        'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm', 'ph_solo',
        'indice_vegetacao', 'risco_agricola', 'alerta'
    ],
    'data/previsoes_agricolas.csv': [
        'id_registro', 'data_hora', 'regiao', 'latitude', 'longitude',
        'temperatura_c', 'umidade_ar_percentual', 'umidade_solo_percentual',
        'luminosidade_lux', 'velocidade_vento_kmh', 'chuva_mm', 'ph_solo',
        'indice_vegetacao', 'risco_agricola', 'risco_previsto',
        'confianca_modelo', 'alerta_previsto'
    ],
    'data/resultado_visao.csv': [
        'imagem', 'classe_visual_predominante',
        'percentual_vegetacao_saudavel', 'percentual_area_seca',
        'percentual_solo_exposto', 'risco_visual', 'observacao'
    ],
    'data/alertas_agricolas.csv': [
        'data_hora', 'regiao', 'risco_previsto',
        'confianca_modelo', 'alerta_previsto', 'mensagem_alerta'
    ],
}

for caminho, colunas in COLUNAS_ESPERADAS.items():
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        faltando = [c for c in colunas if c not in df.columns]
        if faltando:
            erro(f"{caminho} — colunas faltando: {faltando}")
        else:
            ok(f"{caminho} — todas as colunas presentes")

# 3. Validar valores permitidos
print("\nValidando valores permitidos...")

VALORES_PERMITIDOS = {
    ('data/dados_agricolas.csv',    'risco_agricola'): ['saudavel', 'atencao', 'critico'],
    ('data/dados_agricolas.csv',    'alerta'):         ['sem_alerta', 'monitorar', 'acao_recomendada'],
    ('data/previsoes_agricolas.csv','risco_previsto'): ['saudavel', 'atencao', 'critico'],
    ('data/previsoes_agricolas.csv','alerta_previsto'):['sem_alerta', 'monitorar', 'acao_recomendada'],
    ('data/resultado_visao.csv',    'risco_visual'):   ['saudavel', 'atencao', 'critico'],
}

for (caminho, coluna), valores in VALORES_PERMITIDOS.items():
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        if coluna in df.columns:
            invalidos = df[~df[coluna].isin(valores)][coluna].unique()
            if len(invalidos) > 0:
                erro(f"{caminho} [{coluna}] — valores invalidos: {invalidos}")
            else:
                ok(f"{caminho} [{coluna}] — valores validos")

# Resultado final
print("\n" + "=" * 55)
if not erros:
    print(f"{VERDE}PROJETO AGROORBIT AI PRONTO PARA ENTREGA{RESET}")
else:
    print(f"{VERMELHO}ENCONTRADOS {len(erros)} PROBLEMA(S):{RESET}")
    for e in erros:
        print(f"  - {e}")
print("=" * 55)
