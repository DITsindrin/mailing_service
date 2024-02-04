from django.forms import ModelForm

from blog.models import Article
from services.style_form_mixin import StyleFormMixin


class ArticleForm(StyleFormMixin, ModelForm):
    """Форма для создания и изменения статьи"""
    class Meta:
        model = Article
        fields = ('title', 'content', 'preview', 'category',)