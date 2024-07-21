from django.db import models
from django.contrib.auth.models import User

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries', default=1)
    date = models.DateField()
    app_name = models.CharField(max_length=50)
    earnings = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.DecimalField(max_digits=7, decimal_places=2)
    time_spent = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)

