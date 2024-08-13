import json
from typing import Any, Dict

from channels_redis.core import RedisChannelLayer
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from src.apps.chat.models import Chat, Message
from src.utils.functions.models import a_try_to_get_object


class ChatConsumer(AsyncWebsocketConsumer):
    channel_layer: RedisChannelLayer

    async def connect(self):
        self.user = self.scope["user"]
        self.chat_name = self.scope["url_route"]["kwargs"]["chat_name"]
        await self.channel_layer.group_add(
            self.chat_name, self.channel_name
        )
        self.chat = await a_try_to_get_object(
            manager=Chat.objects, exception=Chat.DoesNotExist, title=self.chat_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]

        message = await Message.objects.acreate(
            content=content, author=self.user, chat=self.chat
        )
        event: Dict[str, Any] = {
            "type": "message_handler",
            "message_id": message.id
        }
        await self.channel_layer.group_send(
            self.chat_name, event
        )

    async def message_handler(self, event: Dict[str, Any]) -> None:
        message = await self.get_message(id=event["message_id"])
        context = {
            "message": message,
            "user": self.user,
        }
        html = await sync_to_async(render_to_string)("chat/partials/message.html", context=context)
        await self.send(text_data=html)
        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_name, self.channel_name
        )

    async def get_message(self, id: int) -> Message:
        return await Message.objects.aget(id=id)