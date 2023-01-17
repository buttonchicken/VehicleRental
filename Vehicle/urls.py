from .views import *
from django.urls import path,include

urlpatterns = [
    path('add', AddVehicle.as_view()),
    path('assignstation', AssignVehicleToStation.as_view())
]