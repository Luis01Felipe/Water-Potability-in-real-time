import sys

import schedule
import time
import pytz
from datetime import datetime
import pandas as pd
from tensorflow.keras.models import load_model
import pyrebase

config = {
    "apiKey": "AIzaSyCEQbBuB7PbpfEWifNVJKxKqPOC55PkKCQ",
    "authDomain": "aps-5-semestre.firebaseapp.com",
    "databaseURL": "https://aps-5-semestre-default-rtdb.firebaseio.com",
    "storageBucket": "aps-5-semestre.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def send_to_firebase(df):
    # Converte o DataFrame pra um dictionario
    data_dict = df.to_dict(orient='index')

    # Cria um novo dicionario com a orientação na forma de index
    data_dict = df.to_dict(orient='index')

    # Adiciona 1 ao index para facilitar na interpretação dos dados
    data_dict = {int(key) + 1: value for key, value in data_dict.items()}

    result = db.child("data").set(data_dict)

    print("dados enviados para o firebase")


def recieve_from_firebase():
    data = db.child("toProcess").get()
    return pd.DataFrame(data.val())


def job():
    # Carrega os dados
    # df = pd.read_json('../Dados/water_monitoring.json')
    df = recieve_from_firebase()

    # Armazena a coluna "circuito" em uma variável separada
    circuito = df['Circuito']

    # Remove a coluna "circuito" do DataFrame para a análise
    df = df.drop(columns=['Circuito'])

    # Pré-processamento dos dados
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(df.mean())

    # Carrega o modelo treinado
    model = load_model('../MachineLearning/Modelos/modelo_agua-0.6386-RMSprop.h5')

    # Prepara os dados para a previsão
    entrada = df.iloc[:, :4]

    # Faz as  previsões
    predictions = model.predict(entrada)

    print(predictions.tolist())
    
    # Adiciona as previsões como uma nova coluna no DataFrame
    df['Predicted_Potability'] = predictions.tolist()

    # Adiciona a coluna "circuito" de volta ao DataFrame
    df['Circuito'] = circuito

    # Exporta o DataFrame como um novo arquivo JSON
    df.to_json('../Dados/water_monitoring_prediction.json', orient='records')

    print("Previsões salvas com sucesso!")

    # Manda pro Firebase RealTime database os dados presentes no JSON
    send_to_firebase(df)


def run_job():
    # Obter a hora atual no fuso horário de Brasília
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    print("Aguardando o próximo job...")

    # Se a hora atual for um múltiplo de 5 minutos, execute o job
    if now.minute % 5 == 0:
        job()


# ------------------------------------------------------ #
# Main do programa

job()

# Checa a cada 1 minuto para poder atualizar o arquivo JSON
schedule.every(1).minutes.do(run_job)

while True:
    schedule.run_pending()
    time.sleep(1)
