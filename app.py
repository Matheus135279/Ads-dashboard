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
    
    /* Botões do menu */
    .menu-button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        color: white;
        text-decoration: none;
    }
    
    .menu-button:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .menu-button.active {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        border: none;
    }
    
    .menu-button i {
        margin-right: 10px;
        font-size: 1.2rem;
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
    # Sidebar com logo e menu
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <img src="https://hublever.com.br/wp-content/uploads/2024/02/logo-hublever-branco.png" 
                 style="width: 150px; margin-bottom: 2rem;">
            <h2 style="color: white; margin-bottom: 2rem;">Plataforma de Resultados</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu com botões estilizados
    menu_options = {
        "📊 Painel de Campanhas": "dashboard",
        "📈 Evolução Diária": "evolution",
        "📥 Upload de Arquivos": "upload",
        "📁 Exportar Relatórios": "export",
        "⚙️ Configurações": "settings"
    }
    
    selected = st.session_state.get('menu_selected', 'dashboard')
    
    for label, key in menu_options.items():
        button_class = "menu-button active" if selected == key else "menu-button"
        if st.sidebar.markdown(f"""
            <div class="{button_class}">
                {label}
            </div>
            """, unsafe_allow_html=True):
            selected = key
            st.session_state.menu_selected = key
    
    # Header do usuário
    st.markdown("""
        <div class="user-header">
            👤 Cliente: Dra. Jéssica Martani | Último acesso: 16/04/2025
        </div>
    """, unsafe_allow_html=True)
    
    # Gerenciamento de estado do arquivo
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Upload e processamento do arquivo
    if selected == "upload":
        st.header("📥 Upload de Dados")
        uploaded_file = st.file_uploader(
            "Upload do arquivo CSV do Facebook Ads",
            type="csv",
            help="O arquivo deve conter: campaign_name, spend, clicks, impressions, ctr, cpc"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                processed_df = process_facebook_data(df)
                
                if processed_df is not None:
                    st.session_state.df = processed_df
                    st.success("✅ Arquivo processado com sucesso!")
                    
                    # Preview dos dados
                    st.subheader("Preview dos dados carregados")
                    st.dataframe(processed_df.head(), use_container_width=True)
                else:
                    st.error("❌ Erro ao processar o arquivo. Verifique se o formato está correto.")
            except Exception as e:
                st.error(f"""
                ❌ Erro ao carregar o arquivo:
                {str(e)}
                
                Verifique se o arquivo está no formato correto e tente novamente.
                """)
    
    # Renderização das outras seções apenas se houver dados
    elif st.session_state.df is not None:
        df = st.session_state.df
        
        if selected == "dashboard":
            st.header("📊 Painel de Campanhas")
            
            # KPIs
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
            
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            
            # Rankings
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top 5 Campanhas por Cliques")
                top_clicks = df.nlargest(5, 'clicks')[['campaign_name', 'clicks', 'spend']]
                st.dataframe(top_clicks, use_container_width=True)
            
            with col2:
                st.subheader("⚠️ Top 5 Maiores CPCs")
                top_cpc = df.nlargest(5, 'cpc')[['campaign_name', 'cpc', 'clicks']]
                st.dataframe(top_cpc, use_container_width=True)
            
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            
            # Notas por campanha
            st.subheader("📝 Notas e Observações")
            for campaign in df['campaign_name'].unique():
                with st.expander(f"Campanha: {campaign}"):
                    st.text_area("Insights e observações:", key=f"notes_{campaign}")
        
        elif selected == "evolution":
            st.header("📈 Evolução Diária")
            
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df_daily = df.groupby('date').agg({
                    'spend': 'sum',
                    'clicks': 'sum'
                }).reset_index()
                
                # Gráfico de evolução de gastos
                st.plotly_chart(
                    create_evolution_chart(df_daily, 'spend', 'Evolução do Investimento Diário'),
                    use_container_width=True
                )
                
                # Gráfico de evolução de cliques
                st.plotly_chart(
                    create_evolution_chart(df_daily, 'clicks', 'Evolução dos Cliques Diários'),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ O arquivo não contém dados de data para gerar a evolução diária.")
        
        elif selected == "export":
            st.header("📁 Exportar Relatórios")
            
            excel_data = export_to_excel(df)
            st.download_button(
                label="📥 Baixar Relatório Completo (Excel)",
                data=excel_data,
                file_name="relatorio_campanhas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif selected == "settings":
            st.header("⚙️ Configurações")
            st.info("🚧 Área em desenvolvimento...")
    
    else:
        if selected != "upload":
            st.info("👆 Por favor, faça o upload do arquivo CSV na seção 'Upload de Arquivos'.")
            st.sidebar.warning("⚠️ Nenhum arquivo carregado")

if __name__ == "__main__":
    main() 