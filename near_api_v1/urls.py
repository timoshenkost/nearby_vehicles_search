from django.urls import path

from .views import CargoDetail, CargoList, VehicleDetail

urlpatterns = [
    path("cargo_list/", CargoList.as_view(), name="cargo_list"),
    path("cargo/<int:pk>/", CargoDetail.as_view(), name="cargo_detail"),
    path("vehicle/<int:pk>/", VehicleDetail.as_view(), name="vehicle_detail"),
]
