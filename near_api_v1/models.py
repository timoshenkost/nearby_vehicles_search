from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from geopy.distance import distance


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

    def get_vehicles(self, radius: int = None) -> list:
        """
         This function searches for vehicles and records their number and distance.

        Args:
        radius (int, optional): If specified, limits the search to the specified radius.

        Returns:
        List[Dict[str, Union[str, int]]]: A list of dictionaries representing vehicle data.
            Each dictionary contains the keys 'number' and 'distance', with corresponding
            values being the vehicle's number and the recorded distance to the cargo.
        """
        start_point = (self.pick_up_location.latitude, self.pick_up_location.longitude)
        vehicles = Vehicle.objects.all()
        vehicle_list = []
        # Iterate through all vehicles and record their number and distance in vehicle_list
        for vehicle in vehicles:
            vehicle_point = (vehicle.current_location.latitude, vehicle.current_location.longitude)
            dist = distance(start_point, vehicle_point).miles
            # If radius specified, limits the search
            if radius is not None and radius > dist:
                vehicle_data = {
                    'number': vehicle.number,
                    'distance': dist
                }
                vehicle_list.append(vehicle_data)

        return vehicle_list


class Vehicle(models.Model):
    number = models.CharField(max_length=5, unique=True,
                              validators=[RegexValidator(r'^[1-9][0-9]{3}[A-Z]$')], db_index=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    payload_capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.number
