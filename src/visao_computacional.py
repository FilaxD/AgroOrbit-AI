"""
visao_computacional.py
Analisa uma imagem de lavoura usando OpenCV para identificar areas de
vegetacao saudavel, vegetacao seca e solo exposto.

Esta etapa usa OpenCV como POC. Em uma versao futura, poderia ser substituida
por YOLO treinado com imagens reais de lavouras saudaveis, secas e degradadas.
"""

import os
import cv2
import numpy as np
import pandas as pd

# Criar pastas necessarias
os.makedirs('images', exist_ok=True)
os.makedirs('data', exist_ok=True)

CAMINHO_IMAGEM   = 'images/imagem_lavoura.jpg'
CAMINHO_RESULTADO = 'images/resultado_visao.jpg'


def criar_imagem_sintetica():
    """
    Cria uma imagem sintetica simulando areas de lavoura:
    - Verde: vegetacao saudavel
    - Amarelo/marrom: vegetacao seca
    - Cinza/marrom escuro: solo exposto
    """
    altura, largura = 480, 640
    imagem = np.zeros((altura, largura, 3), dtype=np.uint8)

    # Area verde — vegetacao saudavel (parte superior)
    imagem[0:180, :] = [34, 139, 34]       # verde floresta (BGR)

    # Area amarela — vegetacao seca (parte central)
    imagem[180:340, :] = [32, 165, 218]    # amarelo ouro (BGR)

    # Area marrom — solo exposto (parte inferior)
    imagem[340:480, :] = [42, 74, 101]     # marrom solo (BGR)

    # Adicionar variacao para parecer mais realista
    noise = np.random.randint(-20, 20, imagem.shape, dtype=np.int16)
    imagem = np.clip(imagem.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    cv2.imwrite(CAMINHO_IMAGEM, imagem)
    print("Imagem sintetica criada em: images/imagem_lavoura.jpg")
    return imagem


def analisar_imagem(imagem):
    """
    Analisa a imagem e detecta areas por cor usando mascaras HSV.
    Retorna percentuais de cada tipo de area.
    """
    # Converter para HSV para melhor segmentacao por cor
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    total_pixels = imagem.shape[0] * imagem.shape[1]

    # Mascara para vegetacao saudavel (tons de verde)
    verde_baixo  = np.array([35, 40, 40])
    verde_alto   = np.array([85, 255, 255])
    mascara_verde = cv2.inRange(hsv, verde_baixo, verde_alto)

    # Mascara para vegetacao seca (tons amarelos e laranjas)
    amarelo_baixo = np.array([15, 40, 40])
    amarelo_alto  = np.array([34, 255, 255])
    mascara_seca  = cv2.inRange(hsv, amarelo_baixo, amarelo_alto)

    # Solo exposto: o que nao e verde nem amarelo (tons marrons/cinza)
    mascara_solo = cv2.bitwise_not(cv2.bitwise_or(mascara_verde, mascara_seca))

    # Calcular percentuais
    pct_verde = round(cv2.countNonZero(mascara_verde) / total_pixels * 100, 2)
    pct_seca  = round(cv2.countNonZero(mascara_seca)  / total_pixels * 100, 2)
    pct_solo  = round(100 - pct_verde - pct_seca, 2)
    pct_solo  = max(0, pct_solo)

    return mascara_verde, mascara_seca, mascara_solo, pct_verde, pct_seca, pct_solo


def gerar_resultado_visual(imagem, mascara_verde, mascara_seca, pct_verde, pct_seca, pct_solo, risco):
    """
    Gera imagem marcada com contornos e texto indicando cada area detectada.
    """
    resultado = imagem.copy()

    # Desenhar contorno da area verde
    contornos_verde, _ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(resultado, contornos_verde, -1, (0, 255, 0), 2)

    # Desenhar contorno da area seca
    contornos_seca, _ = cv2.findContours(mascara_seca, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(resultado, contornos_seca, -1, (0, 165, 255), 2)

    # Adicionar textos na imagem
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(resultado, f"Veg. Saudavel: {pct_verde:.1f}%",  (10, 30),  fonte, 0.7, (0, 255, 0),   2)
    cv2.putText(resultado, f"Area Seca:     {pct_seca:.1f}%",   (10, 60),  fonte, 0.7, (0, 165, 255), 2)
    cv2.putText(resultado, f"Solo Exposto:  {pct_solo:.1f}%",   (10, 90),  fonte, 0.7, (42, 74, 101), 2)
    cv2.putText(resultado, f"Risco Visual:  {risco.upper()}",   (10, 120), fonte, 0.7, (0, 0, 255),   2)

    cv2.imwrite(CAMINHO_RESULTADO, resultado)
    print(f"Imagem processada salva em: {CAMINHO_RESULTADO}")


# Carregar ou criar imagem
if os.path.exists(CAMINHO_IMAGEM):
    print(f"Carregando imagem: {CAMINHO_IMAGEM}")
    imagem = cv2.imread(CAMINHO_IMAGEM)
else:
    print("Imagem nao encontrada. Criando imagem sintetica...")
    imagem = criar_imagem_sintetica()

# Analisar imagem
mascara_verde, mascara_seca, mascara_solo, pct_verde, pct_seca, pct_solo = analisar_imagem(imagem)

# Determinar classe predominante
valores = {'vegetacao_saudavel': pct_verde, 'vegetacao_seca': pct_seca, 'solo_exposto': pct_solo}
if max(pct_verde, pct_seca, pct_solo) < 50:
    classe_predominante = 'misto'
else:
    classe_predominante = max(valores, key=valores.get)

# Determinar risco visual
soma_risco = pct_seca + pct_solo
if soma_risco >= 45:
    risco_visual = 'critico'
    observacao   = 'Alta proporcao de area seca ou solo exposto. Acao urgente recomendada.'
elif soma_risco >= 25:
    risco_visual = 'atencao'
    observacao   = 'Area com sinais de estresse. Monitorar com frequencia.'
else:
    risco_visual = 'saudavel'
    observacao   = 'Vegetacao em boas condicoes visuais.'

# Gerar imagem marcada
gerar_resultado_visual(imagem, mascara_verde, mascara_seca, pct_verde, pct_seca, pct_solo, risco_visual)

# Salvar resultado em CSV
resultado_csv = pd.DataFrame([{
    'imagem':                       'imagem_lavoura.jpg',
    'classe_visual_predominante':   classe_predominante,
    'percentual_vegetacao_saudavel': pct_verde,
    'percentual_area_seca':         pct_seca,
    'percentual_solo_exposto':      pct_solo,
    'risco_visual':                 risco_visual,
    'observacao':                   observacao,
}])
resultado_csv.to_csv('data/resultado_visao.csv', index=False)

# Exibir resultado no terminal
print("\nResultado da analise visual:")
print(f"  Vegetacao saudavel: {pct_verde:.2f}%")
print(f"  Area seca:          {pct_seca:.2f}%")
print(f"  Solo exposto:       {pct_solo:.2f}%")
print(f"  Classe predominante: {classe_predominante}")
print(f"  Risco visual:       {risco_visual.upper()}")
print(f"  Observacao:         {observacao}")
print("\nResultado salvo em: data/resultado_visao.csv")
