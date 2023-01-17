from .models import *
from rest_framework import serializers

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['location','station_id']

class TransactionSerializer(serializers.ModelSerializer):
    from_station = StationSerializer()
    to_station = StationSerializer()
    pickup_datetime = serializers.DateTimeField(format="%H:%M, %d-%b-%Y")
    drop_datetime = serializers.DateTimeField(format="%H:%M, %d-%b-%Y")
    class Meta:
        model = Transaction
        fields = ['from_station','to_station','vehicle','pickup_datetime','drop_datetime','ongoing']