from rest_framework import generics

from .models import Cargo, Vehicle
from .serializers import CargoListSerializer, CargoDetailSerializer, VehicleSerializer


class CargoList(generics.ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CargoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer
    name = 'Cargo'

class VehicleDetail(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
