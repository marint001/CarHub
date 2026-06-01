from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
class CarModel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='models')

    year = models.IntegerField()
    code = models.CharField(max_length=100, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    vip_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    drive = models.CharField(max_length=50, blank=True)
    fuel_tank = models.IntegerField(null=True, blank=True)
    seating_capacity = models.IntegerField(null=True, blank=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.car} {self.year}"
    
class Engine(models.Model):
    engine_type = models.CharField(max_length=255)
    horsepower = models.IntegerField()

    def __str__(self):
        return self.engine_type

class CarModelEngine(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_engine_set')
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class FeatureCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Feature Category"
        verbose_name_plural = "Feature Categories"

    def __str__(self):
        return self.name
    
class Feature(models.Model):
    category = models.ForeignKey(FeatureCategory, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class CarModelFeature(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('car_model', 'feature')

    def __str__(self):
        return f"{self.car_model} - {self.feature}"
    
class WheelDesign(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class WheelSize(models.Model):
    size_inch = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'{self.size_inch}"'
    
class Tyre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class TyreSize(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size
    
class Color(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
class WheelPackage(models.Model):
    wheel_design = models.ForeignKey(WheelDesign, on_delete=models.CASCADE)
    wheel_size = models.ForeignKey(WheelSize, on_delete=models.CASCADE)
    tyre = models.ForeignKey(Tyre, on_delete=models.CASCADE)
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f'{self.wheel_design} | '
            f'{self.wheel_size} | '
            f'{self.tyre} | '
            f'{self.tyre_size} | '
            f'{self.color}'
        )
    
class CarModelWheelPackage(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='wheel_packages')
    package = models.ForeignKey(WheelPackage, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('car_model', 'package')

    def __str__(self):
        return f'{self.car_model} - {self.package}'
    
class Transmission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModelTransmission(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_transmissions')
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car_model} - {self.transmission}"

class Brake(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Brake"
        verbose_name_plural = "Brakes"

    def __str__(self):
        return self.name

class CarModelBrake(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_brakes')
    brake = models.ForeignKey(Brake, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Car Model Brake"
        verbose_name_plural = "Car Model Brakes"

    def __str__(self):
        return f"{self.car_model} - {self.brake}"

class Exhaust(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Exhaust"
        verbose_name_plural = "Exhausts"

    def __str__(self):
        return self.name

class CarModelExhaust(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_exhausts')
    exhaust = models.ForeignKey(Exhaust, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Car Model Exhaust"
        verbose_name_plural = "Car Model Exhausts"

    def __str__(self):
        return f"{self.car_model} - {self.exhaust}"

class UsedCar(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)

class CarModelSpecification(models.Model):
    car_model = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='specs')

    interior_length = models.DecimalField(max_digits=6, decimal_places=2)
    interior_width = models.DecimalField(max_digits=6, decimal_places=2)
    interior_height = models.DecimalField(max_digits=6, decimal_places=2)

    exterior_length = models.DecimalField(max_digits=6, decimal_places=2)
    exterior_width = models.DecimalField(max_digits=6, decimal_places=2)
    exterior_height = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    customer = models.OneToOneField('accounts.CustomerProfile', on_delete=models.CASCADE, related_name='cart')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user.username} Cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey( Cart, on_delete=models.CASCADE, related_name='items')

    car_model = models.ForeignKey( CarModel, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    base_price = models.DecimalField( max_digits=12, decimal_places=2)

    total_price = models.DecimalField( max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_model}"

class CartItemConfiguration(models.Model):
    cart_item = models.OneToOneField(CartItem, on_delete=models.CASCADE, related_name='configuration')

    engine = models.ForeignKey(CarModelEngine, null=True, blank=True, on_delete=models.SET_NULL)

    transmission = models.ForeignKey(CarModelTransmission, null=True, blank=True, on_delete=models.SET_NULL)

    brake = models.ForeignKey(CarModelBrake, null=True, blank=True, on_delete=models.SET_NULL)

    exhaust = models.ForeignKey(CarModelExhaust, null=True, blank=True, on_delete=models.SET_NULL)

    wheel_package = models.ForeignKey( CarModelWheelPackage, null=True, blank=True, on_delete=models.SET_NULL)

class CartItemFeature(models.Model):
    configuration = models.ForeignKey(CartItemConfiguration, on_delete=models.CASCADE, related_name='features')

    feature = models.ForeignKey(CarModelFeature, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.feature)