import json
# Funciones personalizadas para procesar texto
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn  # Módulo para definir redes neuronales
# Clases para manejar datasets y loaders
from torch.utils.data import Dataset, DataLoader

# Importar el modelo de red neuronal del chatbot
from chatbot_models import NeuralNet

# Abrir y cargar el archivo JSON que contiene las intenciones y sus patrones
with open('api\intents.json', encoding='utf-8') as f:
    intents = json.loads(f.read())

# Listas para almacenar todas las palabras y etiquetas
all_words = []
tags = []
xy = []  # Lista que almacena las parejas (patrón, etiqueta)

# Recorrer cada intención en el archivo de intents
for intent in intents["intents"]:
    tag = intent["tag"]  # Obtener la etiqueta (intención)
    tags.append(tag)  # Almacenar la etiqueta

    # Tokenizar cada patrón en la lista de patrones de la intención
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        # Añadir las palabras tokenizadas a la lista de todas las palabras
        all_words.extend(w)
        xy.append((w, tag))  # Añadir la pareja (palabras, etiqueta) a xy

# Definir palabras a ignorar
ignore_words = ["?", "!", ".", ","]
# Aplicar stemming y eliminar palabras ignoradas, además de eliminar duplicados y ordenar
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Preparar los datos de entrenamiento
X_train = []  # Características (bolsa de palabras)
y_train = []  # Etiquetas (índice de las tags)

# Convertir las palabras de los patrones en una bolsa de palabras y asociarlas con sus etiquetas
for (pattern_sentence, tag) in xy:
    # Convertir la oración en bolsa de palabras
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    label = tags.index(tag)  # Etiquetar la oración con el índice de su tag
    y_train.append(label)

X_train = np.array(X_train)  # Convertir a matriz numpy
y_train = np.array(y_train)

# Definir la clase para manejar el dataset de entrenamiento


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train  # Características (bolsa de palabras)
        self.y_data = y_train  # Etiquetas

    # Método para obtener un ejemplo individual del dataset
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # Método para obtener el tamaño del dataset
    def __len__(self):
        return self.n_samples


# Definir los parámetros para el entrenamiento
batch_size = 8
hidden_size = 8
output_size = len(tags)  # Número de etiquetas (salidas)
# Número de entradas (tamaño de la bolsa de palabras)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 1000  # Número de épocas de entrenamiento

# Crear el dataset y el DataLoader para manejar lotes de datos durante el entrenamiento
dataset = ChatDataset()
train_loader = DataLoader(
    dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# Configurar el dispositivo (usar GPU si está disponible, de lo contrario CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Crear el modelo de red neuronal y moverlo al dispositivo (CPU/GPU)
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Definir la función de pérdida (Cross Entropy Loss) y el optimizador (Adam)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Ciclo de entrenamiento del modelo
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)  # Mover las características al dispositivo
        labels = labels.to(device)  # Mover las etiquetas al dispositivo

        outputs = model(words)  # Pasar los datos a través del modelo
        loss = criterion(outputs, labels)  # Calcular la pérdida

        optimizer.zero_grad()  # Limpiar los gradientes
        loss.backward()  # Propagación hacia atrás
        optimizer.step()  # Actualizar los parámetros del modelo

    # Imprimir la pérdida cada 100 épocas
    if (epoch + 1) % 100 == 0:
        print(f"epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}")

# Imprimir la pérdida final después del entrenamiento
print(f"final loss, loss={loss.item():.4f}")

# Guardar el modelo y los datos relevantes en un archivo
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags,
}

# Guardar los datos en un archivo .pth
FILE = "data.pth"
torch.save(data, FILE)

# Imprimir mensaje de finalización
print(f"training complete. file saved to {FILE}")
