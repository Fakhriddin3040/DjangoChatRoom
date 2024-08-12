# Generated by Django 5.0.7 on 2024-08-12 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="chat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="chat.chat",
            ),
        ),
    ]
