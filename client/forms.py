from django.forms import ModelForm

from client.models import ClientData
from services.style_form_mixin import StyleFormMixin


class ClientForm(StyleFormMixin, ModelForm):
    """Форма для создания и редоктирования клиента"""
    class Meta:
        model = ClientData
        fields = ('full_name', 'email', 'comment',)
