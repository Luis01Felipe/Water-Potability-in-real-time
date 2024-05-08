import pandas as pd
import tensorflow as tf
import numpy as np
import sys
import os

tf.get_logger().setLevel('ERROR')

# Contador para o número de modelos treinados
i = 0

# Carregar o modelo com a maior acurácia presente na pasta Professor
files = os.listdir('Professor')
model_files = [file for file in files if file.endswith('.h5')]
max_file = max(model_files, key=lambda file: float(file.split('-')[1]))
model_path = os.path.join('Professor', max_file)
print(f"model_path = {model_path}")

ideal_accuracy = 0.70
print(f"ideal_accuracy = {ideal_accuracy}")

# Extrair o valor de max_accuracy do model_path
max_accuracy = float(model_path.split('-')[1])
print(f"max_accuracy = {max_accuracy}")

# Carregar os dados
df = pd.read_csv('../../water_potability.csv', delimiter=';')

# Selecionar as colunas de entrada (X) e saída (Y)
X = df[['pH', 'Solids', 'Conductivity', 'Turbidity']]
y = df['Potability']

# Loop para treinar modelos até obter algo superior a 70% de acurácia
while True:
    # Carregar o modelo
    model = tf.keras.models.load_model(model_path)

    # Criar uma nova instância do otimizador
    optimizer_name = 'RMSprop'
    optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001,
                                            rho=1.0,
                                            momentum=0.0,
                                            centered=False,
                                            name=optimizer_name)

    # Recompilar o modelo com o novo otimizador
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # Dividir os dados em conjuntos de treinamento e teste
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    train_idx, test_idx = np.split(indices, [int((1 - 0.1) * X.shape[0])])

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Converter os rótulos para uma representação categórica
    y_train = tf.keras.utils.to_categorical(y_train)
    y_test = tf.keras.utils.to_categorical(y_test)

    # Treinamento do modelo
    model.fit(X_train, y_train, epochs=256, verbose=0, batch_size=16)
    loss, accuracy = model.evaluate(X_test, y_test)

    # Salvamento do modelo se a acurácia for maior que a máxima registrada
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        nome_modelo = f'modelo_agua-{accuracy:.4f}-{optimizer_name}.h5'.replace('/', '_')
        model.save(f'Professor/{nome_modelo}')
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% salvo com sucesso!")
        model_path = f'DeepLearning/Professor/{nome_modelo}'
    else:
        print(f"Modelo {i} de precisão {accuracy * 100:.4f}% não atingiu a precisão mínima")

    i += 1

    if accuracy > ideal_accuracy:
        nome_modelo = f'modelo_agua-IDEAL-{accuracy:.4f}-{optimizer_name}.h5'.replace('/', '_')
        model.save(f'Ideal/{nome_modelo}')
        break

# Encerra o programa
sys.exit()