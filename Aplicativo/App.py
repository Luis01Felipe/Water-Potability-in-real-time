import tkinter as tk
from datetime import datetime
from tkinter import ttk
import pandas as pd
import pyrebase
import pytz
import pyperclip

# Configuração do Firebase
config = {
    "apiKey": "AIzaSyCEQbBuB7PbpfEWifNVJKxKqPOC55PkKCQ",
    "authDomain": "aps-5-semestre.firebaseapp.com",
    "databaseURL": "https://aps-5-semestre-default-rtdb.firebaseio.com",
    "storageBucket": "aps-5-semestre.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


# ----- Funções -----
# ----- Funções do Firebase
# Obtem  dados do Firebase e transformá-os em um DataFrame
def get_data():
    data = db.child("processed_data").get()
    df = pd.DataFrame(data.val())
    df = df.reindex(columns=['Circuito', 'pH', 'Solids', 'Conductivity', 'Turbidity', 'Predicted_Potability'])
    sort_label_text.set("Dados carregados com sucesso!")
    return df


# -----


# Ordena os dados
def sort_data(column):
    df = get_data()
    if column in df.columns:  # Check if the column exists in the DataFrame
        df = df.dropna(subset=[column])  # Drop rows with NaN values in the sorting column
        descending = sort_order.get(column, False)
        df.sort_values(by=column, ascending=not descending, inplace=True)
        fill_table(df)

        # Alterna o estado de ordenação da coluna
        sort_order[column] = not descending

        # Atualiza o texto da label
        order = "maior" if descending else "menor"
        sort_label_text.set(f"A coluna {column} está sendo ordenada por {order}")


# Cria uma ordenação para uma coluna específica
def create_sort_function(column):
    return lambda: sort_data(column)


# Preenche a tabela com dados
def fill_table(df):
    # Limpa a tabela antes de inserir novos dados
    for row in table.get_children():
        table.delete(row)

    # Insere os novos dados
    for i in range(len(df)):
        table.insert('', 'end', values=tuple(df.iloc[i, :]))


# Copia uma linha para a área de transferência
def copy_row(event):
    selected_items = table.selection()
    if selected_items:  # Check if there's a selection
        selected_item = selected_items[0]
        values = table.item(selected_item, "values")
        pyperclip.copy('\t'.join(values))


# Carrega os dados do Firebase e preenche a tabela
def load_data():
    fill_table(get_data())
    sort_label_text.set("Dados carregados com sucesso!")


# Verifica a cada 5 minutos + 1 se os dados precisam ser recarregados
def schedule_fill_table():
    # Obter a hora atual no fuso horário de Brasília
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))

    # Se a hora atual for um múltiplo de 5 minutos, execute o preenchimento da tabela
    if now.minute % 5 == 0:
        # Agurda 1 minuto antes de carregar os dados novamente, para garantir uma melhor sincronização
        root.after(60000, load_data)
        sort_label_text.set("Dados re-carregados com sucesso!")

    # Agendar a próxima chamada desta função para daqui a 1 minuto (60000 milissegundos)
    root.after(60000, schedule_fill_table)


# ----- Interface Gráfica -----
# Janela Principal
root = tk.Tk()
root.title("Firebase Data Viewer")
root.configure(background='#282a36')

# Criação da tabela
table = ttk.Treeview(root, show='headings')
table["columns"] = ("Circuito", "pH", "Solids", "Conductivity", "Turbidity", "Potabilidade")
for col in table["columns"]:
    table.heading(col, text=col, command=create_sort_function(col))
    table.column(col, stretch=tk.YES)

# Adiciona o evento de duplo clique à tabela
table.bind("<Double-1>", copy_row)

# Dicionário para armazenar o estado de ordenação de cada coluna
sort_order = {}

# Armazena o texto da label
sort_label_text = tk.StringVar()

# ----- Main -----
# Inicia a tabela com os dados na tela
load_data()

# Botão e Label para carregar e exibir os dados
load_button = tk.Button(root, text="Load Data", command=lambda: load_data())
sort_label = tk.Label(root, textvariable=sort_label_text)

# Layout
load_button.pack()
sort_label.pack()
table.pack()

# Inicia o loop principal da interface gráfica
schedule_fill_table()

root.mainloop()
