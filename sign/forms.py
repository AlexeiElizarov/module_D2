from django.core.mail import send_mail
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'age']


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

    def save(self, commit=True):
        user = super(BaseRegisterForm,self).save()
        user.set_password(self.cleaned_data["password1"])
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        if commit:
            user.save()
        print(user.email)
        send_mail(
            subject='Hello',
            message=f'Hello, {user.username}. Вы зарегистрированны.',
            from_email='Lafen55@yandex.ru',
            recipient_list=[user.email]
        )
        return user
