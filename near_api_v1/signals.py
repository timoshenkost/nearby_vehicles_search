import csv

from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Location


@receiver(post_migrate)
def load_data(sender, **kwargs):
    """
    Loading data from uszips.csv after migration
    """
    if sender == apps.get_app_config('near_api_v1') and not Location.objects.exists():
        objs = []
        with open('/code/near_api_v1/data/uszips.csv', 'r', encoding='UTF-8') as locations_file:
            reader = csv.DictReader(locations_file)
            # get a dictionary with data and write it to an object
            for location in reader:
                obj = Location(
                    zip_code=location['zip'],
                    city=location['city'],
                    state=location['state_id'],
                    latitude=location['lat'],
                    longitude=location['lng'],
                )
                objs.append(obj)

        if objs:
            Location.objects.bulk_create(objs, batch_size=1000)
