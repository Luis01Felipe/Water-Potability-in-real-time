import pandas as pd
import tf
import numpy as np
from tensorflow.keras.models import load_model

# Carregar os dados
df = pd.read_csv('data.csv', delimiter=';')

# Remover a coluna "Unnamed: 9"
df = df.drop(columns=['Unnamed: 9'])

# Pré-processamento dos dados
# Substitua os valores ausentes pela média da coluna
df = df.apply(pd.to_numeric, errors='coerce')
df = df.fillna(df.mean())

# Carregar o modelo treinado
model = load_model('modelo_agua-0.6890-RMSprop.h5')

# Preparar os dados para a previsão
X = df[['pH', 'Solids', 'Conductivity', 'Turbidity']]

# Preencher os valores NaN com a média da coluna
X = X.fillna(X.mean())

# Fazer previsões
predictions = model.predict(X)

# Select the first column of the predictions
predictions = predictions[:, 0]

if np.isnan(predictions).any():
    predictions = np.nan_to_num(predictions)


# Adicionar as previsões como uma nova coluna no DataFrame
df['Potabilidade_Prevista'] = predictions

# Exportar o DataFrame como um novo arquivo JSON
df.to_csv('water_potability_predicted.csv', index=False)

# Enviar essa budega pro firebase