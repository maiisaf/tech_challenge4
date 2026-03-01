import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title ="Dashboard Médico - Obesidade", layout="centered")

@st.cache_data
def load_dados():
    df = pd.read_csv("base_de_dados.csv")
    if "imc" not in df.columns and "peso" in df.columns and "altura" in df.columns:
        df["imc"] = df["peso"] / (df["altura"] ** 2)
    return df

df = load_dados()

# Formatação de separador brasileira

def format_sep(valor, decimal=False):
    if decimal:
        return f"{valor:.1f}".replace(".", ",")
    return f"{valor:,.0f}".replace(",", ".")

# Estilização dos cards

st.markdown("""
        <style>
        .stApp {background-color: #f4f7f9;}
        .kpi-card {
              background-color: white;
        padding: 12px 65px;
        border-radius: 0px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        border-right: 8px solid #2E86C1;
        min-height: 80px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;}
        .kpi-label {
                font-size: 13px;
                color: #666;
                font-weight: 700;
                margin-bottom: 10px;
                white-space: nowrap;}
        .kpi-value{
                font-size: 18px;
                font-weight: bold;
                color: #333;
                white-space: nowrap;}
        </style>""", unsafe_allow_html=True)

# Títulos e subtítulos

st.markdown("<h1 style='text-align: center; color: #2E86C1;'> 🩺 Painel de Análise de Saúde Populacional</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Monitoramento de risco de obesidade e hábitos de vida para equipe médica.</p>", unsafe_allow_html=True)
st.markdown("----")


#------------------------------------------------------------
# Filtros
#------------------------------------------------------------

st.sidebar.header("🔍 Filtros de Segmentação")

genero = st.sidebar.multiselect("Gênero", options=df["genero"].unique(),
                            default=df["genero"].unique())

idade_min, idade_max = int(df["idade"].min()), int(df["idade"].max())
faixa_etaria = st.sidebar.slider("Faixa Etária", min_value=idade_min, max_value=idade_max,
                                    value=(idade_min, idade_max))

opcoes_hist = ["Todos", "Sim", "Não"]
hist_selecionado = st.sidebar.selectbox("Histórico Familiar", opcoes_hist)

opcoes_fumo = ["Todos", "Sim", "Não"]
fumo_selecionado = st.sidebar.selectbox("Paciente Fumante", opcoes_fumo)

imc_min_atual, imc_max_atual = float(df["imc"].min()), float(df["imc"].max())
faixa_imc = st.sidebar.slider("IMC (kg/m²)", min_value=imc_min_atual, max_value=imc_max_atual,
                                    value=(imc_min_atual, imc_max_atual))

ordem_diagnostico = [
    "Abaixo do peso", "Peso normal", "Sobrepeso nível I", 
    "Sobrepeso nível II", "Obesidade tipo I", 
    "Obesidade tipo II", "Obesidade tipo III"]
niveis_selecionados = st.sidebar.multiselect(
    "Filtrar Diagnósticos",
    options=ordem_diagnostico,
    default=ordem_diagnostico)

#------------------------------------------------------------
#Aplicação da lógica de filtragem
#------------------------------------------------------------

df_filtrado = df[(df["genero"].isin(genero)) & (df["idade"].between(faixa_etaria[0], faixa_etaria[1])) &
            (df["imc"].between(faixa_imc[0], faixa_imc[1]))]

if hist_selecionado!= "Todos":
    df_filtrado = df_filtrado[df_filtrado["hist_familiar"] == hist_selecionado]

if fumo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["fumante"] == fumo_selecionado]

df_filtrado = df_filtrado[df_filtrado['nivel_obesidade'].isin(niveis_selecionados)]

#------------------------------------------------------------
# Cálculo de indicadores
#------------------------------------------------------------

total_pacientes = len(df_filtrado)
prevalencia_obesidade = (df_filtrado["nivel_obesidade"].str.contains("Obesidade").sum() / total_pacientes) * 100
hist_familiar_pct = ((df_filtrado["hist_familiar"] == "Sim").sum() / total_pacientes) * 100
imc_medio = df_filtrado["imc"].mean()
taxa_alerta_imc = ((df_filtrado["imc"] > 30).sum() / total_pacientes) * 100
maior_imc = df_filtrado["imc"].max()
media_idade = df_filtrado["idade"].mean() if total_pacientes > 0 else 0
pacientes_sedentarios = (((df_filtrado[ "freq_atividade_fisica"] == 0).sum()) / total_pacientes) * 100

# Exibição de indicadores - cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Pacientes</div>
        <div class="kpi-value">{format_sep(total_pacientes)}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Prevalência Obesidade</div>
        <div class="kpi-value">{format_sep(prevalencia_obesidade, True)}%</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Hist. Familiar</div>
        <div class="kpi-value">{format_sep(hist_familiar_pct, True)}%</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Média de Idade</div>
        <div class="kpi-value">{format_sep(media_idade)}<span class="unit"> anos</div>
    </div>""", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">IMC Médio</div>
        <div class="kpi-value">{format_sep(imc_medio, True)}<span class="unit"> m/kg<sup>2</sup> </div>
    </div>""", unsafe_allow_html=True)

with col6:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Taxa IMC > 30</div>
        <div class="kpi-value">{format_sep(taxa_alerta_imc, True)}%</div>
    </div>""", unsafe_allow_html=True)

with col7:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Maior IMC Registrado</div>
        <div class="kpi-value">{format_sep(maior_imc, True)}<span class="unit"> kg/m<sup>2</sup></div>
    </div>""", unsafe_allow_html=True)

with col8:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Taxa de Sedentarismo</div>
        <div class="kpi-value">{format_sep(pacientes_sedentarios, True)}%</div>
    </div>""", unsafe_allow_html=True)

#------------------------------------------------------------
#Gráficos
#------------------------------------------------------------
st.markdown("----")
st.markdown("<h3 style='text-align: center;'> Visão de Diagnóstico (Perfil Geral)</h3>", unsafe_allow_html=True)

tons_azul = [
    '#CCE6FF',  # Abaixo do peso
    '#80C0FF',  # Peso normal
    '#3399FF',  # Sobrepeso nível I
    '#0073E6',  # Sobrepeso nível II
    '#0059B3',  # Obesidade tipo I
    '#004080',  # Obesidade tipo II
    '#001F3F'   # Obesidade tipo III
]

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    df_donut = df_filtrado["nivel_obesidade"].value_counts().reset_index()
    df_donut.columns = ["Nível", "Total"]

    fig_donut = px.pie(
        df_donut,
        values="Total",
        names="Nível",
        hole=0.5,
        title="Distribuição do Níveis de Obesidade",
        color_discrete_sequence = tons_azul,
        category_orders={"Nível": ordem_diagnostico})

    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    fig_donut.update_layout(
        showlegend=False,
        margin=dict(t=50, b=20, l=20, r=20),
        height=450)

    st.plotly_chart(fig_donut, use_container_width=True)

with col_graf2:
    fig_hist = px.histogram(
        df_filtrado, 
        x="idade", 
        color="nivel_obesidade",
        title="Distribuição de Idade por Diagnóstico",
        labels={'idade': 'Idade (Anos)', 'nivel_obesidade': 'Diagnóstico', 'count': 'Nº de Pacientes'},
        barmode='stack', # Barras empilhadas para ver o volume total por idade
        category_orders={"nivel_obesidade": ordem_diagnostico},
        color_discrete_sequence=tons_azul
    )
    
    fig_hist.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Volume de Pacientes",
        legend_title="Diagnóstico",
        height=450,
        bargap = 0.2,
        margin=dict(t=50, b=20, l=20, r=20),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02)
    )

    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("----")
st.markdown("<h3 style='text-align: center;'>Visão de Hábitos e Estilo de Vida (Causas)</h3>", unsafe_allow_html=True)

col_hab1, col_hab2 = st.columns(2)

with col_hab1:
    fig_dieta = px.histogram(
        df_filtrado, 
        x="nivel_obesidade", 
        color="consumo_alimento_calorico",
        barmode="group",
        title="Impacto da Dieta Calórica por Diagnóstico",
        category_orders={"nivel_obesidade": ordem_diagnostico},
        color_discrete_map={"Sim": "#001F3F", "Não": "#CCE6FF"}, # Destaque para o 'Sim' em azul escuro
        labels={'nivel_obesidade': 'Diagnóstico', 'consumo_alimento_calorico': 'Consome Alimentos Calóricos'}
    )
    
    fig_dieta.update_layout(
        height=450, 
        bargap=0.2,
        xaxis_title=None,
        yaxis_title="Quantidade de Pacientes",
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_dieta, use_container_width=True)

with col_hab2:
    # Calculando a média de atividade física para cada nível
    df_atividade = df_filtrado.groupby('nivel_obesidade')['freq_atividade_fisica'].mean().reset_index()
    
    fig_ativ = px.bar(
        df_atividade,
        x='nivel_obesidade',
        y='freq_atividade_fisica',
        title="Média de Atividade Física semanal",
        category_orders={"nivel_obesidade": ordem_diagnostico},
        color='nivel_obesidade',
        color_discrete_sequence=tons_azul,
        labels={'freq_atividade_fisica': 'Freq. Média (0-3)', 'nivel_obesidade': 'Diagnóstico'}
    )
    
    fig_ativ.update_layout(
        height=450,
        bargap=0.2,
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Frequência Média (Semana)"
    )
    st.plotly_chart(fig_ativ, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # Espaço extra
fig_scatter = px.scatter(
    df_filtrado,
    x="peso",
    y="consumo_agua_diario",
    color="nivel_obesidade",
    title="Relação entre Peso, Consumo de Água e Diagnóstico",
    labels={'peso': 'Peso (kg)', 'consumo_agua_diario': 'Consumo de Água (Litros/Dia)', 'nivel_obesidade': 'Diagnóstico'},
    category_orders={"nivel_obesidade": ordem_diagnostico},
    color_discrete_sequence=tons_azul,
    size="imc", # O tamanho do ponto reflete o IMC
    hover_data=['idade', 'genero'] # Informações extras ao passar o mouse
)

fig_scatter.update_layout(
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Visão de Rotina (Fatores Ambientais)</h3>", unsafe_allow_html=True)

col_rot1, col_rot2 = st.columns(2)

with col_rot1:
    # Contagem para o gráfico de barras
    df_transporte = df_filtrado.groupby(['meio_transporte', 'nivel_obesidade']).size().reset_index(name='Pacientes')
    
    fig_trans = px.bar(
        df_transporte,
        y="meio_transporte",
        x="Pacientes",
        color="nivel_obesidade",
        orientation='h', # Transforma em barras horizontais
        title="Meio de Transporte vs. Diagnóstico",
        category_orders={"nivel_obesidade": ordem_diagnostico},
        color_discrete_sequence=tons_azul,
        labels={'meio_transporte': 'Transporte', 'Pacientes': 'Quantidade de Pacientes'}
    )
    
    fig_trans.update_layout(
        legend_title="Diagnóstico",
        height=450,
        bargap=0.2,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02)
    )
    st.plotly_chart(fig_trans, use_container_width=True)

with col_rot2:
    fig_box = px.box(
        df_filtrado,
        x="nivel_obesidade",
        y="tempo_disp_eletronico",
        title="Sedentarismo Digital por Categoria",
        color="nivel_obesidade",
        category_orders={"nivel_obesidade": ordem_diagnostico},
        color_discrete_sequence=tons_azul,
        labels={'tempo_disp_eletronico': 'Uso de Tecnologia (Horas/Dia)', 'nivel_obesidade': 'Diagnóstico'}
    )
    
    fig_box.update_layout(
        height=450,
        showlegend=False, # Como o eixo X já tem os nomes, não precisa de legenda
        xaxis_title=None,
        yaxis_title="Tempo Diário (0-2)" # Escala comum do dataset TUE
    )
    # Melhora a visualização dos pontos (outliers)
    fig_box.update_traces(marker=dict(size=3))
    
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Análise Detalhada de IMC (Índice de Massa Corporal)</h3>", unsafe_allow_html=True)

col_imc1, col_imc2 = st.columns(2)

with col_imc1:
    imc_medio_valor = df_filtrado['imc'].mean() if not df_filtrado.empty else 0
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = imc_medio_valor,
        title = {'text': "IMC Médio do Grupo"},
        number = {'suffix': " kg/m²", 'valueformat': ".1f"},
        gauge = {
            'axis': {'range': [10, 50], 'tickwidth': 1},
            'bar': {'color': "#d3d3d3"}, # Cor do ponteiro
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [10, 18.5], 'color': "#CCE6FF"}, # Abaixo do Peso
                {'range': [18.5, 25], 'color': "#80C0FF"}, # Saudável 
                {'range': [25, 30], 'color': "#0073E6"},   # Sobrepeso
                {'range': [30, 50], 'color': "#001F3F"}    # Obesidade 
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': imc_medio_valor
            }
        }
    ))
    
    fig_gauge.update_layout(height=400, margin=dict(t=50, b=20, l=30, r=30))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_imc2:
    fig_dist_imc = px.histogram(
        df_filtrado,
        x="imc",
        title="Frequência por Valor de IMC",
        labels={'imc': 'IMC (kg/m²)', 'count': 'Nº de Pacientes'},
        color_discrete_sequence=['#001F3F'],
        nbins=40 # Barras finas para ver o detalhe da curva
    )
    
    fig_dist_imc.update_layout(
        height=400,
        bargap=0.1,
        xaxis_title="IMC kg/m² ",
        yaxis_title="Volume de Pacientes"
    )
    st.plotly_chart(fig_dist_imc, use_container_width=True)

# 3. Boxplot de IMC por Gênero (Variabilidade)
st.markdown("<br>", unsafe_allow_html=True)
fig_box_imc = px.box(
    df_filtrado,
    x="genero",
    y="imc",
    color="genero",
    title="Variabilidade de IMC por Gênero",
    labels={'imc': 'IMC (kg/m²)', 'genero': 'Gênero'},
    color_discrete_map={'Mulher': '#80C0FF', 'Homem': '#004080'} # Tons de azul consistentes
)

fig_box_imc.update_layout(height=450, showlegend=False)
st.plotly_chart(fig_box_imc, use_container_width=True)