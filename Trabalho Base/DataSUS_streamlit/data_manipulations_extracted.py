# Cell 1
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import unicodedata
import requests

# Cell 2
dados = pd.read_csv('dados_limpos.csv')

# Cell 3
dados.info()

# Cell 4
nulos = dados.isnull().sum()
print(nulos)

# Cell 5
municipios = pd.read_csv('municipios.csv', sep=',', encoding='utf-8')  # Verifique o separador e a codificação correta

# Cell 6
dados = dados.dropna(subset=['SP_CIDADE_P'])

# Cell 7
municipios.info()

# Cell 8
# Função para normalizar nomes de cidades
def normalize_city_name(name):
    if isinstance(name, str):
        return ''.join(c for c in unicodedata.normalize('NFKD', name) if not unicodedata.combining(c)).lower().strip()
    else:
        return ''

# Cell 9
# Aplicar normalização às colunas relevantes
dados['SP_CIDADE_H_norm'] = dados['SP_CIDADE_H'].apply(normalize_city_name)
dados['SP_CIDADE_P_norm'] = dados['SP_CIDADE_P'].apply(normalize_city_name)
dados['SP_CIDADE_P_EXT_norm'] = dados['SP_CIDADE_P_EXT'].apply(normalize_city_name)
municipios['nome_norm'] = municipios['nome'].apply(normalize_city_name)

# Cell 10
# Mesclar os DataFrames utilizando as colunas normalizadas
dados = dados.merge(municipios[['nome_norm', 'latitude', 'longitude']], how='left', left_on='SP_CIDADE_H_norm', right_on='nome_norm')
dados.rename(columns={'latitude': 'latitude_h', 'longitude': 'longitude_h'}, inplace=True)
dados.drop(columns=['SP_CIDADE_H_norm', 'nome_norm'], inplace=True)

dados = dados.merge(municipios[['nome_norm', 'latitude', 'longitude']], how='left', left_on='SP_CIDADE_P_norm', right_on='nome_norm')
dados.rename(columns={'latitude': 'latitude_p', 'longitude': 'longitude_p'}, inplace=True)
dados.drop(columns=['SP_CIDADE_P_norm', 'nome_norm'], inplace=True)

dados = dados.merge(municipios[['nome_norm', 'latitude', 'longitude']], how='left', left_on='SP_CIDADE_P_EXT_norm', right_on='nome_norm')
dados.rename(columns={'latitude': 'latitude_p_ext', 'longitude': 'longitude_p_ext'}, inplace=True)
dados.drop(columns=['SP_CIDADE_P_EXT_norm', 'nome_norm'], inplace=True)

# Cell 11
# # Mesclar para 'SP_CIDADE_H'
# dados = dados.merge(municipios[['nome', 'latitude', 'longitude']],
#                     how='left', left_on='SP_CIDADE_H', right_on='nome')
# dados.rename(columns={'latitude': 'latitude_h', 'longitude': 'longitude_h'}, inplace=True)
# dados.drop(columns=['nome'], inplace=True)  # Drop a coluna auxiliar 'nome' do município
# #
# # Mesclar para 'SP_CIDADE_P'
# dados = dados.merge(municipios[['nome', 'latitude', 'longitude']],
#                     how='left', left_on='SP_CIDADE_P', right_on='nome')
# dados.rename(columns={'latitude': 'latitude_p', 'longitude': 'longitude_p'}, inplace=True)
# dados.drop(columns=['nome'], inplace=True)  # Drop a coluna auxiliar 'nome' do município

# # Mesclar para 'SP_CIDADE_P_EXT'
# dados = dados.merge(municipios[['nome', 'latitude', 'longitude']],
#                     how='left', left_on='SP_CIDADE_P_EXT', right_on='nome')
# dados.rename(columns={'latitude': 'latitude_p_ext', 'longitude': 'longitude_p_ext'}, inplace=True)
# dados.drop(columns=['nome'], inplace=True)  # Drop a coluna auxiliar 'nome' do município

# # Exibir o resultado
# print(dados.head())

# Cell 12
dados.info()

# Cell 13
nulos = dados.isnull().sum()

# Cell 14
print(nulos)

# Cell 15
print(dados.columns)

# Cell 16
dados = dados.loc[:,~dados.columns.duplicated()]

# Cell 17
# Criando uma máscara booleana para identificar linhas onde a coluna SP_CIDADE_P é nula
mask = dados['latitude_p'].isnull()

# Aplicando a máscara para filtrar as linhas e selecionando as colunas desejadas para visualização
linhas_nulas = dados.loc[mask, ['SP_DES_HOS','SP_CIDADE_H', 'SP_CIDADE_P',
                             'SP_CIDADE_P_EXT', 'SP_N_PROC', 'SP_N_ATOS',
                             'latitude_h', 'longitude_h', 'latitude_p', 'longitude_p',
                             'latitude_p_ext', 'longitude_p_ext']]

# Imprimindo algumas linhas para visualização
print(linhas_nulas.head())

# Cell 18
# Remover duplicatas mantendo apenas a primeira ocorrência
dados = dados.drop_duplicates()

# Exibir o resultado
print(dados.info())

# Cell 19
# Substituir NaN em latitude_p e longitude_p por "cidades de fora RS"
dados['latitude_p_ext'].fillna('cidade do RS', inplace=True)
dados['longitude_p_ext'].fillna('cidade do RS', inplace=True)

# Exibir o resultado
print(dados.head())

# Cell 20
dados.info()

# Cell 21
contador = dados['longitude_p_ext'].value_counts()
print(contador)

# Cell 22
contagem_naih = dados['SP_NAIH'].nunique()

print(f"Quantidade de valores únicos na coluna SP_NAIH: {contagem_naih}")

# Cell 23
dados_sem_duplicatas = dados.drop_duplicates(subset=['SP_NAIH', 'SP_N_PROC'])

# Contar quantos procedimentos únicos cada paciente teve
contagem_procedimentos = dados_sem_duplicatas.groupby('SP_N_PROC')['SP_N_PROC'].size()

print(contagem_procedimentos)
valor = contagem_procedimentos.value_counts()
print(valor)

# Cell 24
cidades_acima_menos25 = dados[dados['latitude_h'] < -25]

contagem_cidades_acima_menos25 = cidades_acima_menos25['SP_CIDADE_H'].nunique()

# Mostrar as linhas onde latitude_h está entre -25 e 0
linhas_latitude_entre_menos25_e_zero = dados[(dados['latitude_h'] > -25) & (dados['latitude_h'] <= 0)]

# Exibir os resultados
print(f"Cidades com latitude acima de -25: {contagem_cidades_acima_menos25}")
print("\nLinhas com latitude entre -25 e 0:")
print(linhas_latitude_entre_menos25_e_zero)

# Cell 25
# Filtrar as cidades com latitude acima de -25
cidades_acima_menos25 = dados[dados['latitude_h'] > -25]

# Selecionar apenas as colunas de interesse: nome da cidade e latitude
resultado = cidades_acima_menos25[['SP_CIDADE_H', 'latitude_h']]

# Exibir os resultados
print("Cidades com latitude acima de -25:")
print(resultado)

# Cell 26
# Filtrar as cidades com latitude acima de -25
cidades_acima_menos25 = dados[dados['latitude_h'] > -25]

# Contar o número de cidades únicas
numero_cidades_acima_menos25 = cidades_acima_menos25['SP_CIDADE_H'].nunique()

# Exibir o resultado
print(f"Número de cidades com latitude acima de -25: {numero_cidades_acima_menos25}")

# Cell 27
# Filtrar as cidades com latitude acima de -25
cidades_acima_menos25 = dados[dados['latitude_h'] > -25]

# Obter as informações relevantes (nome, latitude, longitude)
cidades_info = cidades_acima_menos25[['SP_CIDADE_H', 'latitude_h', 'longitude_h']].drop_duplicates()

# Exibir o resultado
print("Cidades com latitude acima de -25:")
for index, row in cidades_info.iterrows():
    print(f"Nome: {row['SP_CIDADE_H']}, Latitude: {row['latitude_h']}, Longitude: {row['longitude_h']}")

# Cell 28
# Verificar se existe a cidade "Lajeado do Bugre"
cidade_lajeado_bugre = dados[dados['SP_CIDADE_P'] == 'LAJEADO DO BUGRE']

# Exibir o resultado
if not cidade_lajeado_bugre.empty:
    print("A cidade 'Lajeado do Bugre' foi encontrada.")
else:
    print("A cidade 'Lajeado do Bugre' não foi encontrada.")

# Cell 29
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Filtrar as cidades fora do Rio Grande do Sul com latitude > -25
cidades_foras_rgs = dados[dados['latitude_h'] > -25]

# Criar uma lista para armazenar os resultados
resultados = []

# Iterar sobre as cidades fora do Rio Grande do Sul
for index, row in cidades_foras_rgs.iterrows():
    nome_cidade = row['SP_CIDADE_H']
    latitude_for = row['latitude_h']
    
    # Verificar se existe uma cidade com o mesmo nome e latitude < -25 no municipios.csv
    cidade_info = municipios[municipios['nome'] == nome_cidade]
    cidade_rgs = cidade_info[cidade_info['latitude'] < -25]
    
    # Se a cidade for encontrada, adicionar à lista de resultados
    if not cidade_rgs.empty:
        resultados.append((nome_cidade, latitude_for))

# Exibir os resultados
if resultados:
    print("Cidades fora do Rio Grande do Sul com latitude maior que -25 que têm cidades com o mesmo nome no RS:")
    for cidade, lat in resultados:
        print(f"{cidade} (latitude fora do RS: {lat})")
else:
    print("Não foram encontradas cidades fora do Rio Grande do Sul com latitude maior que -25 que têm cidades com o mesmo nome no RS.")

# Cell 30
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Filtrar as linhas correspondentes no DataFrame de municípios (sem considerar maiúsculas/minúsculas)
    cidade_info = municipios[municipios['nome'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada e se sua latitude é menor que -25
    if not cidade_info.empty:
        lat = cidade_info['latitude'].values[0]
        lon = cidade_info['longitude'].values[0]
        
        if lat < -25:  # Verifica se a latitude é menor que -25
            cidades_info.append((cidade, lat, lon))

# Exibir os resultados
print("Cidades com latitude menor que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 31
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Filtrar as linhas correspondentes no DataFrame de municípios sem diferenciar maiúsculas de minúsculas
    cidade_info = municipios[municipios['nome'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada e se sua latitude é menor que -25
    if not cidade_info.empty:
        lat = cidade_info['latitude'].values[0]
        lon = cidade_info['longitude'].values[0]
        
        if lat < -25:  # Verifica se a latitude é menor que -25
            cidades_info.append((cidade_info['nome'].values[0], lat, lon))

# Exibir os resultados
print("Cidades com latitude menor que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 32
# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Cidade que você quer modificar
cidade_especifica = "SARANDI"

# Novos valores de latitude e longitude
nova_latitude = -27.942
nova_longitude = -52.9231

# Alterar a latitude e longitude de todas as ocorrências da cidade específica
municipios.loc[municipios['nome'].str.lower() == cidade_especifica.lower(), ['latitude', 'longitude']] = [nova_latitude, nova_longitude]

# Verificar se a alteração foi aplicada
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Cell 33
# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Cidade que você quer modificar
cidade_especifica = "MARAU"

# Novos valores de latitude e longitude
nova_latitude = -28.4498
nova_longitude = -52.1986

# Alterar a latitude e longitude de todas as ocorrências da cidade específica
municipios.loc[municipios['nome'].str.lower() == cidade_especifica.lower(), ['latitude', 'longitude']] = [nova_latitude, nova_longitude]

# Verificar se a alteração foi aplicada
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Cell 34
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Cidade que você quer modificar
cidade_especifica = "SARANDI"

# Novos valores de latitude e longitude
nova_latitude = -27.942
nova_longitude = -52.9231

# Mostrar todas as ocorrências da cidade antes da alteração
print("Antes da alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude de todas as ocorrências da cidade específica
municipios.loc[municipios['nome'].str.lower() == cidade_especifica.lower(), ['latitude', 'longitude']] = [nova_latitude, nova_longitude]

# Mostrar todas as ocorrências da cidade após a alteração
print("\nApós a alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Cell 35
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Cidade que você quer modificar
cidade_especifica = "MARAU"

# Novos valores de latitude e longitude
nova_latitude = -28.4498
nova_longitude = -52.1986

# Mostrar todas as ocorrências da cidade antes da alteração
print("Antes da alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude de todas as ocorrências da cidade específica
municipios.loc[municipios['nome'].str.lower() == cidade_especifica.lower(), ['latitude', 'longitude']] = [nova_latitude, nova_longitude]

# Mostrar todas as ocorrências da cidade após a alteração
print("\nApós a alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Cell 36
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Filtrar as linhas correspondentes no DataFrame de municípios sem diferenciar maiúsculas de minúsculas
    cidade_info = municipios[municipios['nome'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada e se sua latitude é maior que -25
    if not cidade_info.empty:
        lat = cidade_info['latitude'].values[0]
        lon = cidade_info['longitude'].values[0]
        
        if lat > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info['nome'].values[0], lat, lon))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 37
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Cidade que você quer modificar
cidade_especifica = "SARANDI"

# Novos valores de latitude e longitude
nova_latitude = -27.942
nova_longitude = -52.9231

# Mostrar todas as ocorrências da cidade antes da alteração
print("Antes da alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude de todas as ocorrências da cidade específica
municipios.loc[municipios['nome'].str.lower() == cidade_especifica.lower(), ['latitude', 'longitude']] = [nova_latitude, nova_longitude]

# Mostrar todas as ocorrências da cidade após a alteração
print("\nApós a alteração:")
print(municipios[municipios['nome'].str.lower() == cidade_especifica.lower()])

# Cell 38
import pandas as pd

# Carregar o arquivo municipios.csv
municipios = pd.read_csv('municipios.csv')

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Filtrar as linhas correspondentes no DataFrame de municípios sem diferenciar maiúsculas de minúsculas
    cidade_info = municipios[municipios['nome'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada e se sua latitude é maior que -25
    if not cidade_info.empty:
        lat = cidade_info['latitude'].values[0]
        lon = cidade_info['longitude'].values[0]
        
        if lat > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info['nome'].values[0], lat, lon))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 39
print(dados.columns)

# Cell 40
print(dados.tail)

# Cell 41
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SARANDI"

# Novos valores de latitude e longitude
nova_latitude = -27.942
nova_longitude = -52.9231

# Mostrar as ocorrências da cidade em 'SP_CIDADE_H' antes da alteração
print("Antes da alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade em 'SP_CIDADE_P' antes da alteração
print("\nAntes da alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_H'
print("\nApós a alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_P'
print("\nApós a alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Cell 42
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Procurar nas colunas 'SP_CIDADE_H' e 'SP_CIDADE_P' sem diferenciar maiúsculas de minúsculas
    cidade_info_h = dados[dados['SP_CIDADE_H'].str.lower() == cidade.lower()]
    cidade_info_p = dados[dados['SP_CIDADE_P'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_H' e se sua latitude é maior que -25
    if not cidade_info_h.empty:
        lat_h = cidade_info_h['latitude_h'].values[0]
        lon_h = cidade_info_h['longitude_h'].values[0]
        
        if lat_h > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_h['SP_CIDADE_H'].values[0], lat_h, lon_h))

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_P' e se sua latitude é maior que -25
    if not cidade_info_p.empty:
        lat_p = cidade_info_p['latitude_p'].values[0]
        lon_p = cidade_info_p['longitude_p'].values[0]
        
        if lat_p > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_p['SP_CIDADE_P'].values[0], lat_p, lon_p))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 43
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "PLANALTO"

# Novos valores de latitude e longitude
nova_latitude = -27.3297
nova_longitude = -53.0575

# Mostrar as ocorrências da cidade em 'SP_CIDADE_H' antes da alteração
print("Antes da alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade em 'SP_CIDADE_P' antes da alteração
print("\nAntes da alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_H'
print("\nApós a alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_P'
print("\nApós a alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Cell 44
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Procurar nas colunas 'SP_CIDADE_H' e 'SP_CIDADE_P' sem diferenciar maiúsculas de minúsculas
    cidade_info_h = dados[dados['SP_CIDADE_H'].str.lower() == cidade.lower()]
    cidade_info_p = dados[dados['SP_CIDADE_P'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_H' e se sua latitude é maior que -25
    if not cidade_info_h.empty:
        lat_h = cidade_info_h['latitude_h'].values[0]
        lon_h = cidade_info_h['longitude_h'].values[0]
        
        if lat_h > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_h['SP_CIDADE_H'].values[0], lat_h, lon_h))

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_P' e se sua latitude é maior que -25
    if not cidade_info_p.empty:
        lat_p = cidade_info_p['latitude_p'].values[0]
        lon_p = cidade_info_p['longitude_p'].values[0]
        
        if lat_p > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_p['SP_CIDADE_P'].values[0], lat_p, lon_p))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 45
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "VERA CRUZ"

# Novos valores de latitude e longitude
nova_latitude = -29.7184
nova_longitude = -52.5152

# Mostrar as ocorrências da cidade em 'SP_CIDADE_H' antes da alteração
print("Antes da alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade em 'SP_CIDADE_P' antes da alteração
print("\nAntes da alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_H'
print("\nApós a alteração (SP_CIDADE_H):")
print(dados[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower()])

# Mostrar as ocorrências da cidade após a alteração em 'SP_CIDADE_P'
print("\nApós a alteração (SP_CIDADE_P):")
print(dados[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower()])

# Cell 46
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Procurar nas colunas 'SP_CIDADE_H' e 'SP_CIDADE_P' sem diferenciar maiúsculas de minúsculas
    cidade_info_h = dados[dados['SP_CIDADE_H'].str.lower() == cidade.lower()]
    cidade_info_p = dados[dados['SP_CIDADE_P'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_H' e se sua latitude é maior que -25
    if not cidade_info_h.empty:
        lat_h = cidade_info_h['latitude_h'].values[0]
        lon_h = cidade_info_h['longitude_h'].values[0]
        
        if lat_h > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_h['SP_CIDADE_H'].values[0], lat_h, lon_h))

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_P' e se sua latitude é maior que -25
    if not cidade_info_p.empty:
        lat_p = cidade_info_p['latitude_p'].values[0]
        lon_p = cidade_info_p['longitude_p'].values[0]
        
        if lat_p > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_p['SP_CIDADE_P'].values[0], lat_p, lon_p))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 47
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "LAJEADO"

# Novos valores de latitude e longitude
nova_latitude = -29.4591
nova_longitude = -51.9644



# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 48
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Procurar nas colunas 'SP_CIDADE_H' e 'SP_CIDADE_P' sem diferenciar maiúsculas de minúsculas
    cidade_info_h = dados[dados['SP_CIDADE_H'].str.lower() == cidade.lower()]
    cidade_info_p = dados[dados['SP_CIDADE_P'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_H' e se sua latitude é maior que -25
    if not cidade_info_h.empty:
        lat_h = cidade_info_h['latitude_h'].values[0]
        lon_h = cidade_info_h['longitude_h'].values[0]
        
        if lat_h > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_h['SP_CIDADE_H'].values[0], lat_h, lon_h))

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_P' e se sua latitude é maior que -25
    if not cidade_info_p.empty:
        lat_p = cidade_info_p['latitude_p'].values[0]
        lon_p = cidade_info_p['longitude_p'].values[0]
        
        if lat_p > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_p['SP_CIDADE_P'].values[0], lat_p, lon_p))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 49
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SOLEDADE"

# Novos valores de latitude e longitude
nova_latitude = -28.8306
nova_longitude = -52.5131


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 50
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "CACHOEIRINHA"

# Novos valores de latitude e longitude
nova_latitude = -29.9472
nova_longitude = -51.1016


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 51
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "ALVORADA"

# Novos valores de latitude e longitude
nova_latitude = -29.9914
nova_longitude = -51.0809


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 52
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SOBRADINHO"

# Novos valores de latitude e longitude
nova_latitude = -29.4194
nova_longitude = -53.0326


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 53
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "TAPEJARA"

# Novos valores de latitude e longitude
nova_latitude = -28.0652
nova_longitude = -52.0097


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 54
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "CRUZEIRO DO SUL"

# Novos valores de latitude e longitude
nova_latitude = -29.5148
nova_longitude = -51.9928


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 55
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Lista de cidades que você forneceu
cidades_procuradas = [
    "SARANDI", "LAJEADO", "PLANALTO", "MARAU", "SOLEDADE",
    "CACHOEIRINHA", "ALVORADA", "SÃO GABRIEL", "SOBRADINHO",
    "SANTA MARIA", "SÃO FRANCISCO DE PAULA", "VERA CRUZ",
    "TAPEJARA", "TRIUNFO", "HUMAITÁ", "CRUZEIRO DO SUL",
    "BOM JESUS", "CAIÇARA"
]

# Criar uma lista para armazenar as informações encontradas
cidades_info = []

# Iterar sobre as cidades procuradas
for cidade in cidades_procuradas:
    # Procurar nas colunas 'SP_CIDADE_H' e 'SP_CIDADE_P' sem diferenciar maiúsculas de minúsculas
    cidade_info_h = dados[dados['SP_CIDADE_H'].str.lower() == cidade.lower()]
    cidade_info_p = dados[dados['SP_CIDADE_P'].str.lower() == cidade.lower()]

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_H' e se sua latitude é maior que -25
    if not cidade_info_h.empty:
        lat_h = cidade_info_h['latitude_h'].values[0]
        lon_h = cidade_info_h['longitude_h'].values[0]
        
        if lat_h > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_h['SP_CIDADE_H'].values[0], lat_h, lon_h))

    # Verificar se a cidade foi encontrada em 'SP_CIDADE_P' e se sua latitude é maior que -25
    if not cidade_info_p.empty:
        lat_p = cidade_info_p['latitude_p'].values[0]
        lon_p = cidade_info_p['longitude_p'].values[0]
        
        if lat_p > -25:  # Verifica se a latitude é maior que -25
            cidades_info.append((cidade_info_p['SP_CIDADE_P'].values[0], lat_p, lon_p))

# Exibir os resultados
print("Cidades com latitude maior que -25:")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 56
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
    # Verificar 'SP_CIDADE_H', 'latitude_h', 'longitude_h'
    if row['latitude_h'] > -25:
        cidades_info.add((row['SP_CIDADE_H'], row['latitude_h'], row['longitude_h']))

   


# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 57
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
 
    # Verificar 'SP_CIDADE_P', 'latitude_p', 'longitude_p'
    if row['latitude_p'] > -25:
        cidades_info.add((row['SP_CIDADE_P'], row['latitude_p'], row['longitude_p']))



# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 58
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SÃO GABRIEL"

# Novos valores de latitude e longitude
nova_latitude = -30.3337
nova_longitude = -54.3217


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 59
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "HUMAITÁ"

# Novos valores de latitude e longitude
nova_latitude = -27.5691
nova_longitude = -53.9695


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 60
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "BOM JESUS"

# Novos valores de latitude e longitude
nova_latitude = -28.6697
nova_longitude = -50.4295


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 61
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SANTA MARIA"

# Novos valores de latitude e longitude
nova_latitude = -29.6868
nova_longitude = -53.8149


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 62
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SÃO FRANCISCO DE PAULA"

# Novos valores de latitude e longitude
nova_latitude = -29.4404
nova_longitude = -50.5828


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 63
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "TRIUNFO"

# Novos valores de latitude e longitude
nova_latitude = -29.9291
nova_longitude = -51.7075


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 64
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "BOM JESUS"

# Novos valores de latitude e longitude
nova_latitude = -28.6697
nova_longitude = -50.4295


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 65
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "CAIÇARA"

# Novos valores de latitude e longitude
nova_latitude = -27.2791
nova_longitude = -53.4257


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 66
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "MARAU"

# Novos valores de latitude e longitude
nova_latitude = -28.4498
nova_longitude = -52.1986


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 67
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
    # Verificar 'SP_CIDADE_H', 'latitude_h', 'longitude_h'
    if row['latitude_h'] > -25:
        cidades_info.add((row['SP_CIDADE_H'], row['latitude_h'], row['longitude_h']))

   


# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 68
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
 
    # Verificar 'SP_CIDADE_P', 'latitude_p', 'longitude_p'
    if row['latitude_p'] > -25:
        cidades_info.add((row['SP_CIDADE_P'], row['latitude_p'], row['longitude_p']))



# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 69
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "ALTO ALEGRE"

# Novos valores de latitude e longitude
nova_latitude = -28.7769
nova_longitude = -52.9893


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 70
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "COLINAS"

# Novos valores de latitude e longitude
nova_latitude = -29.3948
nova_longitude = -51.8556


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 71
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "TAVARES"

# Novos valores de latitude e longitude
nova_latitude = -31.2843
nova_longitude = -51.0880


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 72
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "INDEPENDÊNCIA"

# Novos valores de latitude e longitude
nova_latitude = -27.8354
nova_longitude = -54.1886


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 73
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "COLORADO"

# Novos valores de latitude e longitude
nova_latitude = -28.5258
nova_longitude = -52.9928


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 74
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "NOVA SANTA RITA"

# Novos valores de latitude e longitude
nova_latitude = -29.8525
nova_longitude = -51.2837


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 75
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "JACUTINGA"

# Novos valores de latitude e longitude
nova_latitude = -27.7291
nova_longitude = -52.5372


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 76
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "CENTENÁRIO"

# Novos valores de latitude e longitude
nova_latitude = -27.7615
nova_longitude = -51.9984


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 77
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
 
    # Verificar 'SP_CIDADE_P', 'latitude_p', 'longitude_p'
    if row['latitude_p'] > -25:
        cidades_info.add((row['SP_CIDADE_P'], row['latitude_p'], row['longitude_p']))



# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 78
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um conjunto para armazenar as informações únicas
cidades_info = set()

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
    # Verificar 'SP_CIDADE_H', 'latitude_h', 'longitude_h'
    if row['latitude_h'] > -25:
        cidades_info.add((row['SP_CIDADE_H'], row['latitude_h'], row['longitude_h']))

   


# Exibir os resultados
print("Cidades com latitude maior que -25 (únicas):")
for cidade, lat, lon in cidades_info:
    print(f"Nome: {cidade}, Latitude: {lat}, Longitude: {lon}")

# Cell 79
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Converter colunas de latitude e longitude para numérico, forçando erros a NaN
dados['latitude_h'] = pd.to_numeric(dados['latitude_h'], errors='coerce')
dados['longitude_h'] = pd.to_numeric(dados['longitude_h'], errors='coerce')
dados['latitude_p'] = pd.to_numeric(dados['latitude_p'], errors='coerce')
dados['longitude_p'] = pd.to_numeric(dados['longitude_p'], errors='coerce')

# Verificar se a coluna 'latitude_p_ext' existe e converter se necessário
if 'latitude_p_ext' in dados.columns:
    dados['latitude_p_ext'] = pd.to_numeric(dados['latitude_p_ext'], errors='coerce')
    dados['longitude_p_ext'] = pd.to_numeric(dados['longitude_p_ext'], errors='coerce')

# Inicializar variáveis para armazenar a cidade com a maior longitude
maior_longitude = float('-inf')  # Menor infinito
cidade_com_maior_longitude = None
latitude_maior = None

# Verificar todas as colunas de latitude e suas respectivas longitudes e cidades
for index, row in dados.iterrows():
    # Verificar 'SP_CIDADE_H', 'latitude_h', 'longitude_h'
    if row['latitude_h'] > -25 and row['longitude_h'] > maior_longitude:
        maior_longitude = row['longitude_h']
        cidade_com_maior_longitude = row['SP_CIDADE_H']
        latitude_maior = row['latitude_h']

    # Verificar 'SP_CIDADE_P', 'latitude_p', 'longitude_p'
    if row['latitude_p'] > -25 and row['longitude_p'] > maior_longitude:
        maior_longitude = row['longitude_p']
        cidade_com_maior_longitude = row['SP_CIDADE_P']
        latitude_maior = row['latitude_p']

    # Verificar 'SP_CIDADE_P_EXT', 'latitude_p_ext', 'longitude_p_ext' se houver
    if 'latitude_p_ext' in dados.columns and row['latitude_p_ext'] > -25 and row['longitude_p_ext'] > maior_longitude:
        maior_longitude = row['longitude_p_ext']
        cidade_com_maior_longitude = row['SP_CIDADE_P_EXT']
        latitude_maior = row['latitude_p_ext']

# Exibir a cidade com a maior longitude
if cidade_com_maior_longitude:
    print(f"A cidade com a maior longitude é: {cidade_com_maior_longitude}, Longitude: {maior_longitude}, Latitude: {latitude_maior}")
else:
    print("Nenhuma cidade com latitude maior que -25 foi encontrada.")

# Cell 80
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SOLEDADE"

# Novos valores de latitude e longitude
nova_latitude = -28.8306
nova_longitude = -52.5131


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 81
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar uma lista para armazenar as cidades com longitude maior que -49
cidades_longitude_maior_49 = []

# Iterar sobre as linhas do DataFrame para encontrar cidades com longitude maior que -49
for index, row in dados.iterrows():
    if row['longitude_h'] > -49:  # Verifica se a longitude é maior que -49
        cidades_longitude_maior_49.append(row['SP_CIDADE_H'])

# Obter apenas os nomes únicos das cidades
cidades_longitude_maior_49_unicas = list(set(cidades_longitude_maior_49))

# Exibir os resultados
print("Cidades com longitude maior que -49:")
for cidade in cidades_longitude_maior_49_unicas:
    print(cidade)

# Cell 82
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Cidade que você quer modificar
cidade_especifica = "SÃO MARTINHO"

# Novos valores de latitude e longitude
nova_latitude = -27.7112
nova_longitude = -53.9699


# Alterar a latitude e longitude em 'latitude_h', 'longitude_h' quando 'SP_CIDADE_H' for igual à cidade específica
dados.loc[dados['SP_CIDADE_H'].str.lower() == cidade_especifica.lower(), ['latitude_h', 'longitude_h']] = [nova_latitude, nova_longitude]

# Alterar a latitude e longitude em 'latitude_p', 'longitude_p' quando 'SP_CIDADE_P' for igual à cidade específica
dados.loc[dados['SP_CIDADE_P'].str.lower() == cidade_especifica.lower(), ['latitude_p', 'longitude_p']] = [nova_latitude, nova_longitude]

# Cell 83
import pandas as pd

# Supondo que o DataFrame 'dados' já está carregado

# Criar um arquivo CSV chamado 'dados_RS.csv'
dados.to_csv('dados_RS.csv', index=False)

print("Arquivo 'dados_RS.csv' criado com sucesso!")

# Cell 84


# Cell 85


# Cell 86


# Cell 87


