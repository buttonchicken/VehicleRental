from .views import *
from django.urls import path,include

urlpatterns = [
    path('view_cars', GetParkedCars.as_view()),
    path('add', AddStation.as_view()),
    path('pickup', PickupCar.as_view()),
    path('drop', DropCar.as_view()),
]