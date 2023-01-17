from django.db import models
import uuid
from Users.models import User

# Create your models here.
class Station(models.Model):
    location = models.CharField(max_length=256, null=True)
    station_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    total_vehicles = models.IntegerField(default=0)
    vehicles_parked = models.ManyToManyField("Vehicle.Vehicle")

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    from_station = models.ForeignKey("Station.Station",on_delete=models.CASCADE, related_name='from_station')
    to_station = models.ForeignKey("Station.Station",on_delete=models.CASCADE, related_name='to_station')
    vehicle = models.ForeignKey("Vehicle.Vehicle",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_datetime = models.DateTimeField()
    drop_datetime = models.DateTimeField()
    ongoing = models.BooleanField(default=True)
