from django.contrib import admin

# Register your models here.
from .models import Mailing, Message, MailingLogs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'mailing_periodicity', 'mailing_status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_settings', 'letter_subject', 'body_letter',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_try', 'attempt_status', 'client', 'mailing_settings', 'error_msg',)
