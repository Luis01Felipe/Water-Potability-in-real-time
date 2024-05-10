import pandas as pd
import tensorflow as tf
import numpy as np
import sys

i = 0
# Vai começar a salvar a partir de 65%
max_accuracy = 0.62
# Vai parar de salvar a partir de 70%
ideal_accuracy = 0.70

# Carregar os dados
df = pd.read_json('../Dados/water_dataset.json')

# Substituir espaços vazios por NaN
df.replace("", np.nan, inplace=True)

# Remover linhas com NaN
df.dropna(inplace=True)

while True:

    # Substitua os valores ausentes pela média da coluna
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(df.mean())

    # Seleciona as colunas de entrada (entrada) e saída (saida)
    entrada = df[['pH', 'Solids', 'Conductivity', 'Turbidity']]
    saida = df['Potability']

    # Dividi os dados em conjuntos de treinamento e teste
    indices = np.arange(entrada.shape[0])
    np.random.shuffle(indices)

    train_idx, test_idx = np.split(indices, [int((1 - 0.1) * entrada.shape[0])])

    entrada_train, entrada_test = entrada.iloc[train_idx], entrada.iloc[test_idx]
    saida_train, saida_test = saida.iloc[train_idx], saida.iloc[test_idx]

    # Criação do modelo
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    optimizer_name = 'RMSprop'
    optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001,
                                            rho=1.0,
                                            momentum=0.0,
                                            centered=False,
                                            name=optimizer_name)

    # Compilação do modelo
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # Treinamento do modelo
    model.fit(entrada_train, saida_train, epochs=256, verbose=0, batch_size=16)
    loss, accuracy = model.evaluate(entrada_test, saida_test)

    # Salva o modelo se a precisão for maior que a máxima registrada
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        nome_modelo = (f'modelo_agua-{accuracy:.4f}-{optimizer_name}.h5'
                       .replace('/', '_'))
        model.save(f'Modelos/{nome_modelo}')
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% salvo com sucesso!")
    # Ao chegar na precisão ideal, salva o modelo e encerra o script
    elif accuracy > ideal_accuracy:
        nome_modelo = (f'modelo_agua-IDEAL-{accuracy:.4f}-{optimizer_name}.h5'
                       .replace('/', '_'))
        model.save(f'Modelos/{nome_modelo}')
        break
    else:
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% não atingiu a precisão mínima")

    i += 1

    # Ao chegar ao fim da contagem, encerra o script independente se atingiu ou não a precisão ideal
    if i >= 1000:
        break

# Fim do script
sys.exit()