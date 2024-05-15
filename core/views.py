from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AccessLog

def index(request):
    return render(request, 'index/index.html')

def user_access_logs(request, user_id):
    user_logs = AccessLog.objects.filter(user_id=user_id)
    return render(request, 'access_logs.html', {'user_logs': user_logs})