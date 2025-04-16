import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from api_connectors import FacebookAdsConnector, GoogleAdsConnector, load_csv_data
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
    </style>
    """, unsafe_allow_html=True)

# Autenticação simples
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("## Login")
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if username == st.secrets["STREAMLIT_USERNAME"] and password == st.secrets["STREAMLIT_PASSWORD"]:
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Usuário ou senha incorretos")
        return False
    return True

def main():
    st.title("📊 Dashboard de Performance de Anúncios")
    
    # Filtros
    with st.sidebar:
        st.header("Filtros")
        start_date, end_date = create_date_filters()
        selected_platforms = create_platform_filter()
        
        # Upload de arquivos CSV
        st.header("Upload de Dados")
        facebook_csv = st.file_uploader("Dados do Facebook Ads (CSV)", type="csv")
        google_csv = st.file_uploader("Dados do Google Ads (CSV)", type="csv")
    
    # Carregar dados
    try:
        data = []
        
        if "Facebook" in selected_platforms:
            if facebook_csv:
                fb_data = load_csv_data(facebook_csv, "Facebook")
            else:
                fb_connector = FacebookAdsConnector()
                fb_data = fb_connector.get_campaigns_data(start_date, end_date)
            data.append(fb_data)
            
        if "Google" in selected_platforms:
            if google_csv:
                google_data = load_csv_data(google_csv, "Google")
            else:
                google_connector = GoogleAdsConnector()
                google_data = google_connector.get_campaigns_data(start_date, end_date)
            data.append(google_data)
        
        if not data:
            st.warning("Selecione pelo menos uma plataforma e forneça os dados necessários.")
            return
            
        df = pd.concat(data, ignore_index=True)
        
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
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")

if __name__ == "__main__":
    if check_password():
        main() 