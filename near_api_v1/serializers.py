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
        count_nearby_vehicles = len(obj.get_vehicles(radius=450))
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
        vehicle_list = obj.get_vehicles()
        return vehicle_list


class VehicleSerializer(serializers.ModelSerializer):
    current_location = serializers.SlugRelatedField(slug_field='zip_code',
                                                    queryset=Location.objects.all())
    current_city = serializers.ReadOnlyField(source='current_location.city')

    class Meta:
        model = Vehicle
        fields = '__all__'
