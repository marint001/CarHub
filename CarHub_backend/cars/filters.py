import django_filters
from .models import CarModel

class CarModelFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(
        field_name='car__brand__name',
        lookup_expr='icontains'
    )

    year = django_filters.NumberFilter(field_name='year')

    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )

    class Meta:
        model = CarModel
        fields = ['brand', 'year']