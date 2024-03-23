import random
import string

from django.core.management.base import BaseCommand

from near_api_v1.models import Location, Vehicle


def create_vehicle_number():
    """
    Creates a random vehicle number consisting of a number from 1000 to 9999 and
     a random uppercase letter of the English alphabet at the end.
    :return: random vehicle number
    """
    min_number = 1000
    max_number = 9999

    number = random.randint(min_number, max_number)
    letter = random.choice(string.ascii_uppercase)

    vehicle_number = f"{number}{letter}"
    return vehicle_number


class Command(BaseCommand):
    help = 'Creates random vehicle instances in the database'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, nargs='?', default=1,
                            help='The number of vehicles to create in the database')

    def handle(self, *args, **options):
        count = options['count']
        for _ in range(count):
            # create random fields
            number = create_vehicle_number()
            location = Location.objects.order_by('?').first()
            payload_capacity = random.randint(1, 1000)
            while Vehicle.objects.filter(number=number).exists():
                number = create_vehicle_number()
            # create vehicle
            Vehicle.objects.create(
                number=number,
                current_location=location,
                payload_capacity=payload_capacity
            )
        self.stdout.write(self.style.SUCCESS('Vechicles created successfully'))
