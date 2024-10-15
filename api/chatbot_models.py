import torch
import torch.nn as nn  # Módulo de redes neuronales de PyTorch

# Definir la clase NeuralNet, que hereda de nn.Module para crear una red neuronal personalizada


class NeuralNet(nn.Module):
    # El constructor de la clase toma tres parámetros: tamaño de entrada (input_size), tamaño de la capa oculta (hidden_size), y número de clases de salida (num_classes)
    def __init__(self, input_size, hidden_size, num_classes):
        # Llamada al constructor de la clase padre (nn.Module)
        super(NeuralNet, self).__init__()
        # Definir la primera capa totalmente conectada (input_size -> hidden_size)
        self.l1 = nn.Linear(input_size, hidden_size)
        # Definir la segunda capa totalmente conectada (hidden_size -> hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        # Definir la tercera capa totalmente conectada (hidden_size -> num_classes)
        self.l3 = nn.Linear(hidden_size, num_classes)
        # Definir la función de activación ReLU (Rectified Linear Unit), que introduce no linealidad en el modelo
        self.relu = nn.ReLU()

    # Definir el método forward, que especifica cómo los datos pasan a través de la red
    def forward(self, x):
        # Pasar los datos por la primera capa y aplicar la activación ReLU
        out = self.l1(x)
        out = self.relu(out)
        # Pasar los datos por la segunda capa y aplicar nuevamente ReLU
        out = self.l2(out)
        out = self.relu(out)
        # Pasar los datos por la tercera capa (no se aplica activación después de esta capa)
        out = self.l3(out)
        # Devolver la salida
        return out
