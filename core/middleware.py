from django.utils import timezone
from .models import AccessLog


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de executar a view
        response = self.get_response(request)
        
        # Após executar a view
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if request.user.is_authenticated:
            # Se o usuário estiver autenticado, registre normalmente
            access_log = AccessLog(user=request.user, timestamp=timezone.now(), path=request.path,
                                   ip_address=ip_address, user_agent=user_agent)
            access_log.save()
        else:
            # Se o usuário for anônimo, registre suas ações com um usuário especial
            access_log = AccessLog(user=None, timestamp=timezone.now(), path=request.path,
                                   ip_address=ip_address, user_agent=user_agent)
            access_log.save()

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip