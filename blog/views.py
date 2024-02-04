from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import ArticleForm
from blog.models import Article, CategoryArticle


# Create your views here.

class ArticleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Вывод всех статей"""
    model = Article
    paginate_by = 8
    permission_required = 'blog.view_article'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str,]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Печкин NewS'
        context['category_list'] = CategoryArticle.objects.all()

        return context


class ArticleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Вывод полной информации о статье"""
    model = Article
    permission_required = 'blog.view_article'

    def get_context_data(self, **kwargs) -> dict[str,]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание статьи"""
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.add_article'
    success_url = reverse_lazy('blog:blogs')


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение статьи"""
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.change_article'

    def get_success_url(self):
        return reverse('blog:blogs')


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление статьи"""
    model = Article
    permission_required = 'blog.delete_article'
    success_url = reverse_lazy('blog:blogs')

