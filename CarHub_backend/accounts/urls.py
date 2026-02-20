from django.urls import path
from .views import user_list, register_customer, customer_profile

urlpatterns = [
    path('users/', user_list),
    path('register/', register_customer),
    path('me/', customer_profile),
]
