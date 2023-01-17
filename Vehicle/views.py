from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from VehicleRental.custom_permissions import *
from rest_framework import status
from django.db import IntegrityError

# Create your views here.

class AddVehicle(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            make_model = request.data['make_model']
            reg_no = request.data['registration_no']
            c = Vehicle.objects.create(make_model=make_model, reg_no=reg_no)
            return Response({'message':'Car Created Successfully !!', 'car_id': c.vehicle_id },status=status.HTTP_202_ACCEPTED)
        except KeyError:
            return Response({'message':'Please enter make_model and registration_no of the Vehicle'},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'message':'Registration Number already exists !!'},status=status.HTTP_400_BAD_REQUEST)

class AssignVehicleToStation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            vehicle_id = request.data['vehicle_id']
            station_id = request.data['station_id']
            try:
                vehicle = Vehicle.objects.get(vehicle_id = vehicle_id)
                station = Station.objects.get(station_id = station_id)
            except:
                return Response({'message':'Invalid station/vehicle ID !!'},status=status.HTTP_400_BAD_REQUEST)
            if not vehicle.being_used and vehicle not in station.vehicles_parked.all():
                station.vehicles_parked.add(vehicle)
                temp = int(station.total_vehicles)
                temp+=1
                station.total_vehicles = temp
                vehicle.parked_at = station
                vehicle.being_used = False
                vehicle.save()
                station.save()
                return Response({'message':'Vehicle Assigned Successfully !!', 'Vehicle ID': vehicle.vehicle_id,
                                 'Station ID': station.station_id },status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'Vehicle currently being used or already assigned to this station !!'}
                             ,status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message':'Please enter make_model and registration_no of the Vehicle'}
                             ,status=status.HTTP_400_BAD_REQUEST)