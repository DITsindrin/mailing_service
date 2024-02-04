import random

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка ссылки для верификации"""
        user = form.save(commit=False)
        user.is_active = False  # User will be activated after email verification
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        activation_link = reverse_lazy(
            'users:email_verification', kwargs={'uidb64': uid})

        activation_url = f"{current_site}{activation_link}"

        mail_subject = 'Верификации аккаунта'

        massage = render_to_string('users/email_verification.html', {
            'activation_url': activation_url
        })

        # метод email_user для отправкки письма пользователю класса AbstractUser - """Send an email to this user."""
        user.email_user(mail_subject, massage)

        return super().form_valid(form)


def verification_account(request, uidb64):
    """Верификация аккаунта"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=int(uid))
        user.is_active = True
        user.save()
        return redirect('users:verification_completed')
    except User.DoesNotExist:
        return redirect('users:verification_failed')


class ActivationCompleted(TemplateView):
    """Верификация выполнена"""
    template_name = 'users/email_verification_completed.html'


class ActivationFailed(TemplateView):
    """Верификация не выполнена"""
    template_name = 'users/email_verification_failed.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Вывод всех пользователей для модератора"""
    model = User
    paginate_by = 4
    permission_required = 'users.view_user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.all().exclude(is_staff=True)

        return queryset


@permission_required('users.change_user')
def disable_user(request, pk):
    """Блокировка\Активация пользователя для модератора"""
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:user-list'))


@login_required
def generate_new_password(request):
    """Отправка сгенерированного пароля пользователю для восстановления"""
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))
