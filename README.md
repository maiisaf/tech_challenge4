# Calculadora de Risco de Saúde e Obesidade com IA

Este projeto utiliza Inteligência Artificial para prever o risco de obesidade com base em hábitos de vida e características físicas. Diferente de calculadoras de IMC comuns, este modelo foi desenvolvido para identificar padrões comportamentais e riscos futuros, funcionando como uma ferramenta preventiva de saúde.

## 🚀 Acesse o App
O projeto está em produção e pode ser testado através do link abaixo:
👉 **[Calculadora de Risco - Streamlit Cloud](https://avaliador-risco-obesidade.streamlit.app/)**

---

## 🛠️ Diferenciais do Projeto
- **Análise What-If (Simulação):** O app permite que o usuário altere variáveis (como trocar o carro pela caminhada ou ajustar o consumo de água) para ver em tempo real como o risco de saúde é impactado.
- **Engenharia de Variáveis:** O modelo foi ajustado para tratar inconsistências comuns em auto-relatos (como a frequência de "beliscos" entre refeições), garantindo uma lógica biológica mais precisa.
- **Foco Preditivo:** Ao remover o viés direto do peso atual em certas etapas, o modelo foca em como o estilo de vida atual reflete a saúde futura.

## 📊 O Modelo de IA
O coração deste projeto é um modelo de **Random Forest**, escolhido pela sua excelente performance em dados tabulares.
- **Tratamento de Dados:** Uma lógica binária foi implementada para hábitos alimentares, eliminando distorções estatísticas.
- **Scores Personalizados:** Métricas de "Score de Risco" e "Score Protetor" que ponderam hábitos negativos (fumo, sedentarismo) contra hábitos positivos (consumo de vegetais, atividade física).
- **Interface Intuitiva:** Desenvolvido com Streamlit para ser acessível tanto para desenvolvedores quanto para o público leigo.

## 📂 Estrutura do Repositório
- `app_obesidade.py`: Código principal da interface Streamlit.
- `utils.py`: Funções de processamento, engenharia de variáveis e limpeza de dados.
- `.streamlit/config.toml`: Configuração da paleta de cores e tema visual do app.
- `modelo/`: Diretório contendo o modelo treinado em formato `.joblib`.
- `requirements.txt`: Lista de bibliotecas necessárias para rodar o projeto.

## 💻 Como rodar este projeto localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/maiisaf/tech_challenge4.git](https://github.com/maiisaf/tech_challenge4.git)
