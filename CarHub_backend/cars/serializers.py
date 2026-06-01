from rest_framework import serializers
from .models import (CarModel, CarModelEngine, Engine, CarModelFeature, Feature, FeatureCategory, CarModelWheelPackage, CarModelTransmission, CarModelBrake, Transmission, Brake, CarModelExhaust, Exhaust,
                     CartItemFeature, CartItemConfiguration, CartItem)


class CarListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='car.brand.name')
    model = serializers.CharField(source='car.name')
    display_price = serializers.SerializerMethodField()
    vip_price = serializers.SerializerMethodField()
    is_vip_visible = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = [
            'id',
            'brand',
            'model',
            'year',
            'display_price',
            'vip_price',
            'is_vip_visible',
        ]

    def get_display_price(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return obj.price

        user = request.user

        if user.is_staff:
            return {
                'price': obj.price,
                'vip_price': obj.vip_price
            }

        if user.groups.filter(name='VIP').exists():
            return obj.vip_price

        return obj.price
    
    def get_vip_price(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return None

        user = request.user

        if user.is_staff or user.groups.filter(name='VIP').exists():
            return obj.vip_price

        return None
    
    def get_is_vip_visible(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        user = request.user
        return user.is_staff or user.groups.filter(name='VIP').exists()
    
class EngineOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='engine.engine_type')

    class Meta:
        model = CarModelEngine
        fields = ['id', 'name', 'price']

class TransmissionOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='transmission.name')

    class Meta:
        model = CarModelTransmission
        fields = [
            'id',
            'name',
            'price'
        ]

class BrakeOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='brake.name')

    class Meta:
        model = CarModelBrake
        fields = [
            'id',
            'name',
            'price'
        ]

class ExhaustOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='exhaust.name')

    class Meta:
        model = CarModelExhaust
        fields = [
            'id',
            'name',
            'price'
        ]

class FeatureOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id')
    category = serializers.CharField(source='feature.category.name')
    name = serializers.CharField(source='feature.name')

    class Meta:
        model = CarModelFeature
        fields = ['id', 'category', 'name', 'price', 'vip_price']

class FeatureGroupSerializer(serializers.Serializer):
    category = serializers.CharField()
    options = FeatureOptionSerializer(many=True)

class WheelPackageOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id')

    wheel_design = serializers.CharField(source='package.wheel_design.name')
    wheel_size = serializers.CharField(source='package.wheel_size.size_inch')
    tyre = serializers.CharField(source='package.tyre.name')
    tyre_size = serializers.CharField(source='package.tyre_size.size')
    color = serializers.CharField(source='package.color.name')

    class Meta:
        model = CarModelWheelPackage
        fields = [
            'id',
            'wheel_design',
            'wheel_size',
            'tyre',
            'tyre_size',
            'color',
            'price',
            'vip_price'
        ]
    
class CarDetailSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='car.brand.name')
    model = serializers.CharField(source='car.name')

    engines = EngineOptionSerializer(
        source='car_model_engine_set',
        many=True
    )

    transmissions = TransmissionOptionSerializer(
        source='car_model_transmissions',
        many=True
    )

    brakes = BrakeOptionSerializer(
        source='car_model_brakes',
        many=True
    )

    exhausts = ExhaustOptionSerializer(
        source='car_model_exhausts',
        many=True
    )

    wheels = WheelPackageOptionSerializer(
    source='wheel_packages',
    many=True
    )

    features = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = [
            'id',
            'brand',
            'model',
            'year',
            'price',
            'vip_price',
            'engines',
            'transmissions',
            'brakes',
            'exhausts',
            'features',
            'wheels'
        ]

    def get_features(self, obj):
        feature_qs = obj.car_model_features.select_related(
            'feature',
            'feature__category'
        )

        grouped = {}

        for item in feature_qs:
            category = item.feature.category.name

            if category not in grouped:
                grouped[category] = []

            grouped[category].append(item)

        return [
            {
                'category': category,
                'options': FeatureOptionSerializer(options, many=True).data
            }
            for category, options in grouped.items()
        ]

class CarConfigurationSerializer(serializers.Serializer):
    car_model_id = serializers.IntegerField()

    engine_id = serializers.IntegerField(required=False)
    transmission_id = serializers.IntegerField(required=False)
    brake_id = serializers.IntegerField(required=False)
    exhaust_id = serializers.IntegerField(required=False)
    wheel_package_id = serializers.IntegerField(required=False)

    feature_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

class AddToCartSerializer(serializers.Serializer):
    car_model_id = serializers.IntegerField()

    engine_id = serializers.IntegerField(required=False)
    transmission_id = serializers.IntegerField(required=False)
    brake_id = serializers.IntegerField(required=False)
    exhaust_id = serializers.IntegerField(required=False)
    wheel_package_id = serializers.IntegerField(required=False)

    feature_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    quantity = serializers.IntegerField(default=1)

class CartFeatureSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='feature.feature.name')

    class Meta:
        model = CartItemFeature
        fields = ['id', 'name']

class CartConfigurationSerializer(serializers.ModelSerializer):

    engine = serializers.CharField(
        source='engine.engine.engine_type',
        read_only=True
    )

    transmission = serializers.CharField(
        source='transmission.transmission.name',
        read_only=True
    )

    brake = serializers.CharField(
        source='brake.brake.name',
        read_only=True
    )

    exhaust = serializers.CharField(
        source='exhaust.exhaust.name',
        read_only=True
    )

    wheel = serializers.SerializerMethodField()

    features = CartFeatureSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = CartItemConfiguration
        fields = [
            'engine',
            'transmission',
            'brake',
            'exhaust',
            'wheel',
            'features',
        ]

    def get_wheel(self, obj):
        if not obj.wheel_package:
            return None

        package = obj.wheel_package.package

        return (
            f"{package.wheel_size.size}\" "
            f"{package.wheel_design.shape}"
        )

class CartItemSerializer(serializers.ModelSerializer):

    car = serializers.SerializerMethodField()

    configuration = CartConfigurationSerializer(
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'car',
            'quantity',
            'base_price',
            'total_price',
            'configuration',
        ]

    def get_car(self, obj):
        return (
            f"{obj.car_model.car.brand.name} "
            f"{obj.car_model.car.name} "
            f"{obj.car_model.year}"
        )
    
class UpdateCartQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)