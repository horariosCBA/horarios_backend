from django.contrib import admin
from api.models import *

# Register your models here.

'''
El admin de Django sirve para proporcionar una interfaz administrativa web que permite gestionar y 
visualizar fácilmente los datos de la aplicación. Con el admin, los usuarios con permisos adecuados pueden crear, 
editar, eliminar y buscar registros en las tablas de la base de datos definidas por los modelos de Django, 
sin necesidad de escribir código SQL. Es una herramienta poderosa para la administración 
de contenido y datos de la aplicación.
'''

admin.site.register(Programa)
admin.site.register(Competencia)
admin.site.register(ResultadoAprendizaje)
admin.site.register(Planeacion)
admin.site.register(Tematica)
admin.site.register(Producto)
admin.site.register(Ficha)
admin.site.register(Trimestre)
admin.site.register(Usuario)
admin.site.register(Programacion)
admin.site.register(Aula)
admin.site.register(Horario)
admin.site.register(Mensaje)
admin.site.register(InscripcionAprendiz)
admin.site.register(AsignacionCoordinador)
admin.site.register(AsignacionInstructor)
admin.site.register(AsignacionAula)
