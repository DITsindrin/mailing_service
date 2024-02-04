from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig

from .views import home, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    disable_mailings

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(home), name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('mailing-detail/<int:pk>', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailing-edit/<int:pk>', MailingUpdateView.as_view(), name="mailing-edit"),
    path('mailing-create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailing-delete/<int:pk>', MailingDeleteView.as_view(), name='mailing-delete'),
    path('mailing-disable/<int:pk>', disable_mailings, name='mailing-disable'),
]
