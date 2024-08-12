from django.db import models

class Chat(models.Model):
    title: str = models.CharField(max_length=128, verbose_name="Название чата")

    def __str__(self):
        return self.title
    