# import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
# from channels.generic.websocket import WebsocketConsumer
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Dialog
from django.contrib.auth.models import User
from functools import partial
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def create_message(self, **kwargs):
        await database_sync_to_async(partial(Message.objects.create, **kwargs))()


    @database_sync_to_async
    def get_or_create_dialog(self, **kwargs):
        return Dialog.objects.get_or_create_dialog(**kwargs)

    @database_sync_to_async
    def get_user(self, *, username=None):
        return User.objects.get(username=username)


    @database_sync_to_async
    def fetch_history_messages(self, *, owner:User=None, opponent:User=None):
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('**************')
        print(text_data_json)

        # TODO
        # initilise the dialog with somebody

        # preparing the data
        user = self.scope['user']
        message = text_data_json['message']
        opponent_username = text_data_json['opponent_username']
        
        opponent = await self.get_user(username=opponent_username)

        # TODO: check the action
        # await self.create_dialog(user=user)
        dialog = await self.get_or_create_dialog(owner=user, opponent=opponent)
        await self.create_message(owner=user, content=message, dialog=dialog)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))