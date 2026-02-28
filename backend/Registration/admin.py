from django.contrib import admin
from .models import CustomUserModel
@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_staff', 'is_active')
    search_fields = ('email', 'phone')
    ordering = ('email',)
