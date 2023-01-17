from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from VehicleRental.custom_permissions import *
from rest_framework import status
from Vehicle.serializers import VisibleCarSerializer
from Vehicle.models import *
from datetime import datetime

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
            cars_parked = station_obj.vehicles_parked.all()
            cars_parked_data = VisibleCarSerializer(cars_parked, many=True).data
            return Response({'Cars Available':cars_parked_data},status=status.HTTP_200_OK)
        except:
            return Response({'message':'Invalid Station'},status=status.HTTP_400_BAD_REQUEST)

class PickupCar(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        vehicle_id = request.data['vehicle_id']
        station_id = request.data['station_id']
        try:
            station = Station.objects.get(station_id = station_id)
            vehicle = Vehicle.objects.get(vehicle_id = vehicle_id)
        except:
            return Response({'message':'Invalid station/vehicle ID !!'},status=status.HTTP_400_BAD_REQUEST)
        #Checking whether the car is parked at the station to be picked up from
        if vehicle.parked_at!=station:
            print("a")
            return Response({'message':'Vehicle not available !!'},status=status.HTTP_400_BAD_REQUEST)
        #Checking whether the vehicle is not being used currently
        if not vehicle.being_used or not len(Transaction.objects.filter(vehicle=vehicle,ongoing=True))>0:
            print("b")
            station.vehicles_parked.remove(vehicle)
            temp = station.total_vehicles 
            if temp==0:
                temp=0
            else:
                temp -=1
            station.total_vehicles = temp
            vehicle.parked_at = None
            vehicle.being_used = True
            vehicle.save()
            station.save()
            t = Transaction.objects.create(from_station = station, vehicle = vehicle,
                                       user = request.user, pickup_datetime = datetime.now(),
                                       ongoing = True)
            return Response({'message':'Car picked up succesfully','Transaction ID':t.transaction_id },status=status.HTTP_200_OK)
        return Response({'message':'Vehicle not available !!'},status=status.HTTP_400_BAD_REQUEST)

class DropCar(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        vehicle_id = request.data['vehicle_id']
        station_id = request.data['station_id']
        station = Station.objects.get(station_id = station_id)
        vehicle = Vehicle.objects.get(vehicle_id = vehicle_id)
        if vehicle.being_used:
            t_obj = Transaction.objects.get(vehicle = vehicle, user = request.user, ongoing = True)
            t_obj.to_station = station
            t_obj.drop_datetime = datetime.now()
            t_obj.ongoing = False
            t_obj.save()
            vehicle.being_used = False
            vehicle.parked_at = station
            vehicle.save()
            temp = station.total_vehicles
            temp+=1
            station.vehicles_parked.add(vehicle)
            station.save()
            return Response({ 'message':'Car dropped successfully','Transaction ID':t_obj.transaction_id },status=status.HTTP_200_OK)
        return Response({'message':'Vehicle not being used !!'},status=status.HTTP_400_BAD_REQUEST)
