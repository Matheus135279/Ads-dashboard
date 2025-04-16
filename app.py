import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from base64 import b64encode
from datetime import datetime
import io
from openpyxl import Workbook

# Configuração da página
st.set_page_config(
    page_title="Plataforma de Resultados - HubLever",
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
        color: white;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Barra lateral estilizada */
    [data-testid="stSidebar"] {
        background: rgba(45, 26, 77, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem 0;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
        padding: 0 1rem;
    }
    
    /* Logo container */
    .logo-container {
        position: relative;
        width: 100%;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .logo-container img {
        width: 80%;
        max-width: 200px;
        height: auto;
        margin-bottom: 1.5rem;
    }
    
    /* Botões do menu */
    [data-testid="stSidebar"] .stButton > button {
        height: 50px !important;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.4rem 0;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        color: white !important;
        font-size: 0.95rem;
        padding: 0 1.2rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stButton > button.active {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        border: none;
    }
    
    /* Header do usuário */
    .user-header {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Menu da sidebar */
    .sidebar-menu {
        margin: 2rem 0;
    }
    
    .sidebar-menu .stRadio > label {
        color: white !important;
        font-size: 1.1rem;
        padding: 0.5rem 0;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(255,107,107,0.2);
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
    
    /* Tabelas de ranking */
    .ranking-table {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .high-cpc {
        color: #FF6B6B !important;
        font-weight: bold;
    }
    
    /* Área de notas */
    .notes-area {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Botões de exportação */
    .export-button {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        padding: 0.5rem 2rem !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255,107,107,0.2) !important;
    }
    
    .export-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255,107,107,0.3) !important;
    }
    
    /* Divisores */
    .section-divider {
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

def create_evolution_chart(df, metric, title):
    """Cria gráfico de linha com evolução temporal"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[metric],
        mode='lines+markers',
        name=metric.capitalize(),
        line=dict(
            color='#FF6B6B',
            width=3
        ),
        fill='tonexty',
        fillcolor='rgba(255,107,107,0.1)'
    ))
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        title_font_size=20,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Data",
        yaxis_title=metric.capitalize(),
        showlegend=False,
        hovermode='x unified'
    )
    return fig

def export_to_excel(df):
    """Exporta o DataFrame para Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Dados', index=False)
    return output.getvalue()

def main():
    # Sidebar com logo
    st.sidebar.markdown("""
        <div class="logo-container">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAABkCAYAAACoy2Z3AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTAyLTE2VDE2OjI5OjA5LTAzOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDI0LTAyLTE2VDE2OjI5OjA5LTAzOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wMi0xNlQxNjoyOTowOS0wMzowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo5ZjVkYzI5MS03ZTZiLWE1NDItOTU3NC0wYzM3NjM2MjI0ZTQiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIHN0RXZ0OndoZW49IjIwMjQtMDItMTZUMTY6Mjk6MDktMDM6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyNC4wIChXaW5kb3dzKSIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7ABfj+AAABA0lEQVR42u3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1v9QAATX68/0AAAAASUVORK5CYII=" alt="Logo HubLever">
        </div>
    """, unsafe_allow_html=True)

    # Título principal
    st.title("📊 Dashboard de Resultados - Facebook Ads")

    # Upload do arquivo
    uploaded_file = st.file_uploader("Faça upload do arquivo de exportação do Facebook Ads (CSV ou XLSX)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            # Lê o arquivo
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Processa os dados
            df = process_facebook_data(df)

            if df is not None:
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-label">Investimento Total</div>
                            <div class="metric-value">R$ {:.2f}</div>
                        </div>
                    """.format(df["spend"].sum()), unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-label">Total de Cliques</div>
                            <div class="metric-value">{:,.0f}</div>
                        </div>
                    """.format(df["clicks"].sum()), unsafe_allow_html=True)

                with col3:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-label">CTR Médio</div>
                            <div class="metric-value">{:.2%}</div>
                        </div>
                    """.format(df["clicks"].sum() / df["impressions"].sum()), unsafe_allow_html=True)

                with col4:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-label">CPC Médio</div>
                            <div class="metric-value">R$ {:.2f}</div>
                        </div>
                    """.format(df["spend"].sum() / df["clicks"].sum() if df["clicks"].sum() > 0 else 0), unsafe_allow_html=True)

                # Divisor
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                # Gráficos de evolução
                st.subheader("📈 Evolução dos Resultados")
                
                # Agrupa dados por campanha
                campaign_data = df.groupby("campaign_name").agg({
                    "spend": "sum",
                    "clicks": "sum",
                    "impressions": "sum",
                    "conversions": "sum"
                }).reset_index()

                # Calcula métricas adicionais
                campaign_data["ctr"] = campaign_data["clicks"] / campaign_data["impressions"]
                campaign_data["cpc"] = campaign_data["spend"] / campaign_data["clicks"]
                campaign_data["conversion_rate"] = campaign_data["conversions"] / campaign_data["clicks"]
                campaign_data["cost_per_conversion"] = campaign_data["spend"] / campaign_data["conversions"]

                # Ordena campanhas por gasto
                campaign_data = campaign_data.sort_values("spend", ascending=False)

                # Gráfico de barras para gastos por campanha
                fig_spend = px.bar(
                    campaign_data,
                    x="campaign_name",
                    y="spend",
                    title="Investimento por Campanha",
                    labels={"campaign_name": "Campanha", "spend": "Investimento (R$)"},
                    template="plotly_dark"
                )
                fig_spend.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False
                )
                st.plotly_chart(fig_spend, use_container_width=True)

                # Gráfico de dispersão CPC vs CTR
                fig_scatter = px.scatter(
                    campaign_data,
                    x="ctr",
                    y="cpc",
                    text="campaign_name",
                    title="CPC vs CTR por Campanha",
                    labels={"ctr": "CTR", "cpc": "CPC (R$)"},
                    template="plotly_dark"
                )
                fig_scatter.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                fig_scatter.update_traces(
                    textposition="top center",
                    marker=dict(size=12, color="#FF6B6B")
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

                # Divisor
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                # Tabela de resultados
                st.subheader("📋 Resultados Detalhados")
                
                # Formata as colunas numéricas
                campaign_data_display = campaign_data.copy()
                campaign_data_display["spend"] = campaign_data_display["spend"].apply(lambda x: f"R$ {x:.2f}")
                campaign_data_display["ctr"] = campaign_data_display["ctr"].apply(lambda x: f"{x:.2%}")
                campaign_data_display["cpc"] = campaign_data_display["cpc"].apply(lambda x: f"R$ {x:.2f}")
                campaign_data_display["conversion_rate"] = campaign_data_display["conversion_rate"].apply(lambda x: f"{x:.2%}")
                campaign_data_display["cost_per_conversion"] = campaign_data_display["cost_per_conversion"].apply(lambda x: f"R$ {x:.2f}")
                
                # Renomeia as colunas para exibição
                campaign_data_display = campaign_data_display.rename(columns={
                    "campaign_name": "Campanha",
                    "spend": "Investimento",
                    "clicks": "Cliques",
                    "impressions": "Impressões",
                    "conversions": "Conversões",
                    "ctr": "CTR",
                    "cpc": "CPC",
                    "conversion_rate": "Taxa de Conversão",
                    "cost_per_conversion": "Custo por Conversão"
                })
                
                st.dataframe(campaign_data_display, use_container_width=True)

                # Botão de exportação
                st.download_button(
                    label="📥 Exportar Dados",
                    data=export_to_excel(campaign_data),
                    file_name=f"resultados_facebook_ads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="export_button"
                )

        except Exception as e:
            st.error(f"""
            ⚠️ Erro ao processar o arquivo: {str(e)}
            
            Por favor, verifique se o arquivo está no formato correto e tente novamente.
            """)

if __name__ == "__main__":
    main()
