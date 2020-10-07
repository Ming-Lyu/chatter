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

import base64

from django.core.files.base import ContentFile
import hashlib
import io
import re

B64_PAT_RE = 'NOT_SUPPORT'

def base64_decode(data, name=None):
    format, imgstr = data.split(';base64,') 
    ext = format.split('/')[-1]
    if not name:
        name = hashlib.md5(data.encode()).hexdigest()
    data = ContentFile(base64.b64decode(imgstr), name=name + '.' + ext)
    return data

class ChatConsumer(AsyncWebsocketConsumer):
    '''Async chat consumer
    '''
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
        user = self.scope['user']
        opponent_username = text_data_json['opponent_username']
        opponent = await self.get_user(username=opponent_username)

        # TODO: check the action
        # await self.create_dialog(user=user)
        dialog = await self.get_or_create_dialog(owner=user, opponent=opponent)
        
        message = text_data_json['message']

        if self._has_base64_str(message):
            self._has_file = True
            # saving to db.
            img_file = base64_decode(message)
            await self.create_message(owner=user, content='', dialog=dialog, file=img_file)
        else:
            self._has_file = False
            await self.create_message(owner=user, content=message, dialog=dialog)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': user.username,
                'has_file': self._has_file,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author, 
            'has_file': event['has_file'],
        }))

    # utils
    def _has_base64_str(self, value):
        '''test if the data send to server is base64 encoded
        '''
        return True if ';base64' in value else False
