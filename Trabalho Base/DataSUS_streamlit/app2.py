import streamlit as st
import pandas as pd
import os
import pyreaddbc
from pysus.online_data import SIH
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import geopandas as gpd
from shapely.geometry import Point
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components 

def execute_notebook(notebook_path):
    """
    Executa um notebook Jupyter de forma programática
    """
    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)
        
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        os.environ['JUPYTER_PREFER_ENV_PATH'] = '1'
        
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        return True
    except Exception as e:
        st.error(f"Erro ao executar o notebook: {str(e)}")
        st.exception(e)  # Mostra o traceback completo
        return False


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

def main():
    # Configure the page to use wide mode
    st.set_page_config(layout="wide")
    
    # Create two columns: one for the sidebar (smaller) and one for the content (larger)
    sidebar_col, content_col = st.columns([1, 5])
    
    with sidebar_col:
        # Adicionar CSS para estilizar os labels e adicionar espaço no topo
        st.markdown("""
            <style>
                .sidebar-label {
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    margin-top: 1rem;
                    color: #FFFFFF;
                }
                /* Adicionar padding no topo da sidebar */
                .sidebar .sidebar-content {
                    padding-top: 2rem !important;  /* Adiciona espaço no topo */
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Adicionar os labels estilizados antes dos selectboxes
        st.markdown('<p class="sidebar-label">Escolha a cidade:</p>', unsafe_allow_html=True)
        cidade = st.selectbox("", list(cidade_codigos.keys()), label_visibility="collapsed")
        
        st.markdown('<p class="sidebar-label">Escolha o ano:</p>', unsafe_allow_html=True)
        ano = st.selectbox("", list(range(2008, 2025)), label_visibility="collapsed")
        
        if st.button("Baixar e Processar Dados"):
            with st.spinner(f"Baixando e processando dados para {cidade} ({ano})..."):
                df = process_sih_data(cidade, ano, cidade_codigos)
                
                if df is not None:
                    df.to_csv("dados_filtrados.csv", index=False)
                    st.success(f"Dados salvos como 'dadosfiltrados.csv'")
                    st.write(f"Total de registros: {len(df)}")
                    st.subheader("Amostra dos Dados")
                    st.dataframe(df.head())
                    st.session_state['dados_baixados'] = True
        
        if 'dados_baixados' in st.session_state:
            if st.button("Executar Análise"):
                with st.spinner("Executando notebook de análise..."):
                    success = execute_notebook("Tentativa_GUI.ipynb")
                    if success:
                        st.success("Notebook executado com sucesso!")
                        st.session_state['analise_executada'] = True
                    else:
                        st.error("Falha ao executar o notebook.")
    
    # O restante do código (content_col) permanece igual
    with content_col:
        st.markdown("""
            <style>
                .main > div {
                    padding-left: 0;
                    padding-right: 0;
                }
                .block-container {
                    padding-top: 2.5rem;
                    padding-bottom: 0;
                    padding-left: 0;
                    padding-right: 0;
                }
                .main h1:first-child {
                    margin-top: 1rem;
                    margin-bottom: 2rem;
                    padding-top: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.title("Dashboard de Análise de Dados do SUS (SIH)")

        st.markdown("""
        Este dashboard permite analisar dados do Sistema de Informações Hospitalares (SIH) do SUS.
        Selecione uma cidade e um ano para começar.
        """)
        
        if 'analise_executada' in st.session_state and st.session_state['analise_executada']:
            st.subheader(f"Resultados da Análise - {cidade} ({ano})")
            
            arquivo = "analise_completa.html"
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    if html_content.strip():
                        components.html(
                            html_content,
                            height=1000,
                            width=None,
                            scrolling=True
                        )
                except Exception as e:
                    st.error(f"Erro ao renderizar '{arquivo}': {str(e)}")
            else:
                st.warning(f"Arquivo '{arquivo}' não encontrado.")
        
        elif 'dados_baixados' not in st.session_state:
            st.info("Por favor, baixe os dados na barra lateral para começar.")
        elif 'analise_executada' not in st.session_state:
            st.info("Dados baixados. Clique em 'Rodar Análise' na barra lateral para ver os gráficos.")

if __name__ == "__main__":
    main()



# def process_sih_data(cidade, ano, cidade_codigos):
#     try:
#         sih = SIH.SIH()
#         sih.load()
        
#         files = sih.get_files("SP", uf="RS", year=ano)
        
#         if not files:
#             st.error("Nenhum arquivo encontrado para o ano selecionado.")
#             return None
        
#         parquets = sih.download(files)
        
#         if not parquets:
#             st.error("Nenhum arquivo parquet foi baixado.")
#             return None
        
#         cidade_codigo = cidade_codigos[cidade]
#         filtered_dfs = []
        
#         for parquet in parquets:
#             df = parquet.to_dataframe()
#             df_filtered = df[df["SP_M_HOSP"] == cidade_codigo]
#             if not df_filtered.empty:
#                 filtered_dfs.append(df_filtered)
#             del df
        
#         if not filtered_dfs:
#             st.warning(f"Não foram encontrados dados para {cidade} no ano {ano}")
#             return None
            
#         final_data = pd.concat(filtered_dfs, ignore_index=True)
#         return final_data
        
#     except Exception as e:
#         st.error(f"Erro ao processar os dados: {str(e)}")
#         return None

# # Interface principal do app
# def main():
#     st.title("Dashboard de Análise de Dados do SUS (SIH)")
    
#     with st.sidebar:
#         st.markdown("""
#         Este dashboard permite analisar dados do Sistema de Informações Hospitalares (SIH) do SUS.
#         Selecione uma cidade e um ano para começar.
#         """)
        
#         cidade = st.selectbox("Escolha a cidade:", list(cidade_codigos.keys()))
#         ano = st.selectbox("Escolha o ano:", list(range(2008, 2025)))
        
#         if st.button("Baixar e Processar Dados"):
#             with st.spinner(f"Baixando e processando dados para {cidade} ({ano})..."):
#                 df = process_sih_data(cidade, ano, cidade_codigos)
                
#                 if df is not None:
#                     df.to_csv("dados_filtrados.csv", index=False)
#                     st.success(f"Dados salvos como 'dadosfiltrados.csv'")
#                     st.write(f"Total de registros: {len(df)}")
#                     st.subheader("Amostra dos Dados")
#                     st.dataframe(df.head())
#                     st.session_state['dados_baixados'] = True
        
#         if 'dados_baixados' in st.session_state:
#             if st.button("Rodar Análise"):
#                 with st.spinner("Executando notebook de análise..."):
#                     success = execute_notebook("Tentativa_GUI.ipynb")
#                     if success:
#                         st.success("Notebook executado com sucesso!")
#                         st.session_state['analise_executada'] = True
#                     else:
#                         st.error("Falha ao executar o notebook.")
    
#     if 'analise_executada' in st.session_state and st.session_state['analise_executada']:
#         st.subheader(f"Resultados da Análise - {cidade} ({ano})")
        
#         # Definir largura fixa para PNGs
#         image_width = 900  # Largura fixa para caber na tela
        
#         # Lista de gráficos PNG
#         grafico_arquivos = {
#             "internacoes_mes.png": "Distribuição de Internações por Mês",
#             "top_procedimentos.png": "Top 10 Procedimentos Mais Frequentes",
#             "tempo_internacao.png": "Distribuição do Tempo de Internação",
#             "heatmap_temporal.png": "Distribuição de Internações por Hora e Dia da Semana",
#             "tendencia_temporal.png": "Tendência do Valor Médio dos Procedimentos"
#         }
        
#         # Exibir gráficos PNG, 1 por linha, centralizado
#         for arquivo, titulo in grafico_arquivos.items():
#             if os.path.exists(arquivo):
#                 st.subheader(titulo)
#                 with st.container():
#                     col_left, col_center, col_right = st.columns([0.1, 0.8, 0.1])  # 80% centralizado
#                     with col_center:
#                         st.image(arquivo, caption=titulo, use_container_width=False, width=image_width)
#             else:
#                 st.warning(f"Gráfico '{arquivo}' não encontrado.")
        
#         st.markdown("---")
        
#         # Lista de gráficos HTML
#         html_files = {
#             "valores_por_procedimento.html": "Distribuição de Valores por Procedimento",
#             "internacoes_mes.html": "Internações por Mês",
#             "valores_medios.html": "Procedimentos com Maior Valor Médio",
#             "tempo_medio.html": "Tempo Médio de Internação",
#             "procedimentos_comuns.html": "Procedimentos Mais Comuns"
#         }
        
#         # Exibir gráficos HTML, 1 por linha, centralizado
#         for arquivo, titulo in html_files.items():
#             if os.path.exists(arquivo):
#                 st.subheader(titulo)
#                 try:
#                     with open(arquivo, 'r', encoding='utf-8') as f:
#                         html_content = f.read()
#                     if html_content.strip():
#                         with st.container():
#                             col_left, col_center, col_right = st.columns([0.1, 0.8, 0.1])  # 80% centralizado
#                             with col_center:
#                                 components.html(html_content, height=400, width=900)  # Tamanhos fixos ajustados
#                 except Exception as e:
#                     st.error(f"Erro ao renderizar '{arquivo}': {str(e)}")
#             else:
#                 st.warning(f"Gráfico interativo '{arquivo}' não encontrado.")
#     elif 'dados_baixados' not in st.session_state:
#         st.info("Por favor, baixe os dados na barra lateral para começar.")
#     elif 'analise_executada' not in st.session_state:
#         st.info("Dados baixados. Clique em 'Rodar Análise' na barra lateral para ver os gráficos.")

# if __name__ == "__main__":
#     main()



# VERSAO RETA
# # Função para processar os dados do SIH
# def process_sih_data(cidade, ano, cidade_codigos):
#     try:
#         sih = SIH.SIH()
#         sih.load()
        
#         files = sih.get_files("SP", uf="RS", year=ano)
        
#         if not files:
#             st.error("Nenhum arquivo encontrado para o ano selecionado.")
#             return None
        
#         parquets = sih.download(files)
        
#         if not parquets:
#             st.error("Nenhum arquivo parquet foi baixado.")
#             return None
        
#         cidade_codigo = cidade_codigos[cidade]
#         filtered_dfs = []
        
#         for parquet in parquets:
#             df = parquet.to_dataframe()
#             df_filtered = df[df["SP_M_HOSP"] == cidade_codigo]
#             if not df_filtered.empty:
#                 filtered_dfs.append(df_filtered)
#             del df
        
#         if not filtered_dfs:
#             st.warning(f"Não foram encontrados dados para {cidade} no ano {ano}")
#             return None
            
#         final_data = pd.concat(filtered_dfs, ignore_index=True)
#         return final_data
        
#     except Exception as e:
#         st.error(f"Erro ao processar os dados: {str(e)}")
#         return None

# # Interface principal do app
# def main():
#     st.title("Dashboard de Análise de Dados do SUS (SIH)")
    
#     st.markdown("""
#     Este dashboard permite analisar dados do Sistema de Informações Hospitalares (SIH) do SUS.
#     Selecione uma cidade e um ano para visualizar os dados.
#     """)
    
#     col1, col2 = st.columns(2)
#     with col1:
#         cidade = st.selectbox("Escolha a cidade:", list(cidade_codigos.keys()))
#     with col2:
#         ano = st.selectbox("Escolha o ano:", list(range(2008, 2025)))
    
#     tab1, tab2 = st.tabs(["Download dos Dados", "Análise dos Dados"])
    
#     with tab1:
#         if st.button("Baixar e Processar Dados"):
#             with st.spinner(f"Baixando e processando dados para {cidade} ({ano})..."):
#                 df = process_sih_data(cidade, ano, cidade_codigos)
                
#                 if df is not None:
#                     # Salvar como 'dados_limpos.csv' em vez de 'dados_filtrados.csv'
#                     df.to_csv("dados_limpos.csv", index=False)
#                     st.success(f"Dados processados com sucesso! Arquivo salvo como 'dados_limpos.csv'")
#                     st.subheader("Visão Geral dos Dados")
#                     st.write(f"Total de registros: {len(df)}")
#                     st.subheader("Amostra dos Dados")
#                     st.dataframe(df.head())
#                     st.session_state['dados_baixados'] = True
    
#     with tab2:
#         if 'dados_baixados' not in st.session_state:
#             st.warning("⚠️ Por favor, primeiro baixe os dados na aba 'Download dos Dados'")
#         else:
#             st.success("✅ Dados baixados e prontos para análise")
#             if st.button("Rodar Análise"):
#                 with st.spinner("Executando notebook de análise..."):
#                     success = execute_notebook("Tentativa_GUI.ipynb")
#                     if success:
#                         st.success("Notebook executado com sucesso!")
#                         st.session_state['analise_executada'] = True
#                     else:
#                         st.error("Falha ao executar o notebook.")
            
#             # Exibir gráficos após a execução do notebook
#             if 'analise_executada' in st.session_state and st.session_state['analise_executada']:
#                 st.subheader("Resultados da Análise")
                
#                 # Lista de gráficos PNG gerados pelo notebook
#                 grafico_arquivos = {
#                     "internacoes_mes.png": "Distribuição de Internações por Mês",
#                     "top_procedimentos.png": "Top 10 Procedimentos Mais Frequentes",
#                     "tempo_internacao.png": "Distribuição do Tempo de Internação",
#                     "valores_procedimentos.png": "Distribuição dos Valores dos Procedimentos",
#                     "heatmap_temporal.png": "Distribuição de Internações por Hora e Dia da Semana",
#                     "tendencia_temporal.png": "Tendência do Valor Médio dos Procedimentos ao Longo do Tempo"
#                 }
                
#                 # Exibir gráficos PNG
#                 for arquivo, titulo in grafico_arquivos.items():
#                     if os.path.exists(arquivo):
#                         st.image(arquivo, caption=titulo, use_column_width=True)
#                     else:
#                         st.warning(f"Gráfico '{arquivo}' não encontrado.")
                
#                 # Exibir gráficos interativos HTML (opcional)
#                 html_files = {
#                     "valores_por_procedimento.html": "Distribuição de Valores por Procedimento",
#                     "dashboard.html": "Dashboard Interativo de Análise de Internações"
#                 }
                
#                 for arquivo, titulo in html_files.items():
#                     if os.path.exists(arquivo):
#                         st.subheader(titulo)
#                         with open(arquivo, 'r', encoding='utf-8') as f:
#                             html_content = f.read()
#                         components.html(html_content, height=800)
#                     else:
#                         st.warning(f"Gráfico interativo '{arquivo}' não encontrado.")

# if __name__ == "__main__":
#     main()

