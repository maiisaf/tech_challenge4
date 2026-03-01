# Calculadora de Risco de Saúde e Obesidade com IA

Este projeto utiliza Inteligência Artificial para prever o risco de obesidade com base em hábitos de vida e características físicas. Diferente de calculadoras de IMC comuns, este modelo foi desenvolvido para identificar padrões comportamentais e riscos futuros, funcionando como uma ferramenta preventiva de saúde.

## 🚀 Acesse o App
O projeto está em produção e pode ser testado através do link abaixo:
👉 **[Calculadora de Risco - Streamlit Cloud](https://avaliador-risco-obesidade.streamlit.app/)**

Painel analítico pode ser acessado **[clicando aqui](https://dashboard-acompanhamento-obesidade.streamlit.app)**

---

## 🛠️ Diferenciais do Projeto
* **Mitigação de Viés (Bias Reduction):** Para evitar que o modelo se tornasse "preguiçoso" e dependente apenas de genética, removou-se variáveis determinísticas (como histórico familiar e idade) do treinamento direto. Isso forçou a IA a priorizar **fatores modificáveis** (hábitos).
* **Análise What-If (Simulação):** O app permite que o usuário altere variáveis em tempo real (ex: trocar o carro pela caminhada ou ajustar o consumo de água) para visualizar o impacto imediato no seu perfil de risco.
* **Engenharia de Variáveis Avançada:** * **Scores de Comportamento:** Criou-se métricas compostas que ponderam hábitos negativos (fumo, sedentarismo) contra positivos (vegetais, água).
    * **Sedentarismo Risco:** Uma variável de interação que cruza o IMC elevado com a falta de atividade física, criando um sinal de alerta muito mais preciso que o IMC isolado.

## 📊 O Modelo de IA
O modelo escolhido foi o **XGBoost (Extreme Gradient Boosting)**, o algoritmo "estado da arte" para dados tabulares, superando modelos tradicionais como Random Forest e Regressão Logística.

* **Foco em Segurança (Recall):** Alcançou-se um **Recall de 92% para a classe de risco**, garantindo que a ferramenta minimize "Falsos Negativos" (não ignorar quem realmente precisa de atenção).
* **Robustez e Generalização:** * **Acurácia Treino:** 91,78%
    * **Acurácia Teste:** 88,00%
    * A proximidade entre os resultados prova que o modelo é estável e não sofre de *overfitting*.
* **Pipeline de Produção:** Utilização de `ColumnTransformer` e `Pipeline` para garantir que o pré-processamento de dados seja idêntico no ambiente de desenvolvimento e no servidor.



---
- `app_obesidade.py`: Código principal da interface Streamlit.
- `utils.py`: Funções de processamento, engenharia de variáveis e limpeza de dados.
- `.streamlit/config.toml`: Configuração da paleta de cores e tema visual do app.
- `modelo/`: Diretório contendo o modelo treinado em formato `.joblib`.
- `requirements.txt`: Lista de bibliotecas necessárias para rodar o projeto.

## 💻 Como rodar este projeto localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/maiisaf/tech_challenge4.git](https://github.com/maiisaf/tech_challenge4.git)
