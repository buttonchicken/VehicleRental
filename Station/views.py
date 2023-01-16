from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from VehicleRental.custom_permissions import *
from rest_framework import status
from Vehicle.serializers import VisibleCarSerializer

# Create your views here.

class AddStation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            location = request.data['location']
            s = Station.objects.create(location=location)
            return Response({'message':'Station Created Successfully !!', 'station_id': s.station_id },status=status.HTTP_202_ACCEPTED)
        except KeyError:
            return Response({'message':'Please enter location of the station'},status=status.HTTP_400_BAD_REQUEST)

class GetParkedCars(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        station_id = request.data['station_id']
        try:
            station_obj = Station.objects.get(station_id=station_id)
            cars_parked = station_obj.cars_parked.all()
            cars_parked_data = VisibleCarSerializer(cars_parked, many=True)
            return Response({'Cars Available':cars_parked_data},status=status.HTTP_200_OK)
        except:
            return Response({'message':'Invalid Station'},status=status.HTTP_400_BAD_REQUEST)

class AddCarToStation(models.Model):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]