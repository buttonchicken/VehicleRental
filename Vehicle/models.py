from django.db import models
import uuid
from Station.models import Station

# Create your models here.

class Vehicle(models.Model):
    make_model = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=10)
    vehicle_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    parked_at = models.ForeignKey("Station.Station", on_delete=models.CASCADE, blank=True, null=True)
    being_used = models.BooleanField(default=False)