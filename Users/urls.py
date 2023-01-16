from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('send_otp', SendOTP.as_view()),
    path('login', Login.as_view()),
    path('login_admin', LoginAdmin.as_view()),
]