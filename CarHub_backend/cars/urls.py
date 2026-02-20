from django.urls import path, include
from .views import car_detail, car_list

urlpatterns = [
    path('', car_list),
    path('cars/<int:pk>/', car_detail),
]
