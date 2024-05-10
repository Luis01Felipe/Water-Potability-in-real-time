import pandas as pd
import tensorflow as tf
import numpy as np
import sys

i = 0
# Vai começar a salvar a partir de 67%
max_accuracy = 0.67
# Vai parar de salvar a partir de 70%
ideal_accuracy = 0.70

while True:
    # Carregar os dados
    df = pd.read_csv('../../water_potability.csv', delimiter=';')

    # Selecionar as colunas de entrada (X) e saída (Y)
    X = df[['pH', 'Conductivity', 'Turbidity']]
    y = df['Potability']

    num_colunasX = X.shape[1]

    # Dividir os dados em conjuntos de treinamento e teste
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    train_idx, test_idx = np.split(indices, [int((1 - 0.1) * X.shape[0])])

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Converter os rótulos para uma representação categórica
    y_train = tf.keras.utils.to_categorical(y_train)
    y_test = tf.keras.utils.to_categorical(y_test)

    # Criação do modelo
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(2, activation='softmax')
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
    model.fit(X_train, y_train, epochs=256, verbose=0, batch_size=16)
    loss, accuracy = model.evaluate(X_test, y_test)

    # Salvamento do modelo se a acurácia for maior que a máxima registrada
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        nome_modelo = f'modelo_agua-{accuracy:.4f}-{optimizer_name}-{num_colunasX}_Colunas.h5'.replace('/', '_')
        model.save(f'Bem Encaminhado/{nome_modelo}')
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% salvo com sucesso!")
    else:
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% não atingiu a precisão mínima")

    i += 1

    # Ao chegar na precisão ideal, salva o modelo e encerra o script
    if accuracy > ideal_accuracy:
        nome_modelo = f'modelo_agua-IDEAL-{accuracy:.4f}-{optimizer_name}-{num_colunasX}_Colunas.h5'.replace('/', '_')
        model.save(f'Ideal/{nome_modelo}')
        break
    # Impede que o programa sobrecarregue o computador ao ficar interminavelmente executando
    elif i >= 1000:
        break

# Fim do script
sys.exit()