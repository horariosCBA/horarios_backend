from django.db import models
from django.utils import timezone

# Create your models here.

"""
Un modelo en Django sirve para definir la estructura y el comportamiento de los datos en tu aplicación.
Cada modelo representa una tabla en la base de datos, donde los atributos del modelo corresponden a las 
columnas de la tabla. Los modelos permiten crear, leer, actualizar y eliminar registros en la base de 
datos de manera sencilla y coherente con el ORM (Object-Relational Mapping) de Django.
"""

# Modelo programa de formación


class Programa(models.Model):

    # Listas Desplegables

    class TipoPrograma(models.TextChoices):
        TECNICO = "Técnico", ("Técnico")
        TECNOLOGO = "Tecnólogo", ("Tecnólogo")
        ESPECIALIZACION_TECNICA = "Especialización Técnica", (
            "Especialización Técnica")
        ESPECIALIZACION_TECNOLOGICA = "Especialización Tecnológica", (
            "Especialización Tecnológica")
        CURSO_CORTO = "Curso Corto", ("Curso Corto")
        FORMACION_CONTINUA = "Formación Continua", ("Formación Continua")
        CAPACITACION = "Capacitación a Medida", ("Capacitación a Medida")
        CURSO_VIRTUAL = "Curso Virtual", ("Curso Virtual")
        CURSO_IDIOMAS = "Curso de Idiomas", ("Curso de Idiomas")
        EMPRENDIMIENTO = "Emprendimiento", ("Emprendimiento")

    class Certificacion(models.TextChoices):
        TECNICO = "Certificado Técnico", ("Certificado Técnico")
        TECNOLOGO = "Certificado Tecnólogo", ("Certificado Tecnólogo")
        ESPECIALIZACION_TECNICA = "Certificado de Especialización Técnica", (
            "Certificado de Especialización Técnica")
        ESPECIALIZACION_TECNOLOGICA = "Certificado de Especialización Tecnológica", (
            "Certificado de Especialización Tecnológica")
        CURSO_CORTO = "Certificado de Curso Corto", (
            "Certificado de Curso Corto")
        FORMACION_CONTINUA = "Certificado de Formación Continua", (
            "Certificado de Formación Continua")
        CAPACITACION = "Certificado de Capacitación a Medida", (
            "Certificado de Capacitación a Medida")
        CURSO_VIRTUAL = "Certificado de Curso Virtual", (
            "Certificado de Curso Virtual")
        CURSO_IDIOMAS = "Certificado de Idiomas", ("Certificado de Idiomas")
        EMPRENDIMIENTO = "Certificado de Emprendimiento", (
            "Certificado de Emprendimiento")

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=15, null=False, blank=False)
    version = models.IntegerField(null=False, blank=False)
    fechaInicio = models.DateField(null=False, blank=False)
    fechaFin = models.DateField(null=True, blank=True)
    duracionLectiva = models.IntegerField(null=False, blank=False)
    duracionProductiva = models.IntegerField(null=False, blank=False)
    duracionTotal = models.IntegerField(null=False, blank=False)
    tipoPrograma = models.CharField(
        max_length=100, choices=TipoPrograma.choices, default=TipoPrograma.TECNICO, null=False, blank=False
    )
    certificacion = models.CharField(
        max_length=100, choices=Certificacion.choices, default=Certificacion.TECNICO, null=False, blank=False
    )
    descripcion = models.TextField(null=False, blank=False)
    area = models.CharField(max_length=30, null=True, blank=True)


# Modelo Competencia
class Competencia(models.Model):
    id = models.AutoField(primary_key=True)
    norma = models.CharField(max_length=150, null=False, blank=False)
    codigo = models.CharField(max_length=15, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    duracion = models.IntegerField(null=False, blank=False)
    programa = models.ForeignKey(
        Programa, on_delete=models.CASCADE, null=False, blank=False)


# Modelo resultado de aprendizaje relacionado a la competencia
class ResultadoAprendizaje(models.Model):

    # Lista Desplegable
    class Numero(models.TextChoices):
        RAP1 = "Rap. 1", ("Rap. 1")
        RAP2 = "Rap. 2", ("Rap. 2")
        RAP3 = "Rap. 3", ("Rap. 3")
        RAP4 = "Rap. 4", ("Rap. 4")
        RAP5 = "Rap. 5", ("Rap. 5")
        RAP6 = "Rap. 6", ("Rap. 6")
        RAP7 = "Rap. 7", ("Rap. 7")
        RAP8 = "Rap. 8", ("Rap. 8")
        RAP9 = "Rap. 9", ("Rap. 9")
        RAP10 = "Rap. 10", ("Rap. 10")
        RAP11 = "Rap. 11", ("Rap. 11")
        RAP12 = "Rap. 12", ("Rap. 12")
        RAP13 = "Rap. 13", ("Rap. 13")
        RAP14 = "Rap. 14", ("Rap. 14")
        RAP15 = "Rap. 15", ("Rap. 15")

    id = models.AutoField(primary_key=True)
    numero = models.CharField(
        max_length=15, choices=Numero.choices, default=Numero.RAP1, null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)
    competencia = models.ForeignKey(
        Competencia, on_delete=models.CASCADE, null=False, blank=False)


# Modelo Planeacion
class Planeacion(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(default=0, null=False, blank=False)
    duracionPresencial = models.IntegerField(null=True, blank=True)
    duracionVirtual = models.IntegerField(null=True, blank=True)
    duracionTotal = models.IntegerField(null=False, blank=False)
    horasRecomendadas = models.IntegerField(default=2, null=False, blank=False)
    diasRecomendados = models.IntegerField(default=1, null=False, blank=False)
    resultadoAprendizaje = models.ForeignKey(
        ResultadoAprendizaje, on_delete=models.CASCADE, null=False, blank=False
    )


# Modelo Tematica
class Tematica(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(null=False, blank=False)
    planeacion = models.ForeignKey(
        Planeacion, on_delete=models.CASCADE, null=False, blank=False
    )


# Modelo Producto
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(null=False, blank=False)
    planeacion = models.ForeignKey(
        Planeacion, on_delete=models.CASCADE, null=False, blank=False
    )


# Modelo Ficha
class Ficha(models.Model):

    # Listas Desplegables
    class TipoOferta(models.TextChoices):
        OFERTA_ABIERTA = "Oferta Abierta", ("Oferta Abierta")
        COLEGIO = "Colegio", ("Colegio")
        EMPRESA = "Empresa", ("Empresa")
        INSTITUCION = "Institución", ("Institución")
        PROGRAMA_ESPECIAL = "Programa Especial", ("Programa Especial")
        EDUCACION_CONTINUA = "Educación Continua", ("Educación Continua")

    class ModalidadesSENA(models.TextChoices):
        PRESENCIAL = "Presencial", "Presencial"
        VIRTUAL = "Virtual", "Virtual"
        A_DISTANCIA = "A Distancia", "A Distancia"
        MIXTA = "Mixta (B-Learning)", "Mixta (B-Learning)"
        CONTRATO_DE_APRENDIZAJE = "Contrato de Aprendizaje", "Contrato de Aprendizaje"
        ARTICULACION_CON_LA_MEDIA = "Articulación con la Media", "Articulación con la Media"
        ESCUELA_TALLER = "Escuela-Taller", "Escuela-Taller"

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=15, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    fechaInicio = models.DateField(null=False, blank=False)
    fechaFin = models.DateField(null=False, blank=False)
    tipoOferta = models.CharField(
        max_length=100, choices=TipoOferta.choices, default=TipoOferta.OFERTA_ABIERTA, null=False, blank=False
    )
    modalidad = models.CharField(
        max_length=100, choices=ModalidadesSENA.choices, default=ModalidadesSENA.PRESENCIAL, null=False, blank=False
    )
    lugar = models.CharField(max_length=150, null=True, blank=True)
    estado = models.BooleanField(default=True, null=False, blank=False)
    programa = models.ForeignKey(
        Programa, on_delete=models.CASCADE, null=False, blank=False)


# Modelo Trimestre
class Trimestre(models.Model):

    # Lista Desplegable
    class Numero(models.TextChoices):
        T1 = "Trimestre 1", ("Trimestre 1")
        T2 = "Trimestre 2", ("Trimestre 2")
        T3 = "Trimestre 3", ("Trimestre 3")
        T4 = "Trimestre 4", ("Trimestre 4")
        T5 = "Trimestre 5", ("Trimestre 5")
        T6 = "Trimestre 6", ("Trimestre 6")
        T7 = "Trimestre 7", ("Trimestre 7")
        T8 = "Trimestre 8", ("Trimestre 8")

    id = models.AutoField(primary_key=True)
    numero = models.CharField(
        max_length=15, choices=Numero.choices, default=Numero.T1, null=False, blank=False
    )
    fechaInicio = models.DateField(null=False, blank=False)
    fechaFin = models.DateField(null=False, blank=False)
    estado = models.BooleanField(default=True, null=False, blank=False)
    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, null=False, blank=False)


# Modelo Usuario
class Usuario(models.Model):

    # Listas Desplegables
    class TipoDocumento(models.TextChoices):
        TARJETA = "TI", ('Tarjeta de Identidad')
        CEDULA = "CC", ('Cedula de Ciudadanía')
        EXTRANGERA = "CE", ('Cedula de Extranjería')
        PASAPORTE = "PAS", ('Pasaporte')
        NIT = "NIT", ('Número de identificación tributaria')

    class Roles(models.TextChoices):

        INSTRUCTOR = "Instructor", ('Instructor')
        APRENDIZ = "Aprendiz", ('Aprendiz')
        COORDINADOR = "Coordinador", ('Coordinador')
        ADMINISTRADOR = "Administrador", ('Administrador')

    class TipoInstructor(models.TextChoices):

        PLANTA = "Planta", ('Planta')
        CONTRATISTA = "Contratista", ('Contratista')
        

    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50, null=False, blank=False)
    apellidos = models.CharField(max_length=50, null=False, blank=False)
    tipoDocumento = models.CharField(
        max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CEDULA, null=False, blank=False)
    numeroDocumento = models.CharField(
        max_length=15, null=False, blank=False, unique=True)
    correoElectronico = models.EmailField(null=False, blank=False, unique=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    telefonoCelular = models.CharField(max_length=15, null=False, blank=False)
    rol = models.CharField(
        max_length=15, choices=Roles.choices, default=Roles.APRENDIZ, null=True, blank=True)
    cargo = models.CharField(max_length=50, null=True, blank=True)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    foto = models.CharField(max_length=255, null=True, blank=True)
    vocero = models.BooleanField(default=False, null=False, blank=False)
    titulacion = models.CharField(max_length=60, null=True, blank=True)
    estado = models.BooleanField(default=True, null=False, blank=False)
    enLinea = models.BooleanField(default=False, null=False, blank=False)
    tipoInstructor = models.CharField(
        max_length=15, choices=TipoInstructor.choices, default=TipoInstructor.PLANTA, null=True, blank=True
    )
    area = models.CharField(max_length=30, null=True, blank=True)
    fechaRegistro = models.DateField(blank=True, null=True, auto_now_add=True)


# Modelo Programacion
class Programacion(models.Model):
    id = models.AutoField(primary_key=True)
    trimestre = models.IntegerField(null=False, blank=False)
    ficha = models.IntegerField(null=False, blank=False)
    diasAsignados = models.IntegerField(null=False, blank=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=False, blank=False)
    planeacion = models.ForeignKey(
        Planeacion, on_delete=models.CASCADE, null=False, blank=False)


# Modelo Aula
class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    capacidad = models.IntegerField(null=False, blank=False)
    ubicacion = models.CharField(max_length=100, null=False, blank=False)
    estado = models.BooleanField(default=True, null=False, blank=False)


# Modelo Horario
class Horario(models.Model):

    # Lista Desplegable
    class Dia(models.TextChoices):
        LUNES = "Lunes", ("Lunes")
        MARTES = "Martes", ("Martes")
        MIERCOLES = "Miercoles", ("Miercoles")
        JUEVES = "Jueves", ("Jueves")
        VIERNES = "Viernes", ("Viernes")
        SABADO = "Sabado", ("Sabado")
        DOMINGO = "Domingo", ("Domingo")

    id = models.AutoField(primary_key=True)
    dia = models.CharField(
        max_length=15, choices=Dia.choices, default=Dia.LUNES, null=False, blank=False
    )
    horaInicio = models.TimeField(null=False, blank=False)
    horaFin = models.TimeField(null=False, blank=False)
    programacion = models.ForeignKey(
        Programacion, on_delete=models.CASCADE, null=True, blank=True)
    aula = models.ForeignKey(
        Aula, on_delete=models.SET_NULL, null=True, blank=True)


# Modelo Mensaje
class Mensaje(models.Model):
    id = models.AutoField(primary_key=True)
    usuarioReceptor = models.IntegerField(null=False, blank=False)
    usuarioEmisor = models.IntegerField(null=False, blank=False)
    fechaEnviado = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    fechaLeido = models.DateTimeField(null=True, blank=True)
    imagen = models.BooleanField(default=False, null=False, blank=False)
    contenido = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=20, null=True, blank=True)
    eliminarEmisor = models.BooleanField(
        default=False, null=False, blank=False)
    eliminarReceptor = models.BooleanField(
        default=False, null=False, blank=False)


# Modelo InscripcionAprendiz
class InscripcionAprendiz(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.IntegerField(null=False, blank=False)
    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, null=False, blank=False)


# Modelo AsignacionCoordinador
class AsignacionCoordinador(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.IntegerField(null=False, blank=False)
    programa = models.ForeignKey(
        Programa, on_delete=models.CASCADE, null=False, blank=False)


# Modelo AsignacionInstructor
class AsignacionInstructor(models.Model):
    id = models.AutoField(primary_key=True)
    programa = models.IntegerField(null=False, blank=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True, blank=True)


# Modelo AsignacionAula
class AsignacionAula(models.Model):
    id = models.AutoField(primary_key=True)
    programa = models.IntegerField(null=False, blank=False)
    aula = models.ForeignKey(
        Aula, on_delete=models.CASCADE, null=False, blank=False)


# Modelo LiderFicha 
class LiderFicha(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.IntegerField(null=False, blank=False)
    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, null=False, blank=False)
