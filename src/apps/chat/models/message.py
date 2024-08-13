from datetime import datetime
from django.db import models
from src.apps.auth.models import User
from . import Chat


class Message(models.Model):
    author: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages"
    )
    chat: Chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
    content: str = models.CharField(max_length=300, verbose_name="Контент")
    created_at: datetime = models.DateTimeField(
        verbose_name="Время создания", auto_now_add=True
    )

    def __str__(self) -> str:
        return f"{self.author.first_name} {self.author.last_name} : {self.content[:10]}"

    class Meta:
        ordering = ("created_at",)
