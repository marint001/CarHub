import django_filters
from .models import CarModel, UsedCar, FuelType

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

class UsedCarFilter(django_filters.FilterSet):
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

    condition = django_filters.ChoiceFilter(
        field_name='condition',
        choices=UsedCar.Condition.choices
    )

    fuel_type = django_filters.ChoiceFilter(
        field_name='fuel_type',
        choices=FuelType.choices
    )

    class Meta:
        model = UsedCar
        fields = ['brand', 'year', 'condition', 'fuel_type']