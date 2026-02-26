import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler

# --- Função de Feature Engineering ---

def feature_eng_trans(df):
    # Garante que não modifica o original
    df = df.copy()
    

    # Mapeamentos Binários Simples
    dic_sim_nao = {'Sim':1, 'Não':0}
    col_sim_nao = ['hist_familiar', 'consumo_alimento_calorico', 'fumante', 'monitoramento_caloria']

    for col in col_sim_nao:
        # Verifica se a coluna existe para evitar erro
        if col in df.columns:
            df[col] = df[col].map(dic_sim_nao).astype(int)

    # Gênero
    dic_genero = {'Mulher':1, 'Homem':0}
    if 'genero' in df.columns:
        df['genero'] = df['genero'].map(dic_genero).astype(int)

    
    df['belisca_entre_refeicoes'] = df['comer_entre_refeicoes'].apply(lambda x: 0 if x == 'Não consome' else 1)

    
    # Transporte ativo
    if 'meio_transporte' in df.columns:
        df['transporte_ativo'] = df['meio_transporte'].isin(['Caminhada', 'Bicicleta']).astype(int)

    # Atividade vs Sedentarismo
    if 'freq_atividade_fisica' in df.columns and 'tempo_disp_eletronico' in df.columns:
        df['atividade_liquida'] = df['freq_atividade_fisica'] - df['tempo_disp_eletronico']
        df['razao_atividade_sed'] = (df['freq_atividade_fisica'] + 1) / (df['tempo_disp_eletronico'] + 1)

    # Scores: risco, protetor e equilíbrio
    dic_consome_vegetais = {'Raramente':0, 'Às vezes':1, 'Sempre':2}
    dic_outras_freq = {'Não consome':0, 'Às vezes':1, 'Frequentemente':2, 'Sempre':3}

    # Variáveis auxiliares para o cálculo (usando get para segurança)
    trans_consome_vegetais = df['consumo_vegetais'].map(dic_consome_vegetais) if 'consumo_vegetais' in df.columns else 0
    trans_consumo_alcool = df['consumo_alcool'].map(dic_outras_freq) if 'consumo_alcool' in df.columns else 0
    
    consumo_calorico = df['consumo_alimento_calorico'] if 'consumo_alimento_calorico' in df.columns else 0
    fumante = df['fumante'] if 'fumante' in df.columns else 0
    freq_ativ = df['freq_atividade_fisica'] if 'freq_atividade_fisica' in df.columns else 0
    consumo_agua = pd.to_numeric(df['consumo_agua_diario'], errors='coerce').fillna(0) if 'consumo_agua_diario' in df.columns else 0
    beliscar = df['belisca_entre_refeicoes'] if 'belisca_entre_refeicoes' in df.columns else 0

    # Cálculos dos Scores
    # Nota: Usamos fillna(0) e astype(float) para garantir operações matemáticas
    df['score_risco'] = (consumo_calorico.astype(float) + 
                         fumante.astype(float) + 
                         pd.Series(beliscar).fillna(0).astype(float) + 
                         pd.Series(trans_consumo_alcool).fillna(0).astype(float))

    df['score_protetor'] = (pd.Series(trans_consome_vegetais).fillna(0).astype(float) + 
                            consumo_agua.astype(float) + 
                            freq_ativ.astype(float))

    df['score_equilibrio'] =  df['score_protetor'] - df['score_risco']

    return df

# --- Classes do Pipeline ---

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.drop(columns=self.columns_to_drop, errors='ignore')

class OrdinalEnconding(BaseEstimator, TransformerMixin):
    def __init__(self, ordinal_columns, categories, unknown_value=-1):
        self.ordinal_columns = ordinal_columns
        self.categories = categories
        self.unknown_value = unknown_value
    def fit(self, X, y=None):
        self.encoder_ = OrdinalEncoder(categories=self.categories, handle_unknown='use_encoded_value', unknown_value=self.unknown_value)
        self.encoder_.fit(X[self.ordinal_columns])
        return self
    def transform(self, X):
        X = X.copy()
        X[self.ordinal_columns] = self.encoder_.transform(X[self.ordinal_columns]).astype(int)
        return X

class OneHotEncoding(BaseEstimator, TransformerMixin):
    def __init__(self, ohe_columns):
        self.ohe_columns = ohe_columns
        try:
            self.ohe_ = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        except TypeError:
            self.ohe_ = OneHotEncoder(handle_unknown='ignore', sparse=False)
    def fit(self, X, y=None):
        self.ohe_.fit(X[self.ohe_columns])
        self.feature_names_ = self.ohe_.get_feature_names_out(self.ohe_columns)
        return self
    def transform(self, X):
        X = X.copy()
        ohe_array = self.ohe_.transform(X[self.ohe_columns])
        # Ajuste para garantir índices alinhados
        ohe_df = pd.DataFrame(ohe_array, columns=self.feature_names_, index=X.index)
        X = X.drop(columns=self.ohe_columns)
        X = pd.concat([ohe_df, X], axis=1)
        return X

class MinMax(BaseEstimator, TransformerMixin):
    def __init__(self, cols_to_scale):
        self.cols_to_scale = cols_to_scale
    def fit(self, X, y=None):
        self.scaler_ = MinMaxScaler()
        self.scaler_.fit(X[self.cols_to_scale])
        return self
    def transform(self, X):
        X = X.copy()
        X[self.cols_to_scale] = self.scaler_.transform(X[self.cols_to_scale])
        return X
