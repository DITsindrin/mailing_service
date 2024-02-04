from datetime import timedelta, time
from django.db import models

from client.models import ClientData
from users.models import User


# Create your models here.

class Mailing(models.Model):
    """Модель настройи рассылки"""
    DAILY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'
    FREQUENCY_MAILING_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    CREATED = 'создана'
    LAUNCHED = 'запущена'
    COMPLETED = 'завершена'
    NEWSLETTER_STATUS_CHOICES = [
        (COMPLETED, 'завершена'),
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название рассылки')
    start_time = models.TimeField(default=time(hour=11), verbose_name='Время начала рассылки')
    end_time = models.TimeField(default=time(hour=13), verbose_name='Время окончания рассылки')
    mailing_periodicity = models.CharField(choices=FREQUENCY_MAILING_CHOICES, default=DAILY,
                                               verbose_name='Переодичность рассылки')
    mailing_status = models.CharField(max_length=10, choices=NEWSLETTER_STATUS_CHOICES, default=CREATED,
                                      verbose_name='Статус рассылки')

    client = models.ManyToManyField(ClientData, verbose_name='Клиент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    is_active = models.BooleanField(default=False, verbose_name='Признак активной рассылки')

    def __str__(self):
        return f'{self.title} {self.start_time} {self.end_time} {self.mailing_status} {self.mailing_periodicity} {self.client}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    """Модель сообщения"""
    mailing_settings = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    letter_subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body_letter = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.mailing_settings} {self.letter_subject} {self.body_letter}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLogs(models.Model):
    """Модель лога"""
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.BooleanField(verbose_name='Статус попытки')
    error_msg = models.TextField(verbose_name='Сообщение ошибки')

    client = models.CharField(max_length=75, verbose_name='Клиент')
    mailing_settings = models.CharField(max_length=75, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.last_try} {self.attempt_status} {self.error_msg} {self.client} {self.mailing_settings}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
