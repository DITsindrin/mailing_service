from django.urls import path
from django.views.decorators.cache import never_cache

from client.apps import ClientConfig

from .views import ClientCreateView, ClientUpdateView, ClientListView, ClientDetailView, ClientDeleteView

app_name = ClientConfig.name
urlpatterns = [
    path('', ClientListView.as_view(), name='client'),
    path('client-detail/<int:pk>', ClientDetailView.as_view(), name='client-detail'),
    path('client-create/', never_cache(ClientCreateView.as_view()), name='client-create'),
    path('client-edit/<int:pk>', never_cache(ClientUpdateView.as_view()), name='client-edit'),
    path('client-delete/<int:pk>', never_cache(ClientDeleteView.as_view()), name='client-delete'),
]
