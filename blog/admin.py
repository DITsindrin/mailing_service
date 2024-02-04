from django.contrib import admin

from blog.models import Article, CategoryArticle


# Register your models here.
@admin.register(CategoryArticle)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)


@admin.register(Article)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'content', 'date_creation', 'views_count',)
    list_filter = ('category',)
    search_fields = ('category',)
