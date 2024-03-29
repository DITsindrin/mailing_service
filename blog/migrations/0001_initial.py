# Generated by Django 4.2.7 on 2024-02-01 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='название категории')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='заголовок статьи')),
                ('content', models.TextField(verbose_name='контент')),
                ('preview', models.ImageField(default='default.png', upload_to='blog_img', verbose_name='превью')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.categoryarticle', verbose_name='категория статьи')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
