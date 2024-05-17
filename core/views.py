from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import AccessLog, Index
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

User = get_user_model()

def index(request):
    # Template default
    template_name = 'index/index.html'

    # Lista com as três opções
    opcoes = [
        Index.TIPO_LANDING_PAGE,
        Index.TIPO_PORTFOLIO,
        Index.TIPO_AGENCY,
    ]

    # Iterar sobre as opções
    for opcao in opcoes:
        try:
            # Tenta encontrar um objeto Index com o tipo correspondente
            index = Index.objects.get(tipo=opcao)
            template_name = index.template
            print(f"Encontrado um objeto Index com tipo '{opcao}'")
        except ObjectDoesNotExist:
            print(f"Nenhum objeto Index com tipo '{opcao}' encontrado")
        except MultipleObjectsReturned:
            print(f"Mais de um objeto Index com tipo '{opcao}' encontrado")

    return render(request, template_name)

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
