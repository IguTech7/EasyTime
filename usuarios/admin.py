from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo', 'is_staff')
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo',)}),
    )
    pass