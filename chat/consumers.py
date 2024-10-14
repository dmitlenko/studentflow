import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
from .models import ChatGroup, ChatGroupMessage
from asgiref.sync import sync_to_async
from .serializers import ChatGroupMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.serializer = ChatGroupMessageSerializer

    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def convert_date(self, date_time):
        return str(Template('{{d}}').render(Context({'d': date_time})))

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_group_id = data['chat_group']
        body = data['body']

        author = self.scope['user']
        chat_group = await sync_to_async(ChatGroup.objects.get)(id=chat_group_id)

        participants = await sync_to_async(chat_group.participants.all)()
        if not (author == chat_group.creator or author in participants):
            return

        data = await sync_to_async(ChatGroupMessage.objects.create)(author=author, chat_group=chat_group, body=body)
        serialized_data = self.serializer(data)

        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'data': serialized_data.data })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['data']))
            