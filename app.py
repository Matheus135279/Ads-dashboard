import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from api_connectors import process_facebook_csv, process_google_csv
from utils import (
    calculate_metrics, create_performance_chart, create_platform_comparison,
    create_campaign_distribution, format_currency, format_percentage, format_number,
    export_to_excel, export_to_pdf, create_date_filters, create_platform_filter
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Performance de Anúncios",
    page_icon="📊",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .upload-section {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
        border: none;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

def create_daily_spend_chart(df):
    """Cria gráfico de linha para gastos diários"""
    fig = go.Figure()
    
    for platform in df['platform'].unique():
        platform_data = df[df['platform'] == platform]
        fig.add_trace(go.Scatter(
            x=platform_data['date'],
            y=platform_data['spend'],
            name=platform,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title='Evolução do Gasto Diário',
        xaxis_title='Data',
        yaxis_title='Investimento (R$)',
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_campaign_performance_chart(df):
    """Cria gráfico de barras para cliques e conversões por campanha"""
    fig = go.Figure()
    
    campaigns = df.groupby('campaign_name').agg({
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    fig.add_trace(go.Bar(
        name='Cliques',
        x=campaigns['campaign_name'],
        y=campaigns['clicks'],
        marker_color='#2196F3'
    ))
    
    fig.add_trace(go.Bar(
        name='Conversões',
        x=campaigns['campaign_name'],
        y=campaigns['conversions'],
        marker_color='#4CAF50'
    ))
    
    fig.update_layout(
        title='Performance por Campanha',
        xaxis_title='Campanha',
        yaxis_title='Quantidade',
        barmode='group',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def main():
    st.title("📊 Dashboard de Performance de Anúncios")
    
    # Seção de upload de arquivos
    with st.sidebar:
        st.markdown("## Upload de Arquivos")
        
        with st.form("upload_form"):
            st.markdown('<div class="upload-section">', unsafe_allow_html=True)
            st.markdown("### Facebook Ads")
            facebook_csv = st.file_uploader(
                "Upload do arquivo CSV do Facebook Ads",
                type="csv",
                help="Arquivo deve conter: campaign_name, spend, impressions, clicks, ctr, cpc, cpm, reach"
            )
            
            st.markdown("### Google Ads")
            google_csv = st.file_uploader(
                "Upload do arquivo CSV do Google Ads",
                type="csv",
                help="Arquivo deve conter: campaign_name, cost, impressions, clicks, ctr, avg_cpc, avg_cpm"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Filtros
            st.markdown("## Filtros")
            start_date, end_date = create_date_filters()
            selected_platforms = create_platform_filter()
            
            # Botão de visualização
            visualizar = st.form_submit_button("📊 Visualizar Dados", use_container_width=True)
    
    # Processamento e exibição dos dados
    if visualizar:
        data_frames = []
        
        if facebook_csv and "Facebook" in selected_platforms:
            fb_data = process_facebook_csv(facebook_csv)
            if not fb_data.empty:
                data_frames.append(fb_data)
                
        if google_csv and "Google" in selected_platforms:
            google_data = process_google_csv(google_csv)
            if not google_data.empty:
                data_frames.append(google_data)
        
        if not data_frames:
            st.info("👆 Faça o upload dos arquivos CSV do Facebook Ads e/ou Google Ads para visualizar os dados.")
            st.markdown("""
            ### Formato esperado dos arquivos CSV:
            
            **Facebook Ads:**
            - campaign_name
            - spend
            - impressions
            - clicks
            - ctr
            - cpc
            - cpm
            - reach
            - conversions (opcional)
            
            **Google Ads:**
            - campaign_name
            - cost
            - impressions
            - clicks
            - ctr
            - avg_cpc
            - avg_cpm
            - conversions (opcional)
            """)
            return
        
        # Combina os dados
        df = pd.concat(data_frames, ignore_index=True)
        
        # Calcular métricas
        metrics = calculate_metrics(df)
        
        # Seção de KPIs
        st.header("📈 Métricas Principais")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Investimento Total", format_currency(metrics['total_spend']))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("CPM Médio", format_currency(metrics['avg_cpm']))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("CPC Médio", format_currency(metrics['avg_cpc']))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Conversões", format_number(metrics['total_conversions']))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col5:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("CTR Médio", format_percentage(metrics['avg_ctr']))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Seção de Gráficos
        st.header("📊 Análise Visual")
        
        # Gráfico de Pizza - Distribuição de Investimento
        st.subheader("Distribuição de Investimento por Campanha")
        st.plotly_chart(create_campaign_distribution(df), use_container_width=True)
        
        # Gráfico de Barras - Performance por Campanha
        st.subheader("Cliques e Conversões por Campanha")
        st.plotly_chart(create_campaign_performance_chart(df), use_container_width=True)
        
        # Gráfico de Linha - Evolução Temporal
        st.subheader("Evolução do Investimento Diário")
        st.plotly_chart(create_daily_spend_chart(df), use_container_width=True)
        
        # Tabela detalhada
        st.header("📋 Dados Detalhados")
        st.dataframe(df)
        
        # Exportação
        st.header("📥 Exportar Relatórios")
        col1, col2 = st.columns(2)
        with col1:
            excel_data = export_to_excel(df)
            st.download_button(
                "📥 Exportar para Excel",
                excel_data,
                "performance_ads.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        with col2:
            pdf_data = export_to_pdf(
                [create_campaign_distribution(df),
                 create_campaign_performance_chart(df),
                 create_daily_spend_chart(df)],
                {"period": f"{start_date} a {end_date}",
                 "total_spend": metrics['total_spend'],
                 "total_clicks": metrics['total_clicks'],
                 "total_conversions": metrics['total_conversions']}
            )
            st.download_button(
                "📥 Exportar para PDF",
                pdf_data,
                "relatorio_ads.pdf",
                "application/pdf"
            )

if __name__ == "__main__":
    main() 