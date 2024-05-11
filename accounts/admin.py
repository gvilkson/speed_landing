from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreateForm, CustomUserChangeForm
from accounts.models import CustomUser, UserProfile, Address

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissôes', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),

    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('get_username', 'get_email', 'avatar',)  # 'avatar' is just an example, replace it with your actual field
    # remove or correct filter_horizontal, ordering, and list_filter

    def get_username(self, obj):
        return obj.user.first_name + ' ' +  obj.user.last_name
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ('get_username', 'street', 'city', 'state', 'country', 'postal_code')
    search_fields = ('user_profile__user__username', 'street', 'city', 'state', 'country', 'postal_code')
    list_filter = ('country', 'state', 'city')
    ordering = ('user_profile__user__username',)

    def get_username(self, obj):
        return obj.user_profile.user.first_name + ' ' +  obj.user_profile.user.last_name
    get_username.short_description = 'Username'