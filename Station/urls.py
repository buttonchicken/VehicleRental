from .views import *
from django.urls import path,include

urlpatterns = [
    path('add', AddStation.as_view()),
    path('pickupcar', PickupCar.as_view()),
    path('dropcar', DropCar.as_view())
]