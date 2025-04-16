import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from base64 import b64encode
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Performance de Anúncios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    /* Tema escuro personalizado */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #1E1B2E 0%, #2D1A4D 100%);
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Barra lateral estilizada */
    [data-testid="stSidebar"] {
        background: rgba(45, 26, 77, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Estilo dos cards de métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Estilo dos títulos */
    h1, h2, h3 {
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Estilo dos gráficos */
    [data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Estilo da tabela de dados */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Estilo do rodapé */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Estilo dos botões */
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2);
    }
    
    /* Divisores personalizados */
    .custom-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.1) 50%,
            rgba(255,255,255,0) 100%);
        margin: 2rem 0;
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
    try:
        # Mapeamento de colunas do Facebook Ads
        column_mapping = {
            "Nome da campanha": "campaign_name",
            "Valor usado (BRL)": "spend",
            "Impressões": "impressions",
            "Cliques no link": "clicks",
            "CTR (taxa de cliques no link)": "ctr",
            "CPC (custo por clique no link)": "cpc",
            "CPM (custo por 1.000 impressões)": "cpm",
            "Alcance": "reach",
            "Resultados": "conversions",
            # Adicionando mapeamentos alternativos comuns
            "Campaign name": "campaign_name",
            "Amount spent (BRL)": "spend",
            "Link clicks": "clicks",
            "CTR (Link click-through rate)": "ctr",
            "CPC (Cost per link click)": "cpc",
            "Impressions": "impressions",
            "Reach": "reach",
            "Results": "conversions"
        }
        
        # Verifica quais colunas obrigatórias estão presentes (usando ambos os nomes possíveis)
        required_columns_pt = [
            "Nome da campanha",
            "Valor usado (BRL)",
            "Impressões",
            "Cliques no link"
        ]
        
        required_columns_en = [
            "Campaign name",
            "Amount spent (BRL)",
            "Impressions",
            "Link clicks"
        ]
        
        # Verifica se as colunas estão presentes em português ou inglês
        missing_columns = []
        for pt, en in zip(required_columns_pt, required_columns_en):
            if pt not in df.columns and en not in df.columns:
                missing_columns.append(f"{pt} / {en}")
        
        if missing_columns:
            st.error(f"""
            ⚠️ Aviso: Este arquivo não contém todas as colunas necessárias para o funcionamento da dashboard.
            
            Colunas faltantes:
            {', '.join(missing_columns)}
            
            Por favor, verifique se você está usando o arquivo de exportação correto do Facebook Ads.
            """)
            return None
        
        # Renomeia as colunas presentes
        columns_to_rename = {old: new for old, new in column_mapping.items() if old in df.columns}
        df = df.rename(columns=columns_to_rename)
        
        # Converte valores para formato numérico
        if "spend" in df.columns:
            df["spend"] = df["spend"].astype(str).str.replace("R$", "").str.replace(".", "").str.replace(",", ".").astype(float)
        if "cpc" in df.columns:
            df["cpc"] = df["cpc"].astype(str).str.replace("R$", "").str.replace(".", "").str.replace(",", ".").astype(float)
        if "cpm" in df.columns:
            df["cpm"] = df["cpm"].astype(str).str.replace("R$", "").str.replace(".", "").str.replace(",", ".").astype(float)
        
        # Remove % e converte CTR
        if "ctr" in df.columns:
            df["ctr"] = df["ctr"].astype(str).str.rstrip("%").astype(float) / 100
        
        # Converte valores inteiros
        numeric_columns = ["impressions", "clicks", "reach", "conversions"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(".", ""), errors="coerce")
        
        # Se não tiver coluna de conversões, cria com zeros
        if "conversions" not in df.columns:
            df["conversions"] = 0
            
        # Se não tiver coluna de alcance, usa impressões
        if "reach" not in df.columns:
            df["reach"] = df["impressions"]
            
        # Preenche valores NaN com 0
        df = df.fillna(0)
            
        return df
        
    except Exception as e:
        st.error(f"""
        ⚠️ Erro ao processar os dados: Algumas colunas não estão no formato esperado.
        
        Detalhes do erro: {str(e)}
        
        Por favor, verifique se os valores numéricos e formatos estão corretos no arquivo.
        """)
        return None

def create_spend_distribution_chart(df):
    """Cria gráfico de pizza de distribuição de gastos"""
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96C93D', '#FF8E53']
    
    fig = px.pie(
        df, 
        values='spend', 
        names='campaign_name',
        title='Distribuição de Investimento por Campanha',
        template='plotly_dark',
        color_discrete_sequence=colors
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hole=0.4,
        marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=2))
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)'
        ),
        title_x=0.5,
        title_font_size=20
    )
    return fig

def create_performance_chart(df):
    """Cria gráfico de barras de performance"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Cliques',
        x=df['campaign_name'],
        y=df['clicks'],
        marker_color='#FF6B6B'
    ))
    
    fig.add_trace(go.Bar(
        name='Conversões',
        x=df['campaign_name'],
        y=df['conversions'],
        marker_color='#4ECDC4'
    ))
    
    fig.update_layout(
        title='Performance por Campanha',
        title_x=0.5,
        title_font_size=20,
        xaxis_title='Campanha',
        yaxis_title='Quantidade',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)'
        )
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
    
    if visualizar and uploaded_file is not None:
        # Lê e processa os dados
        df = pd.read_csv(uploaded_file)
        df = process_facebook_data(df)
        
        if df is not None:
            # Seção de KPIs
            st.header("📈 Métricas Principais")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<p class="metric-label">Investimento Total</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">R$ {df["spend"].sum():,.2f}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<p class="metric-label">Total de Cliques</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">{int(df["clicks"].sum()):,}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<p class="metric-label">CPC Médio</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">R$ {df["spend"].sum() / df["clicks"].sum():.2f}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<p class="metric-label">CTR Médio</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">{(df["clicks"].sum() / df["impressions"].sum() * 100):.2f}%</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col5:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<p class="metric-label">Conversões</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">{int(df["conversions"].sum()):,}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Divisor personalizado
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            
            # Seção de Gráficos
            st.header("📊 Análise Visual")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_spend_distribution_chart(df),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    create_performance_chart(df),
                    use_container_width=True
                )
            
            # Divisor personalizado
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            
            # Dados Detalhados
            st.header("📋 Dados Detalhados")
            st.dataframe(df, use_container_width=True)
            
            # Rodapé com logo
            st.markdown('<div class="footer">', unsafe_allow_html=True)
            st.markdown("""
                <img src="https://hublever.com.br/wp-content/uploads/2024/02/logo-hublever-branco.png" 
                     style="width: 100px; opacity: 0.7;">
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.info("👆 Faça o upload do arquivo CSV do Facebook Ads e clique em 'Visualizar Dados' para começar.")
        
        st.markdown("""
        ### Formato esperado do arquivo CSV:
        
        O arquivo deve conter as seguintes colunas:
        - Nome da campanha / Campaign name
        - Valor usado (BRL) / Amount spent (BRL)
        - Impressões / Impressions
        - Cliques no link / Link clicks
        - CTR / CTR (opcional)
        - CPC / CPC (opcional)
        - Conversões / Results (opcional)
        """)

if __name__ == "__main__":
    main() 