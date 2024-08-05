from django.urls import path, include
from rest_framework import routers
from api.views import *

# Definimos un enrutador
router = routers.DefaultRouter()

# Registro de las rutas para las vistas
router.register(r'programas', ProgramaViewSet, basename='programas')
router.register(r'competencias', CompetenciaViewSet, basename='competencias')
router.register(r'resultado_aprendizaje',
                ResultadoAprendizajeViewSet, basename='resultado_aprendizaje')
router.register(r'fichas', FichaViewSet, basename='fichas')
router.register(r'trimestres', TrimestreViewSet, basename='trimestres')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'planeacion_pedagogica',
                PlaneacionPedagogicaViewSet, basename='planeacion_pedagogica')
router.register(r'aulas', AulaViewSet, basename='aulas')
router.register(r'horarios', HorarioViewSet, basename='horarios')

# Definimos las URLs tanto de la API como del envío de correos
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas definidas en el router de la API
    path('send-email/', send_email, name='send-email'),  # Ruta para la vista de envío de correos electrónicos
]

urlpatterns += router.urls  # Añade las rutas del router al conjunto de URLs de la aplicación

