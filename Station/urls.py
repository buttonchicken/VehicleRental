from .views import *
from django.urls import path,include

urlpatterns = [
    path('add', AddStation.as_view())
]