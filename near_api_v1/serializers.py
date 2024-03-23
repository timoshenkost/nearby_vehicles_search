from geopy.distance import distance
from rest_framework import serializers

from .models import Cargo, Location, Vehicle


class CargoListSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SlugRelatedField(slug_field='zip_code',
                                                    queryset=Location.objects.all())
    pick_up_city = serializers.ReadOnlyField(source='pick_up_location.city')
    delivery_location = serializers.SlugRelatedField(slug_field='zip_code',
                                                     queryset=Location.objects.all())
    delivery_city = serializers.ReadOnlyField(source='delivery_location.city')
    nearby_vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = '__all__'

    def get_nearby_vehicles(self, obj):
        start_point = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
        vehicles = Vehicle.objects.all()
        count_nearby_vehicles = 0
        # go through all vehicles and count those that are at a distance of up to 450 miles
        for vehicle in vehicles:
            vehicle_point = (vehicle.current_location.latitude, vehicle.current_location.longitude)
            dist = distance(start_point, vehicle_point).miles
            if dist <= 450:
                count_nearby_vehicles += 1

        return count_nearby_vehicles


class CargoDetailSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SlugRelatedField(slug_field='zip_code', read_only=True)
    pick_up_city = serializers.ReadOnlyField(source='pick_up_location.city')
    delivery_location = serializers.SlugRelatedField(slug_field='zip_code', read_only=True)
    delivery_city = serializers.ReadOnlyField(source='delivery_location.city')
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = '__all__'
        read_only_fields = ['pick_up_location', 'delivery_location']

    def get_vehicles(self, obj):
        start_point = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
        vehicles = Vehicle.objects.all()
        vehicle_list = []
        # iterate through all vehicles and record their number and distance in vehicle_list
        for vehicle in vehicles:
            vehicle_point = (vehicle.current_location.latitude, vehicle.current_location.longitude)
            dist = distance(start_point, vehicle_point).miles
            vehicle_data = {
                'number': vehicle.number,
                'distance': dist
            }
            vehicle_list.append(vehicle_data)

        return vehicle_list


class VehicleSerializer(serializers.ModelSerializer):
    current_location = serializers.SlugRelatedField(slug_field='zip_code',
                                                    queryset=Location.objects.all())
    current_city = serializers.ReadOnlyField(source='current_location.city')

    class Meta:
        model = Vehicle
        fields = '__all__'
