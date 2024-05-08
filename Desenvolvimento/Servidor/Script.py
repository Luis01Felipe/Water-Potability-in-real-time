# Este script sera executado no servidor, ele deve receber os dados e então passa-los para o modelo treinado,
# retornando a resposta para o cliente, por fim ira converter o json/csv para sql

import pandas as pd
import tf
import numpy as np
from tensorflow.keras.models import load_model

# Carregar os dados
df = pd.read_json('../Dados/data.json')

# Armazenar a coluna "circuito" em uma variável separada
circuito = df['Circuito']

# Remover a coluna "circuito" do DataFrame para a análise
df = df.drop(columns=['Circuito'])

# Pré-processamento dos dados
# Substitua os valores ausentes pela média da coluna
df = df.apply(pd.to_numeric, errors='coerce')
df = df.fillna(df.mean())

# Carregar o modelo treinado
model = load_model('modelo_agua-0.6890-RMSprop-4_Colunas.h5')

# Preparar os dados para a previsão
X = df.iloc[:, :4]

# Fazer previsões
predictions = model.predict(X)

if np.isnan(predictions).any():
    predictions = np.nan_to_num(predictions)

# Select the first column of the predictions
predictions = predictions[:, 0]

# Adicionar as previsões como uma nova coluna no DataFrame
df['Predicted_Potability'] = predictions

# Adicionar a coluna "circuito" de volta ao DataFrame
df['Circuito'] = circuito

# Exportar o DataFrame como um novo arquivo JSON
df.to_json('../Dados/water_potability_predicted.json', orient='records')

# Mandar pro Firebase Real database os dados