"""
Sistema de Consulta e Dashboard Interativo de Vendas
Autor: Nikolas Pinheiro
Data: Maio de 2026
Descrição: Aplicação web desenvolvida em Python para automação de ETL (Extração,
           Tratamento e Carga) e visualização de dados de planilhas Excel.
"""

import streamlit as st
import pandas as pd
import altair as alt
import io

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA INTERFACE WEB (STREAMLIT)
# -----------------------------------------------------------------------------
# Define as propriedades da página do navegador (Título e Layout Expandido)
st.set_page_config(
    page_title="Dashboard Inteligente de Vendas | Nikolas Pinheiro", 
    layout="wide",
    page_icon="📊"
)

st.title("📊 Sistema Inteligente de Consulta e Dashboard")
st.markdown("---")

# -----------------------------------------------------------------------------
# CAMADA DE ENGENHARIA DE DADOS / PIPELINE DE ETL
# -----------------------------------------------------------------------------
@st.cache_data
def pipeline_tratamento_dados(arquivo):
    """
    Realiza o processo de ETL automatizado:
    - Extração: Lê a planilha Excel fornecida.
    - Tratamento: Remove espaços em branco de strings, trata dados nulos
                  e padroniza formatos de data de maneira dinâmica.
    - Carga: Retorna o DataFrame tratado para a memória RAM.
    """
    # [E] - Extração dos dados brutos do Excel
    df = pd.read_excel(arquivo)
    
    # [T] - Tratamento de Dados (Data Cleaning)
    
    # 1. Limpeza de strings: Remove espaços extras invisíveis no início/fim dos textos
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    # 2. Tipagem Dinâmica de Datas: Identifica colunas temporais e aplica o formato correto
    for col in df.columns:
        if 'data' in col.lower() or 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # 3. Tratamento de Valores Ausentes (Nulos): Preenche vazios numéricos com zero
    colunas_numericas = df.select_dtypes(include=['number']).columns
    df[colunas_numericas] = df[colunas_numericas].fillna(0)
    
    return df

# -----------------------------------------------------------------------------
# FLUXO PRINCIPAL DA APLICAÇÃO
# -----------------------------------------------------------------------------
# Barra Lateral: Permite que o usuário faça o upload de QUALQUER base de dados
st.sidebar.header("📁 Upload de Arquivos")
arquivo_enviado = st.sidebar.file_uploader(
    "Arraste uma nova planilha Excel (.xlsx):", 
    type=["xlsx"]
)

# Define o arquivo de entrada: Usa o enviado ou recorre à base padrão local
arquivo_final = arquivo_enviado if arquivo_enviado is not None else "Base_Vendas_1000_Registros_BI.xlsx"

try:
    # Executa o pipeline de dados
    df_vendas = pipeline_tratamento_dados(arquivo_final)
    
    # Mapeamento dinâmico das colunas por tipo para geração de filtros automáticos
    col_texto = list(df_vendas.select_dtypes(include=['object']).columns)
    col_num = list(df_vendas.select_dtypes(include=['number']).columns)
    col_data = list(df_vendas.select_dtypes(include=['datetime64[ns]']).columns)

    # -------------------------------------------------------------------------
    # PAINEL DE FILTROS (REGRAS DE NEGÓCIO)
    # -------------------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Regras de Consulta / Filtros")
    
    df_filtrado = df_vendas.copy()
    
    # Aplicação dinâmica do Filtro 1 (Primeira coluna de texto encontrada)
    if len(col_texto) > 0:
        f1_nome = col_texto[0]
        f1_opcoes = ["Todos"] + list(df_vendas[f1_nome].unique())
        f1_escolha = st.sidebar.selectbox(f"Filtrar por {f1_nome}:", f1_opcoes)
        if f1_escolha != "Todos":
            df_filtrado = df_filtrado[df_filtrado[f1_nome] == f1_escolha]

    # Aplicação dinâmica do Filtro 2 (Segunda coluna de texto encontrada)
    if len(col_texto) > 1:
        f2_nome = col_texto[1]
        f2_opcoes = ["Todos"] + list(df_vendas[f2_nome].unique())
        f2_escolha = st.sidebar.selectbox(f"Filtrar por {f2_nome}:", f2_opcoes)
        if f2_escolha != "Todos":
            df_filtrado = df_filtrado[df_filtrado[f2_nome] == f2_escolha]

    # -------------------------------------------------------------------------
    # CAMADA DE EXPORTAÇÃO (DOWNLOAD)
    # -------------------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Exportação de Dados")
    
    # Gera o arquivo tratado em memória para evitar gargalos de escrita em disco
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Dados_Filtrados')
        
    st.sidebar.download_button(
        label="Download da Consulta (.xlsx)",
        data=buffer.getvalue(),
        file_name="relatorio_filtrado_tratado.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )

    # -------------------------------------------------------------------------
    # RENDERIZAÇÃO DA INTERFACE GRÁFICA (FRONT-END)
    # -------------------------------------------------------------------------
    # Divide a tela em Abas organizadas para melhor UX (Experiência do Usuário)
    aba1, aba2 = st.tabs(["📊 Visão Gerencial", "📋 Tabela de Dados Tratados"])

    with aba1:
        # Seção de Cartões de Métricas (KPIs)
        st.markdown("### 📈 Principais Indicadores")
        m1, m2, m3 = st.columns(3)
        
        m1.metric("Volume de Transações", f"{len(df_filtrado):,}".replace(",", "."))
        
        if len(col_num) > 0:
            col_valor_principal = col_num[0]
            faturamento_total = df_filtrado[col_valor_principal].sum()
            ticket_medio = df_filtrado[col_valor_principal].mean() if len(df_filtrado) > 0 else 0
            
            m2.metric("Faturamento Líquido", f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            m3.metric("Ticket Médio por Pedido", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.markdown("---")

        # Seção de Gráficos de Alta Performance (Altair)
        st.markdown("### 📊 Análise Visual")
        g1, g2 = st.columns(2)

        with g1:
            if len(col_texto) > 0 and len(col_num) > 0:
                st.markdown(f"#### Volumetria Financeira por {col_texto[0]}")
                dados_grafico1 = df_filtrado.groupby(col_texto[0])[col_num[0]].sum().reset_index()
                
                chart1 = alt.Chart(dados_grafico1).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X(f'{col_texto[0]}:N', sort='-y', title=col_texto[0]),
                    y=alt.Y(f'{col_num[0]}:Q', title="Total Comercial (R$)"),
                    color=alt.Color(f'{col_texto[0]}:N', legend=None)
                ).properties(height=320)
                st.altair_chart(chart1, use_container_width=True)

        with g2:
            # Tenta plotar gráfico de linhas se houver coluna de data, caso contrário plota barras
            if len(col_data) > 0 and len(col_num) > 0:
                st.markdown("#### Evolução Temporal de Faturamento")
                df_filtrado['Mes_Ano'] = df_filtrado[col_data[0]].dt.to_period('M').astype(str)
                dados_grafico2 = df_filtrado.groupby('Mes_Ano')[col_num[0]].sum().reset_index()
                
                chart2 = alt.Chart(dados_grafico2).mark_line(point=True, color="#1f77b4").encode(
                    x=alt.X('Mes_Ano:N', title="Período (Mês/Ano)"),
                    y=alt.Y(f'{col_num[0]}:Q', title="Faturamento (R$)")
                ).properties(height=320)
                st.altair_chart(chart2, use_container_width=True)
                
            elif len(col_texto) > 1 and len(col_num) > 0:
                st.markdown(f"#### Distribuição de Vendas por {col_texto[1]}")
                dados_grafico2 = df_filtrado.groupby(col_texto[1])[col_num[0]].sum().reset_index()
                
                chart2 = alt.Chart(dados_grafico2).mark_bar().encode(
                    y=alt.Y(f'{col_texto[1]}:N', sort='-x', title=col_texto[1]),
                    x=alt.X(f'{col_num[0]}:Q', title="Total Comercial (R$)"),
                    color=alt.Color(f'{col_texto[1]}:N', legend=None)
                ).properties(height=320)
                st.altair_chart(chart2, use_container_width=True)

    with aba2:
        # Tabela Granular de Auditoria
        st.markdown("### 📋 Base de Dados Higienizada")
        st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Falha crítica no processamento do arquivo: {e}")