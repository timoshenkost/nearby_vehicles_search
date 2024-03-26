from celery import Celery

from .models import Vehicle, Location

app = Celery('near_api_v1')


@app.task
def vehicle_locations_update():
    vehicles = Vehicle.objects.all()
    updated_vehicles = []

    for vehicle in vehicles:
        vehicle.current_location = Location.objects.order_by('?').first()
        updated_vehicles.append(vehicle)

    Vehicle.objects.bulk_update(updated_vehicles, ['current_location'])

    print(f"Vehicle locations updated")
