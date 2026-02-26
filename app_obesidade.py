import streamlit as st
import pandas as pd
import joblib
from utils import feature_eng_trans, DropColumns, OrdinalEnconding, OneHotEncoding, MinMax
import os


# Configuração da página

st.set_page_config(page_title = 'Predição de Obesidade',
        layout = 'centered')

# Título e descrição

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🩺 Calculadora de Risco de Obesidade</h1>", unsafe_allow_html=True) 
st.markdown("----")
st.markdown("Responda as perguntas abaixo para que nosso modelo de inteligência artificial analise seu perfil de saúde.")

# Bloco 1: Dados pessoais e biomátricos

st.header("1. Dados Pessoais")

col1, col2 = st.columns(2)

with col1:
    genero = st.selectbox("Qual o seu gênero?", ["Mulher", "Homem"])
    idade = st.number_input("Qual a sua idade?", min_value=10, max_value=100, value=25, step=1)
    hist_familiar = st.radio("Tem histórico de obesidade na família?", ["Sim", "Não"])

with col2:
    #Apenas para cálculo do IMC para mostrar na tela, mas o modelo não usará essas informações
    altura = st.number_input("Qual a sua altura? (em metros)", min_value=1.00, max_value=2.50, value=1.70, step=0.01)
    peso = st.number_input("Qual é o seu peso? (em kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)

st.markdown("----")

# Bloco 2: Hábitos alimentares

st.header("2. Hábitos Alimentares")

col3, col4 = st.columns(2)

with col3:
    consumo_vegetais = st.select_slider("Com que frequência você come vegetais?", options=["Raramente", "Às vezes", "Sempre"])
    qtd_refeicoes = st.number_input("Quantas refeições você faz por dia?", min_value=1, max_value=4, value=3, help="Ex. Café, almoço e jantar = 3 refeições diárias")
    comer_entre_refeicoes = st.selectbox("Você costuma 'beliscar' entre as refeições?",
                                        options=["Não consome", "Às vezes", "Frequentemente", "Sempre"])
    alimento_calorico = st.radio("Você consome alimentos hipercalóricos (frituras/doces) com frequência?", ["Sim", "Não"])
    
  
with col4:
    mapa_agua = {"Menos de 1 litro":1,
                "Entre 1 e 2 litros":2,
                "Mais de 2 litros":3}

    agua_texto = st.selectbox("Quantos litros de água você bebe por dia?", options=["Menos de 1 litro", "Entre 1 e 2 litros", "Mais de 2 litros"])

    consumo_agua_diario = mapa_agua[agua_texto]

    consumo_alcool = st.selectbox("Com que frequência você consome álcool?",
                                options=["Não consome", "Às vezes", "Frequentemente", "Sempre"])

    monitoramento = st.checkbox("Monitoro as minhas calorias ao longo do dia.")
    monitoramento_caloria = "Sim" if monitoramento else "Não"

st.markdown("----")

# Bloco 3: Estilo de vida

st.header("3. Estilo de vida")

col5, col6 = st.columns(2)

with col5:
    mapa_faf = {"Não pratico atividade física":0, "1 a 2 dias por semana": 1, "3 a 4 dias por semana":2, "5 ou mais dias por semana":3}

    faf_texto = st.selectbox("Com que frequência você faz atividade física?", options=list(mapa_faf.keys()))

    freq_atividade_fisica = mapa_faf[faf_texto]

    
    mapa_tue = {"0 a 2 horas por dia":0, "3 a 5 horas por dia": 1, "Mais de 5 horas por dia":2}

    tue_texto = st.selectbox("Quanto tempo você usa celular/computador fora do trabalho?", options=list(mapa_tue.keys()))

    tempo_disp_eletronico = mapa_tue[tue_texto]

with col6:
    meio_transporte = st.selectbox("Qual seu principal meio de transporte?", options=["Transporte público", "Carro",
                                                                                    "Caminhada", "Bicicleta", "Moto"])
    fumante = st.radio("Você fuma?", ["Sim", "Não"])

st.markdown("----")

# Botão de cálculo

if st.button("🔍 Calcular Risco", type="primary", use_container_width=True):
    #Cálculo IMC:  
    imc = peso / (altura ** 2)
    
    # Lógica de Classificação do IMC (Padrão OMS)
    if imc < 18.5:
        classificacao_imc = "Abaixo do peso"
        cor_alerta = "blue" # Apenas informativo
    elif 18.5 <= imc < 25:
        classificacao_imc = "Peso ideal"
        cor_alerta = "green" # Sucesso
    elif 25 <= imc < 30:
        classificacao_imc = "Sobrepeso"
        cor_alerta = "orange" # Atenção
    else:
        classificacao_imc = "Obesidade"
        cor_alerta = "red" # Perigo

    # Exibindo na tela com destaque
    st.markdown("### 📊 Resultado técnico - IMC")
    col_imc1, col_imc2 = st.columns(2)
    
    with col_imc1:
        st.metric("Seu IMC é", f"{imc:.2f} kg/m²")
    
    with col_imc2:
        # Mostra uma caixinha colorida dependendo do resultado
        if cor_alerta == "green":
            st.success(f"Classificação: {classificacao_imc}")
        elif cor_alerta == "orange":
            st.warning(f"Classificação: {classificacao_imc}")
        elif cor_alerta == "red":
            st.error(f"Classificação: {classificacao_imc}")
        else:
            st.info(f"Classificação: {classificacao_imc}")
            
    st.markdown("---")
    
    
    # 1. Cria o DataFrame com os dados brutos (Dicionário)
    input_dict = {
        'genero': genero,
        'idade': idade,
        'altura': altura,
        'peso': peso,
        'hist_familiar': hist_familiar,
        'consumo_alimento_calorico': 'Sim' if alimento_calorico == 'Sim' else 'Não', # Garante string
        'consumo_vegetais': consumo_vegetais,
        'qtd_refeicoes_principais': qtd_refeicoes,
        'comer_entre_refeicoes': comer_entre_refeicoes,
        'fumante': fumante,
        'consumo_agua_diario': consumo_agua_diario,
        'monitoramento_caloria': monitoramento_caloria,
        'freq_atividade_fisica': freq_atividade_fisica,
        'tempo_disp_eletronico': tempo_disp_eletronico,
        'consumo_alcool': consumo_alcool,
        'meio_transporte': meio_transporte
    }
    
    # Transforma em DataFrame (uma linha)
    input_df = pd.DataFrame([input_dict])
    
# Previsão com IA

    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            
        caminho_modelo = os.path.join(diretorio_atual, 'modelo', 'random_forest_modelo_pipeline.joblib')
        
        pipeline = joblib.load(caminho_modelo)

        input_tratado = feature_eng_trans(input_df)

        predicao = pipeline.predict(input_tratado)[0]
        probabilidade = pipeline.predict_proba(input_tratado)[0]

        mapa_resultado = {0:"Abaixo do peso/Peso normal", 1:"Sobrepeso (alerta)", 2:"Obesidade (risco elevado)"}

        resultado_texto = mapa_resultado[predicao]

        st.subheader(f"Resultado do modelo (avaliação de hábitos alimentares e estilo de vida): {resultado_texto}")

        col_prob1, col_prob2, col_prob3 = st.columns(3)

        with col_prob1:
            st.metric("Prob. Normal", f"{probabilidade[0]:.1%}")
        with col_prob2:
            st.metric("Prob. Sobrepeso", f"{probabilidade[1]:.1%}")
        with col_prob3:
            st.metric("Prob. Obesidade", f"{probabilidade[2]:.1%}")

        if predicao == 0:
            st.success("Parabéns! Seus hábitos indicam um perfil saudável. Continue assim!")
        elif predicao == 1:
            st.warning("Atenção! O modelo identificou padrões de risco para sobrepeso. Considere rever seus hábitos diários.")
        else:
            st.error("Alerta! O modelo identificou alta probabilidade de obesidade. Recomendamos buscar orientação médica especializada.")

    except FileNotFoundError:
        st.error("Erro: O arquivo 'random_forest_modelo_pipeline.joblib' não foi encontrado na pasta. Verifique se você salvou o modelo.")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado no processamento: {e}")