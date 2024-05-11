import tkinter as tk
from datetime import datetime
from tkinter import ttk
import pandas as pd
import pyrebase
import pytz

# Configuração do Firebase
config = {
    "apiKey": "AIzaSyCEQbBuB7PbpfEWifNVJKxKqPOC55PkKCQ",
    "authDomain": "aps-5-semestre.firebaseapp.com",
    "databaseURL": "https://aps-5-semestre-default-rtdb.firebaseio.com",
    "storageBucket": "aps-5-semestre.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


# Função para obter dados do Firebase e transformá-los em um DataFrame
def get_data():
    data = db.child("processed_data").get()
    df = pd.DataFrame(data.val())

    # Reordena as colunas
    df = df.reindex(columns=['Circuito', 'pH', 'Solids', 'Conductivity', 'Turbidity', 'Predicted_Potability'])

    return df


# Função para preencher a tabela com dados
def fill_table(df):
    # Limpa a tabela antes de inserir novos dados
    for row in table.get_children():
        table.delete(row)

    # Insere os novos dados
    for i in range(len(df)):
        table.insert('', 'end', values=tuple(df.iloc[i, :]))


def schedule_fill_table():
    # Obter a hora atual no fuso horário de Brasília
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))

    # Se a hora atual for um múltiplo de 5 minutos, execute o preenchimento da tabela
    if now.minute % 5 == 0:
        fill_table(get_data())
        print("Dados re-carregados com sucesso!")

    # Agendar a próxima chamada desta função para daqui a 1 minuto (60000 milissegundos)
    root.after(60000, schedule_fill_table)


# Criação da janela principal
root = tk.Tk()
root.title("Firebase Data Viewer")
root.configure(background='#282a36')

# Criação da tabela
table = ttk.Treeview(root, show='headings')
table["columns"] = ("Circuito", "pH", "Solidos", "Condutividade", "Turbidez", "Potabilidade")
for col in table["columns"]:
    table.heading(col, text=col)
    table.column(col, stretch=tk.YES)

# Incia a tabela com os dados na tela
fill_table(get_data())

# Botão para carregar dados
load_button = tk.Button(root, text="Load Data", command=lambda: fill_table(get_data()))

# Layout
load_button.pack()
table.pack()

schedule_fill_table()

root.mainloop()
