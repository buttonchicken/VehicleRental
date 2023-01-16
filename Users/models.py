from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True, primary_key=True)

class Otp(models.Model):
    value = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=10)
    # User = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    valid_upto = models.DateTimeField(blank=True)
    
    def save(self, *args, **kwargs):
        self.valid_upto = self.created_at + timedelta(minutes=1)
        super(Otp, self).save(*args, **kwargs)