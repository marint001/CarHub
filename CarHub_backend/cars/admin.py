from django.contrib import admin
from .models import Brand, Car, CarModel, Engine, CarModelEngine, FeatureCategory, Feature, Transmission, CarModelTransmission, Brake, CarModelBrake, Exhaust, CarModelExhaust

admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(Engine)
admin.site.register(CarModelEngine)
admin.site.register(FeatureCategory)
admin.site.register(Feature)
admin.site.register(Transmission)
admin.site.register(CarModelTransmission)
admin.site.register(Brake)
admin.site.register(CarModelBrake)