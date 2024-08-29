from django.db import models


class Chat(models.Model):
    title: str = models.CharField(max_length=128, verbose_name="Название чата")
    users_online = models.ManyToManyField(
        "authorization.User",
        related_name="chats_online",
        verbose_name="Пользователи онлайн",
        )

    def __str__(self):
        return self.title
