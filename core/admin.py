from django.contrib import admin
from .models import AccessLog, Index
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address','display_user', 'timestamp', 'path')
    search_fields = ('ip_address','user__username', 'user__first_name', 'user__last_name', 'path')
    list_filter = ('user', 'timestamp')
    ordering = ('-timestamp',)

    def display_user(self, obj):
        if obj.user:
            return obj.user.get_full_name() if obj.user.first_name and obj.user.last_name else obj.user.username
        else:
            return 'Anonymous'
    display_user.short_description = 'User'

@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ('tipo',)
    list_filter = ('tipo',)
    ordering = ('tipo',)