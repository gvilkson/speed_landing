from core.models import Index
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def all_data(request):
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
            index_tipo = Index.objects.get(tipo=opcao)
            tipo = index_tipo.tipo
            print(f"Encontrado um objeto Index com tipo '{opcao}'")
        except ObjectDoesNotExist:
            print(f"Nenhum objeto Index com tipo '{opcao}' encontrado")
        except MultipleObjectsReturned:
            print(f"Mais de um objeto Index com tipo '{opcao}' encontrado")

    return {
        'site_type': tipo,
    }
    