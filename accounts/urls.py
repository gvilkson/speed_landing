from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as v

app_name = 'accounts'

urlpatterns = [

    path('lock-screen/', v.lock_screen, name='lock-screen'),
    path('logout/', v.logout_view, name='logout'),
    path('profile/', v.profile, name='profile'),
    path('register/', v.register, name='register'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_custom.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_custom.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_custom.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_custom.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

]