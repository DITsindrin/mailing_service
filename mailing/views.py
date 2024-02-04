from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Article
from client.models import ClientData
from mailing.models import Mailing, Message
from mailing.forms import MailingCreateForm, MessageCreateForm


# Create your views here.

def home(request):
    """Главная страница. Вывод количества рассылок, вывод количества активных рассылок, вывод уникалных клиентов, Вывод трех первых рандомных статей"""
    title = 'MailingService-Печкин'
    greetings = 'Добро пожаловать на сайт самого лучшего сервиса по массовым рассылкам для бизнеса. У нас Вы можете зарегистрироваться, загрузить данные о клиентах, настроить рассылку и наслаждаться жизнью все остальное сделает наш сервис.'
    mailing_all = Mailing.objects.all().count()
    mailing_is_activ = Mailing.objects.all().filter(is_active=True).count()
    unique_client = ClientData.objects.all().values("email").distinct().count()
    random_blog = Article.objects.all().order_by('?')[:3]

    context = {
        'title': title,
        'appeal': greetings,
        'mailing_all': mailing_all,
        'mailing_is_activ': mailing_is_activ,
        'unique_client': unique_client,
        'random_blog': random_blog,
    }
    return render(request, 'mailing/home.html', context)


@login_required
@permission_required('mailing.change_mailing')
def disable_mailings(request, pk):
    """Блокировка\Активация рассылки для модератора"""
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True

    mailing.save()

    return redirect(reverse('mailing:mailing'))


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Вывод всех рассылок"""
    model = Mailing
    paginate_by = 4
    permission_required = 'mailing.view_mailing'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши рассылки'

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        current_user = self.request.user

        if not current_user.is_staff:
            queryset = queryset.filter(user=current_user)

        return queryset


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Вывод подробной информации о настройки рассылки"""
    model = Mailing
    permission_required = 'mailing.view_mailing'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание настройки рассылки и сообщения"""
    model = Mailing
    form_class = MailingCreateForm
    success_url = reverse_lazy('mailing:mailing')
    permission_required = 'mailing.add_mailing'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFromSet = inlineformset_factory(Mailing, Message, form=MessageCreateForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFromSet(self.request.POST)
        else:
            context_data['formset'] = MessageFromSet()

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        form.instance.user = self.request.user
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение настройки рассылки и сообщения"""
    model = Mailing
    form_class = MailingCreateForm
    success_url = reverse_lazy('mailing:mailing')
    permission_required = 'mailing.change_mailing'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404

        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFromSet = inlineformset_factory(Mailing, Message, form=MessageCreateForm, extra=0)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFromSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFromSet(instance=self.object)

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление настройки рассылки"""
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing')
