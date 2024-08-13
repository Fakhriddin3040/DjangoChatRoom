from django.shortcuts import render

from src.apps.chat.forms import MessageCreateForm
from src.apps.chat.models import Chat
from src.utils.functions.models import try_to_get_object


def chat_view(request) -> render:
    chat = try_to_get_object(
        Chat.objects,
        Chat.DoesNotExist,
        title="Niger.com"
    )
    messages = chat.messages.all()
    form = MessageCreateForm()

    if request.htmx:

        form = MessageCreateForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat
            message.save()

            context = {
                'message': message,
                'user': request.user
            }
            return render(request, "chat/partials/message.html", context)

    return render(request, "chat/chat.html", {"chat_messages": messages, "form": form})
