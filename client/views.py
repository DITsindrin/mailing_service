from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from client.forms import ClientForm
from client.models import ClientData


# Create your views here.
class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание клиента"""
    model = ClientData
    form_class = ClientForm
    permission_required = 'client.add_clientdata'
    success_url = reverse_lazy('client:client')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование клиента"""
    model = ClientData
    form_class = ClientForm
    permission_required = 'client.change_clientdata'

    def get_success_url(self):
        return reverse('client:client')


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Вывод всех клиентов"""
    model = ClientData
    paginate_by = 8
    permission_required = 'client.view_clientdata'

    def get_queryset(self):
        queryset = super().get_queryset()
        current_user = self.request.user

        if not current_user.is_staff:
            queryset = queryset.filter(user=current_user)

        return queryset


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Вывод полной информации о клиенте"""
    model = ClientData
    permission_required = 'client.view_clientdata'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление клиента"""
    model = ClientData
    permission_required = 'client.delete_clientdata'
    success_url = reverse_lazy('client:client')
