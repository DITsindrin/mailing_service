from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='users/', default='users.png', null=True, blank=True, verbose_name='Аватар')

    name_organization = models.CharField(max_length=75, default='Заполните название вашей организации', verbose_name='Название организации пользователя')
    is_active = models.BooleanField(default=False, verbose_name='признак верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
