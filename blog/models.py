from django.db import models


# Create your models here.
class CategoryArticle(models.Model):
    """Модель категории статьи"""
    title = models.CharField(max_length=250, verbose_name='название категории')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Article(models.Model):
    """Модель статьи"""
    title = models.CharField(max_length=300, verbose_name='заголовок статьи')
    content = models.TextField(verbose_name='контент')
    preview = models.ImageField(default='default.png', upload_to='blog_img', verbose_name='превью')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    category = models.ForeignKey(CategoryArticle, on_delete=models.CASCADE, verbose_name='категория статьи')

    introduction = models.CharField(max_length=700, null=True, verbose_name='Вступление')

    def __str__(self):
        return f'{self.title} {self.date_creation} {self.category}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
