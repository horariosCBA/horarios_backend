import json
from django.http import BadHeaderError, JsonResponse
from rest_framework import viewsets

from horarios_cba.settings import EMAIL_HOST_USER
from api.models import *
from api.serializers import *
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

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
            data = json.loads(request.body)  # Intenta cargar los datos JSON del cuerpo de la solicitud
            subject = data.get("subject", "")  # Obtiene el asunto del correo
            message = data.get("message", "")  # Obtiene el mensaje del correo
            from_email = EMAIL_HOST_USER  # Dirección de correo del remitente
            recipient_list = data.get("recipient_list", "")  # Lista de destinatarios

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
                return JsonResponse({"error": "Por favor, complete todos los campos"}, status=400)  # Error si faltan campos
        except json.JSONDecodeError:  # Captura errores en la decodificación del JSON
            return JsonResponse({"error": "Error al procesar la solicitud JSON"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)  # Error si el método no es POST