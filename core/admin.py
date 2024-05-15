from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccessLog

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'path')  # Corrigido 'pat' para 'path'
    search_fields = ('user__username',)  # Adicione '__username' para buscar pelo nome de usuário
    list_filter = ('user', 'timestamp')
    ordering = ('user__username',)