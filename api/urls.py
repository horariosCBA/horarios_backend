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
router.register(r'planeaciones', PlaneacionViewSet, basename='planeaciones')
router.register(r'tematicas', TematicaViewSet, basename='tematicas')
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'fichas', FichaViewSet, basename='fichas')
router.register(r'trimestres', TrimestreViewSet, basename='trimestres')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'programaciones', ProgramacionViewSet, basename='programaciones')
router.register(r'aulas', AulaViewSet, basename='aulas')
router.register(r'horarios', HorarioViewSet, basename='horarios')
router.register(r'mensajes', MensajeViewSet, basename='mensajes')
router.register(r'inscripcion_aprendiz', InscripcionAprendizViewSet, basename='inscripcion_aprendiz')
router.register(r'asignacion_coordinador', AsignacionCoordinadorViewSet, basename='asignacion_coordinador')
router.register(r'asignacion_instructor', AsignacionInstructorViewSet, basename='asignacion_instructor')
router.register(r'asignacion_aula', AsignacionAulaViewSet, basename='asignacion_aula')


# Definimos las URLs tanto de la API como del envío de correos
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas definidas en el router de la API
    path('send_code/', send_code, name='send_code'),  # Ruta para la vista de envío de correos electrónicos
]

urlpatterns += router.urls  # Añade las rutas del router al conjunto de URLs de la aplicación

