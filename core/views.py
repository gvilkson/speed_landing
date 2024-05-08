from django.shortcuts import render
from django.http import HttpResponseServerError
from django.conf import settings
import mercadopago

def checkout(request):
    try:
        mp = mercadopago.MP(settings.MERCADO_PAGO_CLIENT_ID, settings.MERCADO_PAGO_CLIENT_SECRET)
    except Exception as e:
        # Log o erro, renderize uma página de erro ou faça qualquer ação apropriada
        print("Erro ao instanciar o objeto MP:", e)
        return HttpResponseServerError("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.")
    
    preference = {
        "items": [
            {
                "title": "Produto",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100.00
            }
        ],
        "back_urls": {
            "success": request.build_absolute_uri('/sucesso/'),
            "failure": request.build_absolute_uri('/erro/'),
            "pending": request.build_absolute_uri('/pendente/')
        },
        "auto_return": "approved"
    }
    preferenceResult = mp.create_preference(preference)
    checkout_url = preferenceResult['response']['sandbox_init_point']  # Use 'init_point' em produção
    return render(request, 'checkout.html', {'checkout_url': checkout_url})
