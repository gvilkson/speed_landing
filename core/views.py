from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import AccessLog
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

User = get_user_model()

def index(request):
    return render(request, 'index/index.html')

def user_access_logs(request, user_id):
    if request.user.is_authenticated:
        user_logs = AccessLog.objects.filter(user_id=user_id)
        return render(request, 'access_logs.html', {'user_logs': user_logs})
    else:
        # Obtenha ou crie um usuário anônimo
        anonymous_user, created = User.objects.get_or_create(username='Anonymous')
        
        # Crie um objeto AccessLog apenas se o usuário anônimo não existir
        if created:
            access_log = AccessLog.objects.create(user=anonymous_user)
        
        # Redirecione para a página de login ou para uma página apropriada
        return redirect('login')  # Você pode ajustar isso de acordo com suas necessidades
