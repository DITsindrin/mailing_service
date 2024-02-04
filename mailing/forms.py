from django.forms import ModelForm, formset_factory, inlineformset_factory

from services.style_form_mixin import StyleFormMixin
from mailing.models import Mailing, Message


class MailingCreateForm(StyleFormMixin, ModelForm):
    """Форма для создания настройки рассылки"""
    class Meta:
        model = Mailing
        fields = ('title', 'start_time', 'end_time', 'mailing_periodicity', 'mailing_status', 'client',)


class MessageCreateForm(StyleFormMixin, ModelForm):
    """Форма для создания сообщения"""
    class Meta:
        model = Message
        fields = ('letter_subject', 'body_letter',)
