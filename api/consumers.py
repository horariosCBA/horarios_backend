import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Mensaje
from asgiref.sync import sync_to_async
from django.db.models import Q

'''
El archivo consumers.py en Django define los consumidores para manejar conexiones WebSocket, 
permitiendo la comunicación en tiempo real como chat en vivo o notificaciones instantáneas.
'''

class ChatConsumer(AsyncWebsocketConsumer):

    # Función que se ejecuta cuando un usuario se conecta al servidor
    async def connect(self):
        # Obtener los usuarios de la URL
        self.usuario_emisor = self.scope['url_route']['kwargs']['usuario_emisor']
        self.usuario_receptor = self.scope['url_route']['kwargs']['usuario_receptor']
        
        # Generar el nombre de la sala único basado en los IDs de los usuarios
        ids_ordenados = sorted([str(self.usuario_emisor), str(self.usuario_receptor)])
        self.room_name = f'chat_{ids_ordenados[0]}_{ids_ordenados[1]}'

        # Agregar el canal del usuario a la sala
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # Aceptar la conexión WebSocket
        await self.accept()

    # Función que se ejecuta cuando un usuario se desconecta del servidor
    async def disconnect(self, close_code):
        # Eliminar el canal del usuario de la sala al desconectar
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Función que se ejecuta cuando se recibe un mensaje de un usuario
    async def receive(self, text_data):
        # Recibir y procesar datos del WebSocket
        data = json.loads(text_data)
        action = data.get('action')
        usuario_emisor = data.get('usuarioEmisor')
        usuario_receptor = data.get('usuarioReceptor')
        usuario_actual = data.get('usuarioActual')

        if not usuario_emisor or not usuario_receptor:
            await self.send(text_data=json.dumps({'error': 'usuarioEmisor y usuarioReceptor son requeridos'}))
            return

        if action == 'send_message':
            await self.send_message(data, usuario_emisor, usuario_receptor)
        elif action == 'load_conversation':
            await self.load_conversation(usuario_emisor, usuario_receptor, usuario_actual)
        elif action == 'delete_conversation':
            await self.delete_conversation(usuario_emisor, usuario_receptor, usuario_actual)
        elif action == 'mark_as_read':
            await self.mark_as_read(usuario_emisor, usuario_receptor)


    # Función que se ejecuta cuando un usuario envía un mensaje
    async def send_message(self, data, usuario_emisor, usuario_receptor):
        # Crea y guarda el mensaje en la base de datos
        mensaje = await sync_to_async(Mensaje.objects.create)(
            usuarioReceptor=usuario_receptor,
            usuarioEmisor=usuario_emisor,
            contenido=data['contenido'],
            tipo=data['tipo'],
            imagen=data['imagen'],
        )

        # Envía el mensaje a todos los usuarios conectados en la sala
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': mensaje.id,
                    'usuarioReceptor': mensaje.usuarioReceptor,
                    'usuarioEmisor': mensaje.usuarioEmisor,
                    'contenido': mensaje.contenido,
                    'fechaEnviado': mensaje.fechaEnviado.isoformat(),
                    'tipo': mensaje.tipo,
                    'imagen': mensaje.imagen,
                    'eliminarEmisor': mensaje.eliminarEmisor,
                    'eliminarReceptor': mensaje.eliminarReceptor,
                }
            }
        )

    # Función que se ejecuta cuando un usuario carga la conversación
    async def load_conversation(self, usuario_emisor, usuario_receptor, usuario_actual):
        # Filtra los mensajes según el estado de eliminación para el usuario actual
        mensajes = await sync_to_async(list)(
            Mensaje.objects.filter(
                usuarioEmisor__in=[usuario_emisor, usuario_receptor],
                usuarioReceptor__in=[usuario_emisor, usuario_receptor]
            ).exclude(
                # Excluir mensajes eliminados por el usuario actual
                Q(usuarioEmisor=usuario_actual, eliminarEmisor=True) |
                Q(usuarioReceptor=usuario_actual, eliminarReceptor=True)
            ).order_by('fechaEnviado')
        )

        # Convierte los mensajes en JSON
        mensajes_json = [
            {
                'id': msg.id,
                'usuarioReceptor': msg.usuarioReceptor,
                'usuarioEmisor': msg.usuarioEmisor,
                'contenido': msg.contenido,
                'fechaEnviado': msg.fechaEnviado.isoformat(),  # Convertir a formato ISO
                # Formato ISO si no es None
                'fechaLeido': msg.fechaLeido.isoformat() if msg.fechaLeido else None,
                'tipo': msg.tipo,
                'imagen': msg.imagen,
                'eliminarEmisor': msg.eliminarEmisor,
                'eliminarReceptor': msg.eliminarReceptor,
            }
            for msg in mensajes
        ]

        # Envía los mensajes cargados al usuario conectado
        await self.send(text_data=json.dumps({'action': 'load_conversation', 'messages': mensajes_json}))

    # Función que se ejecuta cuando un usuario elimina la conversación
    async def delete_conversation(self, usuario_emisor, usuario_receptor, usuario_actual):
        if usuario_actual == usuario_emisor:
            # Marca los mensajes como eliminados por el emisor
            await sync_to_async(Mensaje.objects.filter(
                usuarioEmisor=usuario_emisor,
                usuarioReceptor=usuario_receptor
            ).update)(eliminarEmisor=True)
            await sync_to_async(Mensaje.objects.filter(
                usuarioEmisor=usuario_receptor,
                usuarioReceptor=usuario_emisor
            ).update)(eliminarReceptor=True)
        elif usuario_actual == usuario_receptor:
            # Marca los mensajes como eliminados por el receptor
            await sync_to_async(Mensaje.objects.filter(
                usuarioEmisor=usuario_receptor,
                usuarioReceptor=usuario_emisor
            ).update)(eliminarReceptor=True)
            await sync_to_async(Mensaje.objects.filter(
                usuarioEmisor=usuario_emisor,
                usuarioReceptor=usuario_receptor
            ).update)(eliminarEmisor=True)
        else:
            # Maneja el caso donde el usuario que hace la petición no es ni el emisor ni el receptor
            await self.send(text_data=json.dumps({'action': 'delete_conversation', 'status': 'error', 'message': 'Usuario no autorizado'}))
            return

        # Notifica al usuario que la conversación se ha eliminado con éxito
        await self.send(text_data=json.dumps({'action': 'delete_conversation', 'status': 'success'}))

        # Envía la acción para limpiar la conversación al usuario conectado
        await self.send(text_data=json.dumps({'action': 'clear_conversation'}))


    # Función que se ejecuta cuando un usuario marca los mensajes como leídos
    async def mark_as_read(self, usuario_emisor, usuario_receptor):
        # Marca los mensajes como leídos
        mensajes = await sync_to_async(list)(
            Mensaje.objects.filter(
                usuarioReceptor=usuario_receptor,
                usuarioEmisor=usuario_emisor,
                fechaLeido__isnull=True
            )
        )

        for msg in mensajes:
            msg.fechaLeido = datetime.now()
            await sync_to_async(msg.save)()

        # Notifica al usuario que los mensajes se han marcado como leídos
        await self.send(text_data=json.dumps({'action': 'mark_as_read', 'status': 'success'}))

    # Función que se ejecuta cuando un usuario recibe un mensaje
    async def chat_message(self, event):

        # Envía el mensaje a través del WebSocket
        message = event['message']

        await self.send(text_data=json.dumps({
            'action': 'chat_message',
            'message': message
        }))
