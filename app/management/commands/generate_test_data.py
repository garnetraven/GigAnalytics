from django.core.management.base import BaseCommand
from app.models import Delivery
from django.contrib.auth.models import User
from datetime import date
import random

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        user = User.objects.get(id=1)
        apps = ['Spark Delivery', 'Amazon Flex', 'DoorDash', 'Instacart']
        for i in range(100):
            Delivery.objects.create(
                user=user,
                date=date(2024, random.randint(1, 12), random.randint(1, 28)),
                app_name=random.choice(apps),
                earnings=random.uniform(10.0, 100.0),
                expenses=random.uniform(5.0, 50.0),
                mileage=random.uniform(1.0, 10.0),
                time_spent=random.uniform(0.5, 5.0),
                description='Test delivery record {}'.format(i)
            )
        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))

