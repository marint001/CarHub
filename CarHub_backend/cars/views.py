from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import CarModel
from .serializers import CarDetailSerializer, CarListSerializer
from .filters import CarModelFilter

ALLOWED_SORT_FIELDS = {
    'price': 'price',
    'year': 'year',
    'brand': 'car__brand__name',
    'model': 'car__name',
}

@api_view(['GET'])
def car_list(request):
    queryset = CarModel.objects.select_related(
        'car',
        'car__brand'
    ).all()

    filterset = CarModelFilter(request.GET, queryset=queryset)
    queryset = filterset.qs

    sort_param = request.GET.get('sort')

    if sort_param:
        descending = sort_param.startswith('-')
        field = sort_param.lstrip('-')

        if field in ALLOWED_SORT_FIELDS:
            order_field = ALLOWED_SORT_FIELDS[field]
            if descending:
                order_field = f"-{order_field}"
            queryset = queryset.order_by(order_field)
    else:
        queryset = queryset.order_by(
            'car__brand__name',
            'car__name',
            '-year'
        )

    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)

    serializer = CarListSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def car_detail(request, pk):
    car = get_object_or_404(
        CarModel.objects.select_related(
            'car',
            'car__brand'
        ).prefetch_related(
            'car_model_engine_set',
            'car_model_transmissions__transmission',
            'car_model_brakes__brake',
        ),
        pk=pk
    )

    serializer = CarDetailSerializer(
        car,
        context={'request': request}
    )
    return Response(serializer.data)