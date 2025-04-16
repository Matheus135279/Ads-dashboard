import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
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
    }
    .upload-section {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("📊 Dashboard de Performance de Anúncios")
    
    # Seção de upload de arquivos
    st.sidebar.markdown("## Upload de Arquivos")
    
    with st.sidebar:
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
    
    # Processamento dos dados
    data_frames = []
    
    if facebook_csv and "Facebook" in selected_platforms:
        fb_data = process_facebook_csv(facebook_csv)
        if not fb_data.empty:
            data_frames.append(fb_data)
            
    if google_csv and "Google" in selected_platforms:
        google_data = process_google_csv(google_csv)
        if not google_data.empty:
            data_frames.append(google_data)
    
    # Verifica se há dados para mostrar
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
    
    # Cards de métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Investimento Total", format_currency(metrics['total_spend']))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total de Cliques", format_number(metrics['total_clicks']))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("CTR Médio", format_percentage(metrics['avg_ctr']))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Conversões", format_number(metrics['total_conversions']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráficos
    st.subheader("Performance ao Longo do Tempo")
    metric_options = ["spend", "clicks", "impressions", "conversions"]
    selected_metric = st.selectbox("Selecione a métrica", metric_options)
    st.plotly_chart(create_performance_chart(df, selected_metric), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Comparação entre Plataformas")
        st.plotly_chart(create_platform_comparison(df, selected_metric), use_container_width=True)
        
    with col2:
        st.subheader("Distribuição de Investimento")
        st.plotly_chart(create_campaign_distribution(df), use_container_width=True)
    
    # Tabela detalhada
    st.subheader("Dados Detalhados")
    st.dataframe(df)
    
    # Exportação
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
            [create_performance_chart(df, "spend"),
             create_platform_comparison(df, "spend"),
             create_campaign_distribution(df)],
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