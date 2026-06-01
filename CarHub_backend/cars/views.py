from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import (CarModel, CarModelEngine, CarModelFeature, FeatureCategory, CarModelWheelPackage, CarModelTransmission, CarModelBrake, CarModelExhaust,
                    Cart, CartItem, CartItemConfiguration, CartItemFeature)
from .serializers import CarDetailSerializer, CarListSerializer, CarConfigurationSerializer, AddToCartSerializer, CartItemSerializer, UpdateCartQuantitySerializer
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
            'car_model_exhausts__exhaust',
            'car_model_features__feature__category',
            'wheel_packages__package__wheel_design',
            'wheel_packages__package__wheel_size',
            'wheel_packages__package__tyre',
            'wheel_packages__package__tyre_size',
            'wheel_packages__package__color',
        ),
        pk=pk
    )

    serializer = CarDetailSerializer(
        car,
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['POST'])
def calculate_configuration(request):
    serializer = CarConfigurationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    try:
        car = CarModel.objects.get(id=data['car_model_id'])
    except CarModel.DoesNotExist:
        return Response({"error": "Invalid car model"}, status=404)

    total_price = car.price
    breakdown = []

    # Engine
    if 'engine_id' in data:
        engine = CarModelEngine.objects.get(id=data['engine_id'], car_model=car)
        total_price += engine.price
        breakdown.append({
            "type": "engine",
            "name": engine.engine.engine_type,
            "price": engine.price
        })

    # Transmission
    if 'transmission_id' in data:
        transmission = CarModelTransmission.objects.get(
            id=data['transmission_id'],
            car_model=car
        )
        total_price += transmission.price
        breakdown.append({
            "type": "transmission",
            "name": transmission.transmission.name,
            "price": transmission.price
        })

    # Brake
    if 'brake_id' in data:
        brake = CarModelBrake.objects.get(id=data['brake_id'], car_model=car)
        total_price += brake.price
        breakdown.append({
            "type": "brake",
            "name": brake.brake.name,
            "price": brake.price
        })

    # Exhaust
    if 'exhaust_id' in data:
        exhaust = CarModelExhaust.objects.get(id=data['exhaust_id'], car_model=car)
        total_price += exhaust.price
        breakdown.append({
            "type": "exhaust",
            "name": exhaust.exhaust.name,
            "price": exhaust.price
        })

    # Wheels
    if 'wheel_package_id' in data:
        wheel = CarModelWheelPackage.objects.get(
            id=data['wheel_package_id'],
            car_model=car
        )
        total_price += wheel.price
        breakdown.append({
            "type": "wheel",
            "name": str(wheel.package),
            "price": wheel.price
        })

    # Features
    if 'feature_ids' in data:
        features = CarModelFeature.objects.filter(
            id__in=data['feature_ids'],
            car_model=car
        )

        for f in features:
            total_price += f.price
            breakdown.append({
                "type": "feature",
                "name": f.feature.name,
                "price": f.price
            })

    return Response({
        "car_model": str(car),
        "base_price": car.price,
        "total_price": total_price,
        "breakdown": breakdown
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    customer = request.user.customer_profile

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    car = CarModel.objects.get(id=data['car_model_id'])

    total_price = car.price

    engine = None
    transmission = None
    brake = None
    exhaust = None
    wheel = None

    # Engine
    if 'engine_id' in data:
        engine = CarModelEngine.objects.get(
            id=data['engine_id'],
            car_model=car
        )
        total_price += engine.price

    # Transmission
    if 'transmission_id' in data:
        transmission = CarModelTransmission.objects.get(
            id=data['transmission_id'],
            car_model=car
        )
        total_price += transmission.price

    # Brake
    if 'brake_id' in data:
        brake = CarModelBrake.objects.get(
            id=data['brake_id'],
            car_model=car
        )
        total_price += brake.price

    # Exhaust
    if 'exhaust_id' in data:
        exhaust = CarModelExhaust.objects.get(
            id=data['exhaust_id'],
            car_model=car
        )
        total_price += exhaust.price

    # Wheels
    if 'wheel_package_id' in data:
        wheel = CarModelWheelPackage.objects.get(
            id=data['wheel_package_id'],
            car_model=car
        )
        total_price += wheel.price

    # Features
    features = []

    if 'feature_ids' in data:
        features = CarModelFeature.objects.filter(
            id__in=data['feature_ids'],
            car_model=car
        )

        for f in features:
            total_price += f.price

    cart_item = CartItem.objects.create(
        cart=cart,
        car_model=car,
        quantity=data['quantity'],
        base_price=car.price,
        total_price=total_price
    )

    config = CartItemConfiguration.objects.create(
        cart_item=cart_item,
        engine=engine,
        transmission=transmission,
        brake=brake,
        exhaust=exhaust,
        wheel_package=wheel
    )

    for feature in features:
        CartItemFeature.objects.create(
            configuration=config,
            feature=feature
        )

    return Response({
        "message": "Added to cart successfully"
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):

    customer = request.user.customer_profile

    try:
        cart = Cart.objects.prefetch_related(
            'items__configuration__features__feature__feature',
            'items__configuration__engine__engine',
            'items__configuration__transmission__transmission',
            'items__configuration__brake__brake',
            'items__configuration__exhaust__exhaust',
            'items__car_model__car__brand',
        ).get(customer=customer)

    except Cart.DoesNotExist:
        return Response({
            "items": [],
            "cart_total": 0
        })

    items = cart.items.all()

    serializer = CartItemSerializer(items, many=True)

    cart_total = items.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    return Response({
        "items": serializer.data,
        "cart_total": cart_total
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):

    customer = request.user.customer_profile

    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__customer=customer
        )

    except CartItem.DoesNotExist:
        return Response(
            {"error": "Cart item not found"},
            status=404
        )

    cart_item.delete()

    return Response({
        "message": "Item removed from cart"
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request, item_id):

    serializer = UpdateCartQuantitySerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    quantity = serializer.validated_data['quantity']

    customer = request.user.customer_profile

    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__customer=customer
        )

    except CartItem.DoesNotExist:
        return Response(
            {"error": "Cart item not found"},
            status=404
        )

    cart_item.quantity = quantity

    # IMPORTANT
    # multiply stored single-item total
    single_price = (
        cart_item.total_price / cart_item.quantity
    )

    cart_item.total_price = single_price * quantity

    cart_item.save()

    return Response({
        "message": "Quantity updated",
        "quantity": cart_item.quantity,
        "total_price": cart_item.total_price
    })