from django.db import models

from users.models import User


# Create your models here.


class ClientData(models.Model):
    """Модель клиента"""
    full_name = models.CharField(max_length=300, verbose_name='ФИО клиента')
    email = models.EmailField(verbose_name='Email клиента')
    comment = models.CharField(max_length=500, verbose_name='Коментарий')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.full_name}, {self.email}, {self.user}'

    class Meta:
        unique_together = (["email", "user"],)
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
