import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Importação adicionada

import os
import pyreaddbc
from pysus.online_data import SIH
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

#grafico bouble
from shapely.geometry import Point 
import geopandas as gpd



# Título do aplicativo
st.title("Análise de Dados do SUS (SIH)")

# Criando abas
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Baixar Dados", "Grupos mapa", "TreeMap", "Bubble map", "Mapas de fluxo", "procedimentos", "Hospitais"])

# Conteúdo da primeira aba
with tab1:
    st.header("Dashboard de Análise de Dados do SUS (SIH)")
    
    # Dicionário com os códigos das cidades do RS
    cidade_codigos = {
        "ACEGUÁ": "430003", "AGUDO": "430010", "AJURICABA": "430020", "ALECRIM": "430030", "ALEGRETE": "430040",
        "ALPESTRE": "430050", "ALVORADA": "430060", "AMETISTA DO SUL": "430064", "ANTA GORDA": "430070", "ANTÔNIO PRADO": "430080",
        "ARATIBA": "430090", "ARROIO DO MEIO": "430100", "ARROIO DO TIGRE": "430120", "ARROIO GRANDE": "430130", "ARVOREZINHA": "430140",
        "AUGUSTO PESTANA": "430150", "BAGÉ": "430160", "BENTO GONÇALVES": "430210", "BOA VISTA DO BURICÁ": "430220", "BOM JESUS": "430230",
        "BOM PRINCÍPIO": "430235", "BOM RETIRO DO SUL": "430240", "BOQUEIRÃO DO LEÃO": "430245", "CACEQUI": "430290", "CAÇAPAVA DO SUL": "430280",
        "CACHOEIRA DO SUL": "430300", "CACHOEIRINHA": "430310", "CAIBATÉ": "430330", "CAIÇARA": "430340", "CAMAQUÃ": "430350",
        "CAMBARÁ DO SUL": "430360", "CAMPINA DAS MISSÕES": "430370", "CAMPINAS DO SUL": "430380", "CAMPO BOM": "430390", "CAMPO NOVO": "430400",
        "CANDELÁRIA": "430420", "CANDIDO GODÓI": "430430", "CÂNDIDO GODÓI": "430430", "CANELA": "430440", "CANGUÇU": "430450",
        "CANOAS": "430460", "CAPÃO DA CANOA": "430463", "CARAZINHO": "430470", "CARLOS BARBOSA": "430480", "CASCA": "430490",
        "CAXIAS DO SUL": "430510", "CERRO LARGO": "430520", "CHAPADA": "430530", "CHARQUEADAS": "430535", "CHIAPETTA": "430540",
        "CONSTANTINA": "430580", "CONDOR": "430570", "CORONEL BICACO": "430590", "CRISSIUMAL": "430600", "CRUZ ALTA": "430610",
        "CRUZEIRO DO SUL": "430620", "DAVID CANABARRO": "430630", "DOIS IRMÃOS": "430640", "DOIS LAJEADOS": "430645", "DOM FELICIANO": "430650",
        "DOM PEDRITO": "430660", "ENCANTADO": "430680", "ENCRUZILHADA DO SUL": "430690", "ERECHIM": "430700", "ESPUMOSO": "430750",
        "ESTÂNCIA VELHA": "430760", "ESTEIO": "430770", "ESTRELA": "430780", "FARROUPILHA": "430790", "FAXINAL DO SOTURNO": "430800",
        "FELIZ": "430810", "FLORES DA CUNHA": "430820", "FORMIGUEIRO": "430840", "FREDERICO WESTPHALEN": "430850", "GARIBALDI": "430860",
        "GAURAMA": "430870", "GETÚLIO VARGAS": "430890", "GIRUÁ": "430900", "GRAMADO": "430910", "GRAVATAÍ": "430920",
        "GUABIJU": "430925", "GUAÍBA": "430930", "GUAPORÉ": "430940", "GUARANI DAS MISSÕES": "430950", "HERVAL": "430710",
        "HORIZONTINA": "430960", "HUMAITÁ": "430970", "IGREJINHA": "431010", "ILÓPOLIS": "431030", "IRAÍ": "431050",
        "ITAQUI": "431060", "IVORÁ": "431075", "IVOTI": "431080", "JABOTICABA": "431085", "JAGUARÃO": "431100",
        "JAGUARI": "431110", "JAQUIRANA": "431112", "JÚLIO DE CASTILHOS": "431120", "LAGOA VERMELHA": "431130", "LAJEADO": "431140",
        "LAVRAS DO SUL": "431150", "MARAU": "431180", "MARCELINO RAMOS": "431190", "MARQUES DE SOUZA": "431205", "MATA": "431210",
        "MAXIMILIANO DE ALMEIDA": "431220", "MONTENEGRO": "431240", "MOSTARDAS": "431250", "MUÇUM": "431260", "NÃO-ME-TOQUE": "431265",
        "NONOAI": "431270", "NOVA BASSANO": "431290", "NOVA BRÉSCIA": "431300", "NOVA PALMA": "431310", "NOVA PETRÓPOLIS": "431320",
        "NOVA PRATA": "431330", "NOVO HAMBURGO": "431340", "OSÓRIO": "431350", "PAIM FILHO": "431360", "PALMARES DO SUL": "431365",
        "PALMEIRA DAS MISSÕES": "431370", "PALMITINHO": "431380", "PANAMBI": "431390", "PARAÍ": "431400", "PARAÍSO DO SUL": "431402",
        "PAROBÉ": "431405", "PASSO FUNDO": "431410", "PEDRO OSÓRIO": "431420", "PEJUÇARA": "431430", "PELOTAS": "431440",
        "PINHAL GRANDE": "431447", "PINHEIRO MACHADO": "431450", "PIRATINI": "431460", "PLANALTO": "431470", "PORTÃO": "431480",
        "PORTO ALEGRE": "431490", "PORTO LUCENA": "431500", "PORTO XAVIER": "431510", "PROGRESSO": "431515", "PUTINGA": "431520",
        "QUARAÍ": "431530", "QUINZE DE NOVEMBRO": "431535", "RESTINGA SECA": "431550", "RIO GRANDE": "431560", "RIO PARDOS": "431570",
        "RIOZINHO": "431575", "ROCA SALES": "431580", "RODEIO BONITO": "431590", "ROLANTE": "431600", "RONDA ALTA": "431610",
        "RONDINHA": "431620", "ROQUE GONZALES": "431630", "ROSÁRIO DO SUL": "431640", "SALDANHA MARINHO": "431643", "SALTO DO JACUÍ": "431645",
        "SALVADOR DO SUL": "431650", "SANANDUVA": "431660", "SANTA BÁRBARA DO SUL": "431670", "SANTA CRUZ DO SUL": "431680", "SANTA MARIA": "431690",
        "SANTA ROSA": "431720", "SANTA VITÓRIA DO PALMAR": "431730", "SANT'ANA DO LIVRAMENTO": "431710", "SANTIAGO": "431740", "SANTO ÂNGELO": "431750",
        "SANTO ANTÔNIO DA PATRULHA": "431760", "SANTO AUGUSTO": "431780", "SANTO CRISTO": "431790", "SÃO BORJA": "431800", "SÃO FRANCISCO DE ASSIS": "431810",
        "SÃO FRANCISCO DE PAULA": "431820", "SÃO GABRIEL": "431830", "SÃO JERÔNIMO": "431840", "SÃO JOÃO DO POLÊSINE": "431843", "SÃO JOSÉ DO NORTE": "431850",
        "SÃO JOSÉ DO OURO": "431860", "SÃO LEOPOLDO": "431870", "SÃO LOURENÇO DO SUL": "431880", "SÃO LUIZ GONZAGA": "431890", "SÃO MARCOS": "431900",
        "SÃO MARTINHO": "431910", "SÃO MIGUEL DAS MISSÕES": "431915", "SÃO PAULO DAS MISSÕES": "431930", "SÃO PEDRO DO SUL": "431940", "SÃO SEBASTIÃO DO CAÍ": "431950",
        "SÃO SEPÉ": "431960", "SÃO VICENTE DO SUL": "431980", "SAPIRANGA": "431990", "SAPUCAIA DO SUL": "432000", "SEBERI": "432020",
        "SEGREDO": "432026", "SELBACH": "432030", "SERAFINA CORRÊA": "432040", "SERTÃO": "432050", "SEVERIANO DE ALMEIDA": "432060",
        "SINIMBU": "432067", "SOBRADINHO": "432070", "SOLEDADE": "432080", "TAPEJARA": "432100", "TAPERA": "432100",
        "TAQUARA": "432120", "TAQUARI": "432130", "TEUTÔNIA": "432145", "TORRES": "432150", "TRAMANDAÍ": "432160",
        "TRÊS COROAS": "432170", "TRÊS DE MAIO": "432180", "TRÊS PASSOS": "432190", "TRINDADE DO SUL": "432195", "TRIUNFO": "432200",
        "TUCUNDUVA": "432210", "TUPANCIRETÃ": "432220", "TUPARENDI": "432230", "URUGUAIANA": "432240", "VACARIA": "432250",
        "VALE DO SOL": "432253", "VENÂNCIO AIRES": "432260", "VERA CRUZ": "432270", "VERANÓPOLIS": "432280", "VIADUTOS": "432290",
        "VIAMÃO": "432300"
    }
    
    # Função para processar os dados do SIH (com cache)
    @st.cache_data
    def process_sih_data(cidade, ano, cidade_codigos):
        try:
            sih = SIH.SIH()
            sih.load()
            files = sih.get_files("SP", uf="RS", year=ano)
            
            if not files:
                st.error("Nenhum arquivo encontrado para o ano selecionado.")
                return None
            
            parquets = sih.download(files)
            
            if not parquets:
                st.error("Nenhum arquivo parquet foi baixado.")
                return None
            
            cidade_codigo = cidade_codigos[cidade]
            filtered_dfs = []
            
            for parquet in parquets:
                df = parquet.to_dataframe()
                df_filtered = df[df["SP_M_HOSP"] == cidade_codigo]
                if not df_filtered.empty:
                    filtered_dfs.append(df_filtered)
                del df
            
            if not filtered_dfs:
                st.warning(f"Não foram encontrados dados para {cidade} no ano {ano}")
                return None
                
            final_data = pd.concat(filtered_dfs, ignore_index=True)
            return final_data
            
        except Exception as e:
            st.error(f"Erro ao processar os dados: {str(e)}")
            return None
    
    # Interface principal do app
    def main():
        st.markdown("""
        Este dashboard permite analisar dados do Sistema de Informações Hospitalares (SIH) do SUS.
        Selecione uma cidade e um ano para visualizar os dados.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            cidade = st.selectbox("Escolha a cidade:", list(cidade_codigos.keys()))
        with col2:
            ano = st.selectbox("Escolha o ano:", list(range(2008, 2025)))
        
        tab1, tab2 = st.tabs(["Download dos Dados", "Análise dos Dados"])
        
        with tab1:
            if st.button("Baixar e Processar Dados"):
                with st.spinner(f"Baixando e processando dados para {cidade} ({ano})..."):
                    df = process_sih_data(cidade, ano, cidade_codigos)
                    
                    if df is not None:
                        df.to_csv("dados_filtrados.csv", index=False)
                        st.success(f"Dados processados com sucesso! Arquivo salvo como 'dados_filtrados.csv'")
                        st.subheader("Visão Geral dos Dados")
                        st.write(f"Total de registros: {len(df)}")
                        st.subheader("Amostra dos Dados")
                        st.dataframe(df.head())
                        st.session_state['dados_baixados'] = True
        
        with tab2:
            if 'dados_baixados' not in st.session_state:
                st.warning("⚠️ Por favor, primeiro baixe os dados na aba 'Download dos Dados'")
            else:
                st.success("✅ Dados baixados e prontos para análise")
                if st.button("Rodar Análise"):
                    try:
                        with st.spinner("Executando notebook de análise..."):
                            execute_notebook("Tentativa_GUI.ipynb")
                            st.success("Notebook executado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao executar o notebook: {str(e)}")
    
    if __name__ == "__main__":
        main()
    

############################################################################

# Conteúdo da segunda aba
with tab2:
    st.header("Gráfico grupos")
    
    dados = pd.read_csv('pacote_light_sem_NAIH_duplo.csv')

    # Agrupar dados para contar internações por cidade e hospital
    point_counts = dados.groupby(['SP_CIDADE_P', 'NO_HOSPITAL', 'SP_CIDADE_H', 'LAT_ESPECIFICA', 'LONG_ESPECIFICA', 'SP_PROCREA']).size().reset_index(name='counts')
    
    # Título da aplicação
    st.title("Hospitais utilizados por pessoas de uma cidade")
    
    # Dropdown para selecionar o grupo
    grupo_selecionado = st.selectbox(
        "Selecione um grupo (1 a 8):",
        options=[str(i) for i in range(1, 9)],
        index=None,  # Nenhum valor selecionado por padrão
        placeholder="Selecione um número de 1 a 8"
    )
    
    # Filtrar pelo grupo selecionado
    if grupo_selecionado:
        dados_filtrados = point_counts[point_counts['SP_PROCREA'].astype(str).str.startswith(grupo_selecionado)]
    else:
        dados_filtrados = point_counts
    
    # Contagem de pessoas por hospital
    hospitais_contagem = dados_filtrados.groupby(['NO_HOSPITAL', 'SP_CIDADE_H', 'LAT_ESPECIFICA', 'LONG_ESPECIFICA'])['counts'].sum().reset_index()
    
    # Criar o gráfico de dispersão no mapa
    fig = px.scatter_mapbox(
        hospitais_contagem,
        lat='LAT_ESPECIFICA',
        lon='LONG_ESPECIFICA',
        size='counts',
        color='counts',
        hover_name='NO_HOSPITAL',  # Nome do hospital
        hover_data={'SP_CIDADE_H': True, 'counts': True},  # Exibir cidade do hospital e quantidade
        mapbox_style='carto-positron',
        zoom=6,
        center={"lat": -30.0318, "lon": -51.2065}
    )
    
    # Atualizar layout do gráfico
    fig.update_layout(
        width=900,
        height=600,
        title=f"Hospitais associados ao Grupo {grupo_selecionado}" if grupo_selecionado else "Hospitais no mapa"
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)



###########################################################
# Conteúdo da terceira aba
with tab3:
    st.header("TreeMap")


    # Carregar os dados do CSV
    dados = pd.read_csv('pacote_light_sem_NAIH_duplo.csv')
    
    # Configurar a lista de grupos e subgrupos
    grupo_subgrupo = {
        "01": {"01": "Ações coletivas/individuais em saúde", "02": "Vigilância em saúde"},
        "02": {
            "01": "Coleta de material",
            "02": "Diagnóstico em laboratório clínico",
            "03": "Diagnóstico por anatomia patológica e citopatologia",
            "04": "Diagnóstico por radiologia",
            "05": "Diagnóstico por ultrassonografia",
            "06": "Diagnóstico por tomografia",
            "07": "Diagnóstico por ressonância magnética",
            "08": "Diagnóstico por medicina nuclear in vivo",
            "09": "Diagnóstico por endoscopia",
            "10": "Diagnóstico por radiologia intervencionista",
            "11": "Métodos diagnósticos em especialidades",
            "12": "Diagnóstico e procedimentos especiais em hemoterapia",
            "13": "Diagnóstico em vigilância epidemiológica e ambiental",
            "14": "Diagnóstico por teste rápido"
        },
        "03": {
            "01": "Consultas / Atendimentos / Acompanhamentos",
            "02": "Fisioterapia",
            "03": "Tratamentos clínicos (outras especialidades)",
            "04": "Tratamento em oncologia",
            "05": "Tratamento em nefrologia",
            "06": "Hemoterapia",
            "07": "Tratamentos odontológicos",
            "08": "Tratamento de lesões, envenenamentos e outros, decorrentes de causas externas",
            "09": "Terapias especializadas",
            "10": "Parto e nascimento"
        }
        # Adicione os demais grupos e subgrupos aqui...
    }
    
    # Título da aplicação
    st.title("Treemap de Grupos e Subgrupos com Contagem")
    
    # Criar o treemap para grupos e subgrupos com contagem de ocorrências
    dados["grupo"] = dados["SP_PROCREA"].astype(str).str[0]
    dados["subgrupo"] = dados["SP_PROCREA"].astype(str).str[1:3]
    
    contagem = dados.groupby(["grupo", "subgrupo"]).size().reset_index(name="ocorrencias")
    
    contagem["grupo_nome"] = contagem["grupo"].map(lambda x: f"Grupo {x}")
    
    def obter_nome_subgrupo(row):
        grupo = row["grupo"]
        subgrupo = row["subgrupo"]
        if grupo in grupo_subgrupo and subgrupo in grupo_subgrupo[grupo]:
            return f"Subgrupo {subgrupo} - {grupo_subgrupo[grupo][subgrupo]}"
        else:
            return f"Subgrupo {subgrupo} "
    
    contagem["subgrupo_nome"] = contagem.apply(obter_nome_subgrupo, axis=1)
    
    # Criar o gráfico treemap com Plotly
    treemap_fig = px.treemap(
        contagem,
        path=["grupo_nome", "subgrupo_nome"],
        values="ocorrencias",
        color="grupo",  # Define cores baseadas no grupo
        color_discrete_sequence=px.colors.qualitative.Set2,  # Escolhe uma paleta de cores
        title="Distribuição de Grupos e Subgrupos com Contagem",
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(treemap_fig)

with tab4:

    
    # Carregar o arquivo CSV 'dados_RS_nomes.csv'
    try:
        dados = pd.read_csv('dados_RS_nomes.csv')
    except FileNotFoundError:
        st.error("Arquivo 'dados_RS_nomes.csv' não encontrado.")
        st.stop()  # Interrompe a execução do código se o arquivo não for encontrado
    
    # Verificar se as colunas necessárias existem no DataFrame
    if 'longitude_h' not in dados.columns or 'latitude_h' not in dados.columns:
        st.error("As colunas 'longitude_h' e 'latitude_h' não foram encontradas no arquivo CSV.")
        st.stop()  # Interrompe a execução se as colunas não existirem
    
    # Criar geometrias do tipo Point usando latitude e longitude
    geometry = [Point(xy) for xy in zip(dados['longitude_h'], dados['latitude_h'])]
    gdf = gpd.GeoDataFrame(dados, geometry=geometry, crs="EPSG:4326")
    
    # Contar o número de internações em cada ponto (latitude, longitude)
    gdf['coord'] = gdf['geometry'].apply(lambda x: (x.x, x.y))  # Cria uma coluna com as coordenadas
    point_counts = gdf.groupby('coord').size().reset_index(name='counts')  # Conta o número de pontos por coordenada
    
    # Adicionar nomes dos hospitais ao DataFrame de contagem
    point_counts['nome_h'] = point_counts['coord'].apply(
        lambda x: gdf.loc[(gdf['longitude_h'] == x[0]) & (gdf['latitude_h'] == x[1]), 'nome_h'].values[0]
    )
    
    # Criar um DataFrame para os resultados
    point_counts['longitude'] = point_counts['coord'].apply(lambda x: x[0])
    point_counts['latitude'] = point_counts['coord'].apply(lambda x: x[1])
    
    # Excluir coordenadas do ponto que não deve receber a seta
    ponto_excluir = (0, 0)
    point_counts = point_counts[
        ~point_counts['coord'].apply(lambda x: (x[0], x[1]) == ponto_excluir)
    ]
    
    # Configuração da aplicação Streamlit
    st.title("Internações por Localização de Hospital")
    
    # Adicionar controles para limites de bolhas
    limite_max = st.number_input(
        "Limite máximo para bolhas:",
        min_value=1,
        value=99999999  # Valor inicial do limite máximo
    )
    limite_min = st.number_input(
        "Limite mínimo para bolhas:",
        min_value=1,
        value=1  # Valor inicial do limite mínimo
    )
    
    # Filtrar os dados conforme os limites informados
    dados_filtrados = point_counts[
        (point_counts['counts'] <= limite_max) & 
        (point_counts['counts'] >= limite_min)
    ]
    
    # Criar o gráfico de dispersão no mapa
    fig = px.scatter_mapbox(
        dados_filtrados,
        lat='latitude',
        lon='longitude',
        size='counts',
        color='counts',
        hover_name=dados_filtrados['nome_h'],  # Exibir o nome do hospital no hover
        mapbox_style='carto-positron',
        zoom=6,
        center={"lat": -30.0318, "lon": -51.2065}
    )
    
    # Ajustar o layout do gráfico
    fig.update_layout(
        width=900,
        height=600,
        title="Internações por Localização de Hospital (Limites de bolhas aplicados)"
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

with tab5:

    # Título da aplicação
    st.title("Comparação de Cidades")
    
    # Carregar o arquivo CSV
    dados = pd.read_csv('pacote_light_sem_NAIH_duplo.csv')
    
    # Contar a quantidade de vezes que cada cidade aparece em nome_p
    contagem_p = dados['SP_CIDADE_P'].value_counts().reset_index()
    contagem_p.columns = ['Cidade', 'Contagem_nome_p']
    
    # Contar a quantidade de vezes que cada cidade aparece em nome_h
    contagem_h = dados['SP_CIDADE_H'].value_counts().reset_index()
    contagem_h.columns = ['Cidade', 'Contagem_nome_h']
    
    # Unir as duas contagens
    contagem_total = pd.merge(contagem_p, contagem_h, on='Cidade', how='outer').fillna(0)
    
    # Transformar contagens em inteiros
    contagem_total['Contagem_nome_p'] = contagem_total['Contagem_nome_p'].astype(int)
    contagem_total['Contagem_nome_h'] = contagem_total['Contagem_nome_h'].astype(int)
    
    # Criar lista de cidades únicas em ordem alfabética
    cidades_unicas = sorted(contagem_total['Cidade'].unique().tolist())
    
    # Dropdown para selecionar cidades
    cidades_selecionadas = st.multiselect(
        "Selecione as cidades:",
        options=cidades_unicas,
        default=cidades_unicas[:5]  # Seleciona as primeiras 5 cidades por padrão
    )
    
    # Verificar se há cidades selecionadas
    if not cidades_selecionadas:
        st.warning("Selecione pelo menos uma cidade para visualizar o gráfico.")
    else:
        # Filtrar as contagens para as cidades selecionadas
        dados_filtrados = contagem_total[contagem_total['Cidade'].isin(cidades_selecionadas)]
    
        # Criar o gráfico de barras
        fig = px.bar(
            dados_filtrados,
            x='Cidade',
            y=['Contagem_nome_p', 'Contagem_nome_h'],
            title='Quantidade de Aparições de Cidades em nome_p e nome_h',
            labels={'value': 'Contagem', 'variable': 'Tipo de Nome'},
            barmode='group'
        )
    
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

with tab6:
    
    
    # Dicionário para mapear os grupos e nomes
    procrea_grupos = {
        "1": "AÇÕES DE PROMOÇÃO E PREVENÇÃO EM SAÚDE",
        "2": "PROCEDIMENTOS COM FINALIDADE DIAGNÓSTICA",
        "3": "PROCEDIMENTOS CLÍNICOS",
        "4": "PROCEDIMENTOS CIRÚRGICOS",
        "5": "TRANSPLANTES DE ÓRGÃOS, TECIDOS e CÉLULAS",
        "6": "MEDICAMENTOS",
        "7": "ÓRTESES, PRÓTESES E MATERIAIS ESPECIAIS",
        "8": "AÇÕES COMPLEMENTARES DA ATENÇÃO À SAÚDE",
    }
    
    # Carregar o arquivo CSV
    @st.cache_data  # Cache para evitar recarregar os dados a cada interação
    def carregar_dados():
        return pd.read_csv('pacote_light_sem_NAIH_duplo.csv')
    
    dados = carregar_dados()
    
    # Extrair o grupo inicial de SP_PROCREA
    dados['GRUPO_SP_PROCREA'] = dados['SP_PROCREA'].astype(str).str[0]
    
    # Título da aplicação
    st.title("Filtrar Procedimentos por Grupo SP_PROCREA")
    
    # Dropdown para selecionar o grupo
    grupo_selecionado = st.selectbox(
        "Selecione um grupo:",
        options=[f"{grupo} - {nome}" for grupo, nome in procrea_grupos.items()],
        index=None,  # Nenhum valor selecionado por padrão
        placeholder="Selecione um grupo"
    )
    
    # Verificar se um grupo foi selecionado
    if grupo_selecionado:
        # Extrair o código do grupo selecionado
        grupo_codigo = grupo_selecionado.split(" - ")[0]
    
        # Filtrar os dados pelo grupo selecionado
        dados_filtrados = dados[dados['GRUPO_SP_PROCREA'] == grupo_codigo]
    
        # Contar procedimentos por hospital
        contagem_procedimentos = dados_filtrados.groupby(['NO_HOSPITAL', 'SP_CIDADE_H']).size().reset_index(name='counts')
    
        # Criar gráfico de barras
        fig = px.bar(
            contagem_procedimentos,
            x='NO_HOSPITAL',
            y='counts',
            color='SP_CIDADE_H',
            title=f"Procedimentos do Grupo {grupo_codigo} - {procrea_grupos[grupo_codigo]}",
            labels={"NO_HOSPITAL": "Hospital", "counts": "Quantidade", "SP_CIDADE_H": "Cidade do Hospital"}
        )
    
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    
        # Exibir lista de hospitais e contagem
        st.subheader(f"Detalhes dos Procedimentos do Grupo {grupo_codigo} - {procrea_grupos[grupo_codigo]}:")
        for _, row in contagem_procedimentos.iterrows():
            hospital = row['NO_HOSPITAL']
            cidade = row['SP_CIDADE_H']
            quantidade = row['counts']
            st.write(f"{hospital} (Cidade: {cidade}): {quantidade} procedimentos")
    else:
        st.warning("Por favor, selecione um grupo para visualizar os dados.")

with tab7:
      
    # Função para carregar os dados (com cache)
    @st.cache_data
    def carregar_dados():
        return pd.read_csv('pacote_light_sem_NAIH_duplo.csv')
    
    # Carregar os dados
    dados = carregar_dados()
    
    # Contar o número de internações por hospital
    dados['coord'] = list(zip(dados['LONG_ESPECIFICA'], dados['LAT_ESPECIFICA']))
    point_counts = dados.groupby(['NO_HOSPITAL', 'SP_CIDADE_H', 'coord']).size().reset_index(name='counts')
    
    # Separar as coordenadas
    point_counts['longitude'] = point_counts['coord'].apply(lambda x: x[0])
    point_counts['latitude'] = point_counts['coord'].apply(lambda x: x[1])
    
    # Título da aplicação
    st.title("Internações por Hospital")
    
    # Dropdown para selecionar o hospital
    hospital_selecionado = st.selectbox(
        "Selecione o hospital:",
        options=sorted(point_counts['NO_HOSPITAL'].unique()),
        index=None,  # Nenhum valor selecionado por padrão
        placeholder="Selecione o hospital",
        key="hospital_select"  # Chave única para evitar conflitos
    )
    
    # Inputs para limites de bolhas
    limite_max = st.number_input(
        "Limite máximo para bolhas:",
        min_value=1,
        value=99999999,  # Valor inicial do limite máximo
        key="limite_max"  # Chave única para o primeiro number_input
    )
    limite_min = st.number_input(
        "Limite mínimo para bolhas:",
        min_value=1,
        value=1,  # Valor inicial do limite mínimo
        key="limite_min"  # Chave única para o segundo number_input
    )
    
    # Botão para aplicar os limites
    if st.button("Aplicar Limites", key="botao_aplicar"):  # Chave única para o botão
        # Filtrar dados com os limites informados
        dados_filtrados = point_counts[
            (point_counts['counts'] <= limite_max) & 
            (point_counts['counts'] >= limite_min)
        ]
        
        # Filtrar pelos hospitais específicos
        if hospital_selecionado:
            dados_filtrados = dados_filtrados[dados_filtrados['NO_HOSPITAL'] == hospital_selecionado]
        
        # Modificar o hover para exibir o nome do hospital e a cidade no formato desejado
        dados_filtrados['hover_info'] = (
            dados_filtrados['NO_HOSPITAL'] + "<br>Cidade: " + dados_filtrados['SP_CIDADE_H']
        )
        
        # Criar o gráfico de dispersão no mapa
        fig = px.scatter_mapbox(
            dados_filtrados,
            lat='latitude',
            lon='longitude',
            size='counts',
            color='counts',
            hover_name='hover_info',  # Usar a coluna personalizada de hover
            mapbox_style='carto-positron',
            zoom=6,
            center={"lat": -30.0318, "lon": -51.2065}
        )
        
        fig.update_layout(
            width=900,
            height=600,
            title="Internações por Hospital (Limites de bolhas aplicados)"
        )
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

