from django.contrib import admin

from .models import ClientData


# Register your models here.
@admin.register(ClientData)
class ClientDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment',)
