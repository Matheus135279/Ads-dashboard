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
        background: #2D1A4D;
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

    /* Título da Plataforma */
    .platform-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0 2rem 0;
        padding: 0.5rem;
    }

    /* Botões do menu */
    div[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: none;
        padding: 15px 20px;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 10px;
        border-radius: 10px;
        color: white;
        font-size: 0.95rem;
        margin: 5px 0;
        transition: all 0.3s ease;
    }

    div[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
    }

    div[data-testid="stSidebar"] button[kind="secondary"].active {
        background-color: rgba(255, 255, 255, 0.1);
    }

    /* Divisor */
    .section-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.1) 50%,
            rgba(255,255,255,0) 100%);
        margin: 2rem 0;
    }

    /* Container principal */
    .main-content {
        padding: 2rem;
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
    # Inicializa o estado da página se não existir
    if "page" not in st.session_state:
        st.session_state.page = "Painel de Campanhas"

    # Sidebar com logo e título
    st.sidebar.markdown("""
        <div class="logo-container">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAABkCAYAAACoy2Z3AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTAyLTE2VDE2OjI5OjA5LTAzOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDI0LTAyLTE2VDE2OjI5OjA5LTAzOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wMi0xNlQxNjoyOTowOS0wMzowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo5ZjVkYzI5MS03ZTZiLWE1NDItOTU3NC0wYzM3NjM2MjI0ZTQiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo2YjY1ZDg4Yy1iNjA4LTRlNGEtODM0ZC1mNzY0NmI1ZjA5MmUiIHN0RXZ0OndoZW49IjIwMjQtMDItMTZUMTY6Mjk6MDktMDM6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyNC4wIChXaW5kb3dzKSIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7ABfj+AAABA0lEQVR42u3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1v9QAATX68/0AAAAASUVORK5CYII=" alt="Logo HubLever">
        </div>
        <div class="platform-title">Plataforma de Resultados</div>
    """, unsafe_allow_html=True)

    # Botões da sidebar
    if st.sidebar.button("🖥️ Painel de Campanhas", key="btn_dashboard", help="Visualizar painel de campanhas"):
        st.session_state.page = "Painel de Campanhas"
    
    if st.sidebar.button("📈 Evolução Diária", key="btn_evolution", help="Ver evolução diária"):
        st.session_state.page = "Evolução Diária"
    
    if st.sidebar.button("📥 Upload de Arquivos", key="btn_upload", help="Fazer upload de arquivos"):
        st.session_state.page = "Upload de Arquivos"
    
    if st.sidebar.button("📤 Exportar Relatórios", key="btn_export", help="Exportar relatórios"):
        st.session_state.page = "Exportar Relatórios"
    
    if st.sidebar.button("⚙️ Configurações", key="btn_settings", help="Configurações do sistema"):
        st.session_state.page = "Configurações"

    # Container principal baseado na página selecionada
    main_container = st.container()
    
    with main_container:
        if st.session_state.page == "Painel de Campanhas":
            st.title("📊 Painel de Campanhas")
            # Conteúdo do painel de campanhas
            show_campaign_dashboard()
        
        elif st.session_state.page == "Evolução Diária":
            st.title("📈 Evolução Diária")
            # Conteúdo da evolução diária
            show_daily_evolution()
        
        elif st.session_state.page == "Upload de Arquivos":
            st.title("📥 Upload de Arquivos")
            # Conteúdo do upload de arquivos
            show_file_upload()
        
        elif st.session_state.page == "Exportar Relatórios":
            st.title("📤 Exportar Relatórios")
            # Conteúdo da exportação de relatórios
            show_export_reports()
        
        elif st.session_state.page == "Configurações":
            st.title("⚙️ Configurações")
            # Conteúdo das configurações
            show_settings()

def show_campaign_dashboard():
    """Função para mostrar o painel de campanhas"""
    # Aqui vai o código original do dashboard de campanhas
    pass

def show_daily_evolution():
    """Função para mostrar a evolução diária"""
    st.write("Em desenvolvimento: Evolução Diária")

def show_file_upload():
    """Função para mostrar a tela de upload"""
    uploaded_file = st.file_uploader("Faça upload do arquivo de exportação do Facebook Ads (CSV ou XLSX)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            # Código existente para processar o arquivo
            pass
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

def show_export_reports():
    """Função para mostrar a tela de exportação"""
    st.write("Em desenvolvimento: Exportação de Relatórios")

def show_settings():
    """Função para mostrar a tela de configurações"""
    st.write("Em desenvolvimento: Configurações")

if __name__ == "__main__":
    main()
