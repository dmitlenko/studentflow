import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
from .models import ChatGroup, ChatGroupMessage
from base.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def convert_date(self, date_time):
        return str(Template('{{d}}').render(Context({'d': date_time})))

    async def receive(self, text_data):
        data = json.loads(text_data)
        author_id = data['author']
        chat_group_id = data['chat_group']
        body = data['body']

        author = await sync_to_async(User.objects.get)(id=author_id)
        chat_group = await sync_to_async(ChatGroup.objects.get)(id=chat_group_id)

        if not (author == chat_group.creator or author in await sync_to_async(chat_group.participants.all)()):
            return

        message = await sync_to_async(ChatGroupMessage.objects.create)( author = author, chat_group = chat_group,body = body)
        response_data = {
            'userId': message.author.id,
            'username': message.author.username,
            'message': message.body,
            'date_created': await self.convert_date(message.date_created)
        }

        await self.channel_layer.group_send(
            self.room_group_name, 
            {'type': 'chat_message', 'data': response_data})

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['data']))