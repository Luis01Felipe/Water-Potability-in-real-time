import numpy as np
import schedule
import time
import pytz
from datetime import datetime
import pandas as pd
from tensorflow.keras.models import load_model
import pyrebase
import os
import re

model_dir = '../MachineLearning/Modelos/'

# Lista todos os arquivos no diretório
model_files = os.listdir(model_dir)

# Inicializa a precisão máxima e o nome do modelo correspondente
max_accuracy = 0
max_accuracy_model = ''

config = {
    "apiKey": "AIzaSyCEQbBuB7PbpfEWifNVJKxKqPOC55PkKCQ",
    "authDomain": "aps-5-semestre.firebaseapp.com",
    "databaseURL": "https://aps-5-semestre-default-rtdb.firebaseio.com",
    "storageBucket": "aps-5-semestre.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def send_to_firebase(df):
    # Converte o DataFrame pra um dictionario com a orientação na forma de index
    data_dict = df.to_dict(orient='index')

    # Adiciona 1 ao index para facilitar na interpretação dos dados
    # TODO: Ver se isso realmente é necessario
    # data_dict = {int(key) + 1: value for key, value in data_dict.items()}

    db.child("processed_data").set(data_dict)

    print("dados enviados para o firebase")


def recieve_from_firebase():
    data = db.child("data_to_process").get()
    return pd.DataFrame(data.val())


def job():
    global max_accuracy
    global max_accuracy_model

    # Carrega os dados do firebase
    df = recieve_from_firebase()

    # Armazena a coluna "circuito" em uma variável separada
    circuito = df['Circuito']

    # Remove a coluna "circuito" do DataFrame para a análise
    df = df.drop(columns=['Circuito'])

    # Pré-processamento dos dados
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(df.mean())

    # Percorre todos os arquivos no diretório
    for model_file in model_files:
        # Usa uma expressão regular para extrair a precisão do nome do arquivo
        match = re.search(r'modelo_agua-(\d+\.\d+)-', model_file)
        if match:
            # Converte a precisão para float e verifica se é a maior encontrada até agora
            accuracy = float(match.group(1))
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                max_accuracy_model = model_file

    # Carrega o modelo com a maior precisão
    model = load_model(model_dir + max_accuracy_model)

    # Prepara os dados para a previsão
    entrada = df.iloc[:, :4]

    # Faz as  previsões
    predictions = model.predict(entrada)

    print(predictions.tolist())

    # Arredonda as previsões para 0 ou 1, pois a água não pode ser meio potavel
    predictions_rounded = np.round(predictions)

    # Adiciona as previsões como uma nova coluna no DataFrame
    df['Predicted_Potability'] = predictions_rounded

    # Adiciona a coluna "circuito" de volta ao DataFrame
    df['Circuito'] = circuito

    # Manda pro Firebase RealTime database os dados presentes no JSON
    send_to_firebase(df)

    print("Previsões salvas com sucesso!")


def run_job():
    # Obter a hora atual no fuso horário de Brasília
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    print("Aguardando o próximo trabalho...")

    # Se a hora atual for um múltiplo de 5 minutos, execute o job
    if now.minute % 5 == 0:
        job()


# ------------------------------------------------------ #
# Main do programa

job()

# Checa a cada 1 minuto para poder atualizar a data processada
schedule.every(1).minutes.do(run_job)

while True:
    schedule.run_pending()
    time.sleep(1)
