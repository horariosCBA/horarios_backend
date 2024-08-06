from rest_framework import serializers
from api.models import *

'''
Los serializadores en Django convierten datos de la base de datos en formatos 
como JSON para enviarlos a través de una API, y también transforman datos recibidos en 
la API para guardarlos en la base de datos.
'''


# Serializador del modelo Programa
class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'


# Serializador del modelo Competencia
class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = '__all__'

    #Trae tanto la estructura y los valores de la tabla programa
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['programa'] = ProgramaSerializer(
                instance.programa, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)


# Serializador del modelo ResultadoAprendizaje
class ResultadoAprendizajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoAprendizaje
        fields = '__all__'

    #Trae tanto la estructura y los valores de la tabla competencia
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['competencia'] = CompetenciaSerializer(
                instance.competencia, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)
        

# Serializador del modelo Ficha
class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'

    #Trae tanto la estructura y los valores de la tabla programa
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['programa'] = ProgramaSerializer(
                instance.programa, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)


# Serializador del modelo Trimestre
class TrimestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trimestre
        fields = '__all__'

    #Trae tanto la estructura y los valores de la tabla ficha
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['ficha'] = FichaSerializer(
                instance.ficha, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)
        

# Serializador del modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


# Serializador del modelo PlaneacionPedagogica
class PlaneacionPedagogicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaneacionPedagogica
        fields = '__all__'

    #Trae tanto la estructura y los valores de las tablas ficha y usuario
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['usuario'] = UsuarioSerializer(
                instance.usuario, context=self.context).data
            representation['ficha'] = FichaSerializer(
                instance.ficha, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)


# Serializador del modelo Aula
class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'


# Serializador del modelo Horario
class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

    #Trae tanto la estructura y los valores de las tablas PlaneacionPedagogica y Aula
    def to_representation(self, instance):
        if 'request' in self.context:
            # Agregar campos adicionales para la solicitud GET
            representation = super().to_representation(instance)
            representation['planeacionPedagogica'] = PlaneacionPedagogicaSerializer(
                instance.planeacionPedagogica, context=self.context).data
            representation['aula'] = AulaSerializer(
                instance.aula, context=self.context).data
            return representation
        else:
            return super().to_representation(instance)
        

# Serializador del modelo Mensaje
class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'
