from django.contrib import admin
from .models import (Brand, Car, CarModel, Engine, CarModelEngine, FeatureCategory, Feature, Transmission, CarModelTransmission, Brake, CarModelBrake, Exhaust, CarModelExhaust, CarModelWheelPackage,
                      WheelPackage, WheelDesign, Tyre, WheelSize, TyreSize, Color, CarModelFeature, CarModelSpecification, CarModelImage, UsedCar, UsedCarImage, Accessory, AccessoryImage, AccessoryCompatibility)


class CarModelImageInline(admin.TabularInline):
    model = CarModelImage
    extra = 1


class CarModelAdmin(admin.ModelAdmin):
    inlines = [CarModelImageInline]

    list_display = (
        'id',
        'code',
        'car',
        'year',
        'cost',
        'vip_price',
        'price',
    )

    list_filter = (
        'car__brand__name',
        'year',
    )

    search_fields = (
        'code',
        'car__name',
        'car__brand__name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


class UsedCarImageInline(admin.TabularInline):
    model = UsedCarImage
    extra = 1


class UsedCarAdmin(admin.ModelAdmin):
    inlines = [UsedCarImageInline]

    list_display = (
        'id',
        'code',
        'car',
        'year',
        'cost',
        'vip_price',
        'price',
        'status',
        'condition',
    )

    list_filter = (
        'status',
        'condition',
        'fuel_type',
        'car__brand__name',
    )

    search_fields = (
        'code',
        'vin',
        'car__name',
        'car__brand__name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


class AccessoryImageInline(admin.TabularInline):
    model = AccessoryImage
    extra = 1


class AccessoryCompatibilityInline(admin.TabularInline):
    model = AccessoryCompatibility
    extra = 1


class AccessoryAdmin(admin.ModelAdmin):
    inlines = [AccessoryImageInline, AccessoryCompatibilityInline]

    list_display = (
        'id',
        'code',
        'name',
        'price',
        'vip_price',
        'requires_installation',
        'installation_fee',
    )

    list_filter = (
        'requires_installation',
    )

    search_fields = (
        'code',
        'name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand',
        'name',
    )

    list_filter = (
        'brand',
    )

    search_fields = (
        'name',
        'brand__name',
    )


class EngineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'engine_type',
        'fuel_type',
        'horsepower',
    )

    list_filter = (
        'fuel_type',
    )

    search_fields = (
        'engine_type',
    )


class CarModelEngineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'engine',
        'price',
    )

    list_filter = (
        'engine__fuel_type',
    )

    search_fields = (
        'car_model__car__name',
        'engine__engine_type',
    )


class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'display_order',
        'is_configurable',
    )

    list_filter = (
        'is_configurable',
    )

    search_fields = (
        'name',
    )


class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
        'category__name',
    )


class TransmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class CarModelTransmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'transmission',
        'price',
    )

    list_filter = (
        'transmission',
    )

    search_fields = (
        'car_model__car__name',
        'transmission__name',
    )


class BrakeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class CarModelBrakeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'brake',
        'price',
    )

    list_filter = (
        'brake',
    )

    search_fields = (
        'car_model__car__name',
        'brake__name',
    )


class ExhaustAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class CarModelExhaustAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'exhaust',
        'price',
    )

    list_filter = (
        'exhaust',
    )

    search_fields = (
        'car_model__car__name',
        'exhaust__name',
    )


class WheelDesignAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class WheelSizeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'size_inch',
    )


class TyreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class TyreSizeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'size',
    )

    search_fields = (
        'size',
    )


class ColorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'hex_code',
    )

    search_fields = (
        'name',
    )


class WheelPackageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'wheel_design',
        'wheel_size',
        'tyre',
        'tyre_size',
        'color',
    )

    list_filter = (
        'wheel_design',
        'wheel_size',
    )

    search_fields = (
        'wheel_design__name',
        'tyre__name',
    )


class CarModelWheelPackageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'package',
        'price',
    )

    search_fields = (
        'car_model__car__name',
    )


class CarModelFeatureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'feature',
        'price',
    )

    list_filter = (
        'feature__category',
    )

    search_fields = (
        'car_model__car__name',
        'feature__name',
    )


class CarModelSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car_model',
        'interior_length',
        'interior_width',
        'interior_height',
        'exterior_length',
        'exterior_width',
        'exterior_height',
    )

    search_fields = (
        'car_model__car__name',
    )


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(UsedCar, UsedCarAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(CarModelEngine, CarModelEngineAdmin)
admin.site.register(FeatureCategory, FeatureCategoryAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(CarModelTransmission, CarModelTransmissionAdmin)
admin.site.register(Brake, BrakeAdmin)
admin.site.register(CarModelBrake, CarModelBrakeAdmin)
admin.site.register(Exhaust, ExhaustAdmin)
admin.site.register(CarModelExhaust, CarModelExhaustAdmin)
admin.site.register(CarModelWheelPackage, CarModelWheelPackageAdmin)
admin.site.register(WheelPackage, WheelPackageAdmin)
admin.site.register(WheelDesign, WheelDesignAdmin)
admin.site.register(Tyre, TyreAdmin)
admin.site.register(WheelSize, WheelSizeAdmin)
admin.site.register(TyreSize, TyreSizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(CarModelFeature, CarModelFeatureAdmin)
admin.site.register(CarModelSpecification, CarModelSpecificationAdmin)