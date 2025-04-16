import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from base64 import b64encode

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Performance de Anúncios",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    /* Fundo principal branco */
    .main {
        background-color: white !important;
    }
    .stApp {
        background-color: white !important;
    }
    
    /* Barra lateral em tons de roxo */
    .css-1d391kg {
        background-color: #6B46C1 !important;
    }
    .css-1d391kg .stButton > button {
        background-color: white !important;
        color: #6B46C1 !important;
    }
    
    /* Cards de métricas */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Botões */
    .stButton > button {
        background-color: #6B46C1 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #553C9A !important;
    }
    
    /* Textos na barra lateral */
    .css-1d391kg .stMarkdown {
        color: white !important;
    }
    
    /* Logo container */
    .logo-container {
        padding: 20px;
        margin-bottom: 30px;
    }
    
    /* Ajustes de cores para outros elementos */
    .stSelectbox label, .stDateInput label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Logo HubLever
st.sidebar.markdown("""
    <div class="logo-container">
        <img src="https://hublever.com.br/wp-content/uploads/2024/02/logo-hublever-branco.png" 
             style="width: 150px;">
    </div>
    """, unsafe_allow_html=True)

def process_facebook_data(df):
    """Processa e valida os dados do Facebook Ads"""
    required_columns = ['campaign_name', 'spend', 'clicks', 'impressions', 'ctr', 'cpc']
    
    # Verifica colunas obrigatórias
    if not all(col in df.columns for col in required_columns):
        st.error("O arquivo CSV não contém todas as colunas necessárias!")
        return None
    
    # Converte colunas numéricas
    df['spend'] = pd.to_numeric(df['spend'], errors='coerce')
    df['clicks'] = pd.to_numeric(df['clicks'], errors='coerce')
    df['impressions'] = pd.to_numeric(df['impressions'], errors='coerce')
    df['ctr'] = pd.to_numeric(df['ctr'], errors='coerce')
    df['cpc'] = pd.to_numeric(df['cpc'], errors='coerce')
    
    if 'conversions' in df.columns:
        df['conversions'] = pd.to_numeric(df['conversions'], errors='coerce')
    else:
        df['conversions'] = 0
        
    return df

def create_spend_distribution_chart(df):
    """Cria gráfico de pizza de distribuição de gastos"""
    fig = px.pie(
        df, 
        values='spend', 
        names='campaign_name',
        title='Distribuição de Investimento por Campanha',
        template='plotly_white'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_performance_chart(df):
    """Cria gráfico de barras de performance"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Cliques',
        x=df['campaign_name'],
        y=df['clicks'],
        marker_color='#2196F3'
    ))
    
    fig.add_trace(go.Bar(
        name='Conversões',
        x=df['campaign_name'],
        y=df['conversions'],
        marker_color='#4CAF50'
    ))
    
    fig.update_layout(
        title='Performance por Campanha',
        xaxis_title='Campanha',
        yaxis_title='Quantidade',
        barmode='group',
        template='plotly_white',
        showlegend=True
    )
    return fig

def create_spend_trend_chart(df):
    """Cria gráfico de linha de tendência de gastos"""
    if 'date' in df.columns:
        fig = px.line(
            df,
            x='date',
            y='spend',
            title='Evolução do Investimento Diário',
            template='plotly_white'
        )
        fig.update_traces(mode='lines+markers')
        return fig
    return None

def main():
    st.title("📊 Dashboard de Performance de Anúncios")
    
    # Upload do arquivo
    st.sidebar.header("Upload de Dados")
    uploaded_file = st.sidebar.file_uploader(
        "Upload do arquivo CSV do Facebook Ads",
        type="csv",
        help="O arquivo deve conter: campaign_name, spend, clicks, impressions, ctr, cpc"
    )
    
    # Botão de visualização
    visualizar = st.sidebar.button("📊 Visualizar Dados", use_container_width=True)
    
    if visualizar:
        if uploaded_file is None:
            st.info("👆 Por favor, faça o upload do arquivo CSV do Facebook Ads para visualizar os dados.")
            return
        
        # Lê e processa os dados
        df = pd.read_csv(uploaded_file)
        df = process_facebook_data(df)
        
        if df is None:
            return
            
        # Seção de KPIs
        st.header("📈 Métricas Principais")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Investimento Total",
                f"R$ {df['spend'].sum():,.2f}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Total de Cliques",
                f"{int(df['clicks'].sum()):,}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "CPC Médio",
                f"R$ {df['spend'].sum() / df['clicks'].sum():.2f}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "CTR Médio",
                f"{(df['clicks'].sum() / df['impressions'].sum() * 100):.2f}%"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col5:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Conversões",
                f"{int(df['conversions'].sum()):,}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Seção de Gráficos
        st.header("📊 Análise Visual")
        
        # Distribuição de Gastos
        st.subheader("Distribuição do Investimento")
        st.plotly_chart(
            create_spend_distribution_chart(df),
            use_container_width=True
        )
        
        # Performance por Campanha
        st.subheader("Performance das Campanhas")
        st.plotly_chart(
            create_performance_chart(df),
            use_container_width=True
        )
        
        # Evolução Temporal (se houver data)
        trend_chart = create_spend_trend_chart(df)
        if trend_chart:
            st.subheader("Evolução do Investimento")
            st.plotly_chart(trend_chart, use_container_width=True)
        
        # Dados Detalhados
        st.header("📋 Dados Detalhados")
        st.dataframe(df)
        
    else:
        st.info("👆 Faça o upload do arquivo CSV do Facebook Ads e clique em 'Visualizar Dados' para começar.")
        
        st.markdown("""
        ### Formato esperado do arquivo CSV:
        
        O arquivo deve conter as seguintes colunas:
        - campaign_name
        - spend
        - clicks
        - impressions
        - ctr
        - cpc
        - conversions (opcional)
        - date (opcional, para gráfico de evolução)
        """)

if __name__ == "__main__":
    main() 