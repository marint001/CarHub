from rest_framework import serializers
from .models import CarModel, CarModelEngine, Engine, CarModelFeature, Feature, FeatureCategory, CarModelWheelPackage, CarModelTransmission, CarModelBrake


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
            'features',
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

class FeatureOptionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='feature.category.name')
    name = serializers.CharField(source='feature.name')

    class Meta:
        model = CarModelFeature
        fields = [
            'id',
            'category',
            'name',
            'price',
        ]

class FeatureGroupSerializer(serializers.Serializer):
    category = serializers.CharField()
    options = FeatureOptionSerializer(many=True)

class WheelPackageOptionSerializer(serializers.ModelSerializer):
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
        ]



