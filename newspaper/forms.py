from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, BooleanField
from .models import Post
from django.contrib.auth.models import User
from django import forms


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и
    # нужные нам поля. Мы уже делали что-то похожее с фильтрами.

    # check_box = BooleanField(label='Ало, Галочка!')

    class Meta:
        model = Post
        fields = ['author', 'title_post', 'body_post']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

