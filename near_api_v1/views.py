from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import CargoFilter
from .models import Cargo, Vehicle
from .serializers import (CargoDetailSerializer, CargoListSerializer,
                          VehicleSerializer)


class CargoList(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoFilter


class CargoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer
    name = 'Cargo'


class VehicleDetail(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
