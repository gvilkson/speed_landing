from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.index, name='index'),
    path('add_to_cart/<int:product_id>/', v.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', v.remove_from_cart, name='remove_from_cart'),
    path('cart/', v.view_cart, name='cart'),
]
