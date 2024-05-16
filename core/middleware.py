from django.utils import timezone
from .models import AccessLog
from django.contrib.auth import get_user_model

User = get_user_model()

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de executar a view
        response = self.get_response(request)
        
        # Após executar a view
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            # Se o usuário estiver autenticado, usa o usuário autenticado
            user = request.user
        else:
            # Se não estiver autenticado, usa um usuário padrão (ou cria um)
            user, _ = User.objects.get_or_create(username='Anonymous')

        # Cria o AccessLog
        access_log = AccessLog.objects.create(
            user=user,
            timestamp=timezone.now(),
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
