from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = ['author',
                  'postCategory',
                  'title',
                  'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Текст не должен быть идентичным названию."
            )

        return cleaned_data
