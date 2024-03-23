from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Location(models.Model):
    zip_code = models.CharField(max_length=5, unique=True, db_index=True,
                                validators=[RegexValidator(r'^\d{5}$')])
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, db_index=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, db_index=True)

    def __str__(self):
        return self.zip_code


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, related_name='pick_up_cargos',
                                         on_delete=models.SET_NULL, null=True)
    delivery_location = models.ForeignKey(Location, related_name='delivery_cargos',
                                         on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField(default=1,
                                 validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return f"{self.pick_up_location.city} - {self.delivery_location.city}"


class Vehicle(models.Model):
    number = models.CharField(max_length=5, unique=True,
                              validators=[RegexValidator(r'^[1-9][0-9]{3}[A-Z]$')], db_index=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    payload_capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.number
