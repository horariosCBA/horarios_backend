import json
from django.http import BadHeaderError, JsonResponse
from rest_framework import viewsets

from horarios_cba.settings import EMAIL_HOST_USER
from api.models import *
from api.serializers import *
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

import random
import torch
from .nltk_utils import tokenize, bag_of_words
from api.chatbot_models import NeuralNet

# Create your views here.

'''
Las vistas (views) en Django sirven para manejar las solicitudes del usuario y devolver las respuestas adecuadas. 
Pueden procesar datos, interactuar con modelos y renderizar plantillas para generar páginas web o enviar datos 
a través de una API.
'''

# Vista de programa


class ProgramaViewSet(viewsets.ModelViewSet):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer


# Vista de competencia
class CompetenciaViewSet(viewsets.ModelViewSet):
    queryset = Competencia.objects.all()
    serializer_class = CompetenciaSerializer


# Vista de resultado de aprendizaje
class ResultadoAprendizajeViewSet(viewsets.ModelViewSet):
    queryset = ResultadoAprendizaje.objects.all()
    serializer_class = ResultadoAprendizajeSerializer


# Vista de planeacion
class PlaneacionViewSet(viewsets.ModelViewSet):
    queryset = Planeacion.objects.all()
    serializer_class = PlaneacionSerializer


# Vista de tematica
class TematicaViewSet(viewsets.ModelViewSet):
    queryset = Tematica.objects.all()
    serializer_class = TematicaSerializer


# Vista de producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# Vista de ficha
class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer


# Vista de trimestre
class TrimestreViewSet(viewsets.ModelViewSet):
    queryset = Trimestre.objects.all()
    serializer_class = TrimestreSerializer


# Vista de usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


# Vista de programacion
class ProgramacionViewSet(viewsets.ModelViewSet):
    queryset = Programacion.objects.all()
    serializer_class = ProgramacionSerializer


# Vista de aula
class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer


# Vista de horario
class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer


# Vista de mensaje
class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer


# Vista de InscripcionAprendiz
class InscripcionAprendizViewSet(viewsets.ModelViewSet):
    queryset = InscripcionAprendiz.objects.all()
    serializer_class = InscripcionAprendizSerializer


# Vista de AsignacionCoordinador
class AsignacionCoordinadorViewSet(viewsets.ModelViewSet):
    queryset = AsignacionCoordinador.objects.all()
    serializer_class = AsignacionCoordinadorSerializer


# Vista de AsignacionInstructor
class AsignacionInstructorViewSet(viewsets.ModelViewSet):
    queryset = AsignacionInstructor.objects.all()
    serializer_class = AsignacionInstructorSerializer


# Vista de AsignacionAula
class AsignacionAulaViewSet(viewsets.ModelViewSet):
    queryset = AsignacionAula.objects.all()
    serializer_class = AsignacionAulaSerializer


# Vista de LiderFicha
class LiderFichaViewSet(viewsets.ModelViewSet):
    queryset = LiderFicha.objects.all()
    serializer_class = LiderFichaSerializer


# Vista para enviar correo electrónico a un destinatario con la finalidad de hacer autenticación de código y
# tengo planeado enviar un correo al administrador para que asigne los roles a los usuarios nuevos.
@csrf_exempt  # Exenta esta vista de la verificación CSRF
def send_code(request):
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST
        try:
            # Intenta cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            subject = data.get("subject", "")  # Obtiene el asunto del correo
            message = data.get("message", "")  # Obtiene el mensaje del correo
            from_email = EMAIL_HOST_USER  # Dirección de correo del remitente
            # Lista de destinatarios
            recipient_list = data.get("recipient_list", "")

            # Verifica que todos los campos requeridos estén presentes
            if subject and message and from_email and recipient_list:
                try:
                    # Renderiza la plantilla HTML con el contexto
                    html_message = render_to_string('code.html', {
                        'subject': subject,
                        'message': message,
                    })

                    # Prepara el mensaje de correo
                    email = EmailMessage(
                        subject,
                        html_message,
                        from_email,
                        recipient_list.split(),  # Convierte la lista de destinatarios a una lista de Python
                        connection=get_connection()  # Obtiene la conexión de correo
                    )
                    email.content_subtype = 'html'  # Define el tipo de contenido como HTML
                    email.send()  # Envía el correo electrónico
                    return JsonResponse({"message": "Correo electrónico enviado exitosamente"}, status=200)
                except BadHeaderError:  # Captura errores relacionados con cabeceras de correo inválidas
                    return JsonResponse({"error": "Error al enviar correo electrónico"}, status=400)
            else:
                # Error si faltan campos
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)
        except json.JSONDecodeError:  # Captura errores en la decodificación del JSON
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
    else:
        # Error si el método no es POST
        return JsonResponse({"error": "Método no permitido"}, status=405)


# Seleccionar el dispositivo (GPU si está disponible, de lo contrario CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Cargar el archivo de intents (intenciones) en formato JSON que contiene patrones y respuestas para el chatbot
with open('api\intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Cargar el modelo previamente entrenado desde un archivo .pth
FILE = "data.pth"
data = torch.load(FILE)

# Extraer información del modelo entrenado, como tamaño de entrada, tamaño oculto y tamaño de salida
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']  # Lista de todas las palabras tokenizadas
tags = data['tags']  # Lista de todas las etiquetas o intenciones
model_state = data["model_state"]  # Estado del modelo (parámetros entrenados)

# Crear una instancia del modelo con la arquitectura cargada y enviarla al dispositivo (CPU o GPU)
model = NeuralNet(input_size, hidden_size, output_size).to(device)
# Cargar el estado del modelo con los pesos entrenados
model.load_state_dict(model_state)
# Poner el modelo en modo de evaluación, desactivando algunas capas como Dropout
model.eval()

# Decorador para permitir solicitudes POST sin requerir un token CSRF


@csrf_exempt
def chatbot_response(request):
    # Verificar si la solicitud es de tipo POST
    if request.method == 'POST':
        # Obtener el mensaje del usuario desde el cuerpo de la solicitud
        user_input = json.loads(request.body).get('message')
        # Si no hay mensaje, devolver una respuesta indicando que no se entiende
        if not user_input:
            return JsonResponse({'response': "No entiendo..."})

        # Tokenizar el mensaje del usuario
        sentence = tokenize(user_input)
        # Convertir la oración tokenizada en una bolsa de palabras (vector de características)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])  # Cambiar la forma para que sea una fila
        # Convertir la matriz a tensor y enviarla al dispositivo
        X = torch.from_numpy(X).to(device)

        # Hacer una predicción con el modelo
        output = model(X)
        # Obtener el índice de la clase predicha con mayor probabilidad
        _, predicted = torch.max(output, dim=1)

        # Obtener el tag correspondiente a la predicción
        tag = tags[predicted.item()]

        # Calcular las probabilidades para todas las clases
        probs = torch.softmax(output, dim=1)
        # Obtener la probabilidad de la clase predicha
        prob = probs[0][predicted.item()]

        # Si la probabilidad de la predicción es mayor al 75%, devolver una respuesta apropiada
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    # Responder con una respuesta aleatoria del conjunto de respuestas para esa intención
                    return JsonResponse({'response': random.choice(intent['responses'])})
        else:
            # Si la probabilidad es baja, indicar que no se entiende el mensaje
            return JsonResponse({'response': "No entiendo..."})
