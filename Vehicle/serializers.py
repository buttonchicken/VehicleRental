from .models import Vehicle
from rest_framework import serializers

class VisibleCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['make_model']