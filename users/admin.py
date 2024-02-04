from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", 'phone', 'avatar', 'is_active', 'is_staff', 'first_name', 'last_name', 'is_superuser',)
