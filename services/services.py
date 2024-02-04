from django.conf import settings
from django.core.cache import cache

# from blog.models import CategoryArticle


# def get_category_article_cache():
#     if settings.CACHE_ENABLED:
#         key = 'category_list'
#         category_list = cache.get(key)
#         if category_list is None:
#             category_list = CategoryArticle.objects.all()
#             cache.set(key, category_list)
#     else:
#         category_list = CategoryArticle.objects.all()
#
#     return category_list
