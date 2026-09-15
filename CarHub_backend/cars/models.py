from django.db import models, IntegrityError, transaction
from django.core.validators import RegexValidator
from .code_generator import assign_code

# Create your models here.
class FuelType(models.TextChoices):
    PETROL = 'petrol', 'Petrol'
    DIESEL = 'diesel', 'Diesel'
    HYBRID = 'hybrid', 'Hybrid'
    PLUG_IN_HYBRID = 'plug_in_hybrid', 'Plug-in Hybrid'
    ELECTRIC = 'electric', 'Electric'

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
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    vip_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    drive = models.CharField(max_length=50, blank=True)
    fuel_tank = models.IntegerField(null=True, blank=True)
    seating_capacity = models.IntegerField(null=True, blank=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.code:
            for attempt in range(5):
                self.code = assign_code(CarModel, '001')
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    if CarModel.objects.filter(code=self.code).exists():
                        continue
                    else:   
                        raise
            raise IntegrityError("Could not assign a unique code after 5 attempts")
        else:
            super().save(*args, **kwargs)

    def compatible_accessories(self):
        return Accessory.objects.filter(
            compatibilities__car=self.car,
            compatibilities__year=self.year
        )

    def __str__(self):
        return f"{self.car} {self.year}"
    
class Engine(models.Model):
    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
        default=FuelType.PETROL
    )
    engine_type = models.CharField(max_length=255)
    horsepower = models.IntegerField()

    def __str__(self):
        return self.engine_type

class CarModelEngine(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_engine')
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class FeatureCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    display_order = models.PositiveIntegerField(default=0)

    is_configurable = models.BooleanField(
        default=False,
        help_text="Can customers choose an option from this category?"
    )
    class Meta:
        ordering = ["display_order", "name"]
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

class CarModelColor(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_model_colors')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('car_model', 'color')

    def __str__(self):
        return f"{self.car_model} - {self.color}"

class UsedCar(models.Model):
    class Condition(models.TextChoices):
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        POOR = 'poor', 'Poor'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        RESERVED = 'reserved', 'Reserved'
        SOLD = 'sold', 'Sold'

    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='used_cars')
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    condition = models.CharField(max_length=20, choices=Condition.choices)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    vin = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-HJ-NPR-Z0-9]{17}$',
                message='Enter a valid 17-character VIN in uppercase.'
            )
        ]
    )
    transmission = models.ForeignKey(
        Transmission,
        on_delete=models.PROTECT,
        related_name='used_cars'
    )
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    exterior_color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        related_name='used_cars'
    )
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.code:
            for attempt in range(5):
                self.code = assign_code(UsedCar, '002')
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    if UsedCar.objects.filter(code=self.code).exists():
                        continue
                    else:   
                        raise
            raise IntegrityError("Could not assign a unique code after 5 attempts")
        else:
            super().save(*args, **kwargs)

    def compatible_accessories(self):
        return Accessory.objects.filter(
            compatibilities__car=self.car,
            compatibilities__year=self.year
        )

    def __str__(self):
        return f"{self.code} - {self.car} {self.year} ({self.vin[-6:]})"

class UsedCarImage(models.Model):
    used_car = models.ForeignKey(UsedCar, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='used_car_images/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.used_car} image #{self.order}"

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

    unit_price = models.DecimalField( max_digits=12, decimal_places=2)

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

class CarModelImage(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.car_model} image #{self.order}"

class Accessory(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    price = models.DecimalField(
            max_digits=10,
            decimal_places=2
        )
    
    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    requires_installation = models.BooleanField(default=False)
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            for attempt in range(5):
                self.code = assign_code(Accessory, '003')
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    if Accessory.objects.filter(code=self.code).exists():
                        continue
                    else:
                        raise
            raise IntegrityError("Could not assign a unique code after 5 attempts")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

class AccessoryImage(models.Model):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accessory_images/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.accessory} image #{self.order}"

class AccessoryCompatibility(models.Model):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='compatibilities')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('accessory', 'car', 'year')
