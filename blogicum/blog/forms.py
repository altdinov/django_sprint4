from django import forms
from django.utils import timezone

from .models import Comment, Post, User


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
        initial=timezone.now,
        label='Дата и время публ.'
    )

    class Meta:
        model = Post
        exclude = ('author', 'is_published')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
