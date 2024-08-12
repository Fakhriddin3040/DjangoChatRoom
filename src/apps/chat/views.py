from django.shortcuts import render

from src.apps.chat.models import Chat
from src.utils.functions.models import try_to_get_object


def chat_view(request) -> render:
    chat = try_to_get_object(
        Chat.objects,
        Chat.DoesNotExist,
        title="Niger.com"
    )
    messages = chat.messages.all()
    print(messages)
    return render(request, "chat/chat.html", {"chat_messages": messages})
