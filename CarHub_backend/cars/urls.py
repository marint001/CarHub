from django.urls import path, include
from .views import (car_detail, car_list, calculate_configuration, add_to_cart, remove_cart_item, view_cart, update_cart_quantity,
                    used_car_list, used_car_detail)

urlpatterns = [
    path('', car_list),
    path('cars/<int:pk>/', car_detail),
    path('configurator/', calculate_configuration),
    path('cart/add/', add_to_cart),
    path('cart/', view_cart),
    path('cart/item/<int:item_id>/remove/', remove_cart_item),
    path('cart/item/<int:item_id>/update/', update_cart_quantity),
    path('used-cars/', used_car_list),
    path('used-cars/<int:pk>/', used_car_detail),
]
