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
    chat: Chat

    async def connect(self):
        self.user = self.scope["user"]
        self.chat_name = self.scope["url_route"]["kwargs"]["chat_name"]
        await self.channel_layer.group_add(
            self.chat_name, self.channel_name
        )
        self.chat = await a_try_to_get_object(
            manager=Chat.objects, exception=Chat.DoesNotExist, title=self.chat_name
        )
        await self.update_online_users(connected=True)
        await self.update_online_count()
        await self.accept()

    async def update_online_users(self, connected: bool) -> None:
        if connected:
            if not await self.user_exists_in_chat(self.user.id):
                await self.chat.users_online.aadd(self.user)
        else:
            if await self.user_exists_in_chat(self.user.id):
                await self.chat.users_online.aremove(self.user)

    async def user_exists_in_chat(self, user_id: int) -> bool:
        return await self.chat.users_online.filter(id=user_id).aexists()

    async def update_online_count(self) -> None:
        event: Dict[str, Any] = {
            "type": "online_count_handler",
            "online_count": await self.chat.users_online.acount() - 1
        }
        await self.channel_layer.group_send(
            self.chat_name, event
        )

    async def online_count_handler(self, event: Dict[str, Any]) -> None:
        context = self.get_template_context(online_count=event["online_count"])
        html = await self.render_to_string("chat/partials/online_count.html", context)

        await self.send(text_data=html)

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

    def get_template_context(self, **kwargs) -> Dict[str, Any]:
        return {
            "user": self.user,
            **kwargs,
        }

    async def message_handler(self, event: Dict[str, Any]) -> None:
        message = await self.get_message(id=event["message_id"])
        context = self.get_template_context(message=message)
        html = await self.render_to_string("chat/partials/message.html", context)

        await self.send(text_data=html)

    async def render_to_string(self, template_name: str, context: Dict[str, Any], **kwargs: Dict[str, Any]):
        return await sync_to_async(render_to_string)(template_name=template_name, context=context, **kwargs)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_name, self.channel_name
        )
        await self.update_online_users(connected=False)
        await self.update_online_count()

    async def get_message(self, id: int) -> Message:
        return await Message.objects.aget(id=id)