from django import forms
from .models import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(
                attrs={
                "placeholder": "Add message ...", "class": "p-4 text-black", "maxlength": "300", "autofocus": True
                }
            )
        }