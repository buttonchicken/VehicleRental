from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from VehicleRental.custom_permissions import *
from rest_framework import status

# Create your views here.

class AddVehicle(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            make_model = request.data['make_model']
            reg_no = request.data['registration_no']
            v = Vehicle.objects.create(make_model=make_model, reg_no=reg_no)
            return Response({'message':'Car Created Successfully !!', 'Vehicle ID': v.vehicle_id },status=status.HTTP_202_ACCEPTED)
        except KeyError:
            return Response({'message':'Please enter make_model and registration_no of the Vehicle'},status=status.HTTP_400_BAD_REQUEST)

class AssignVehicleToStation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            vehicle_id = request.data['vehicle_id']
            station_id = request.data['station_id']
            station = Station.objects.get(station_id = station_id)
            vehicle = Vehicle.objects.get(vehicle_id = vehicle_id)
            if not vehicle.being_used:
                station.vehicles_parked.add(vehicle)
                vehicle.parked_at = station
                vehicle.save()
                station.save()
                return Response({'message':'Vehicle added to station Successfully !!', 
                                 'station_id': station.station_id , 'vehicle_id': vehicle.vehicle_id}
                                 ,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'Vehicle is being already used !!'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message':'Invalid vehicle/station ID !!'},status=status.HTTP_400_BAD_REQUEST)
