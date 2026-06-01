from django.urls import path, include
from .views import car_detail, car_list, calculate_configuration, add_to_cart, remove_cart_item, view_cart

urlpatterns = [
    path('', car_list),
    path('cars/<int:pk>/', car_detail),
    path('configurator/', calculate_configuration),
    path('cart/add/', add_to_cart),
    path('cart/', view_cart),
    path('cart/item/<int:item_id>/remove/', remove_cart_item),
]
