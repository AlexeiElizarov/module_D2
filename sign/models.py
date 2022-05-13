from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

# Форма для создания нового пользователя

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    about = models.CharField(max_length=250, blank=True)
    age = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('user_profile_page', kwargs={'pk': self.user.id})