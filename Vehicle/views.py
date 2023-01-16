from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from VehicleRental.custom_permissions import *
from rest_framework import status

# Create your views here.

class AddCar(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isadmin]
    def post(self,request):
        try:
            make_model = request.user['make_model']
            reg_no = request.user['registration_no']
            c = Vehicle.objects.create(make_model=make_model, reg_no=reg_no)
            return Response({'message':'Car Created Successfully !!', 'car_id': c.station_id },status=status.HTTP_202_ACCEPTED)
        except KeyError:
            return Response({'message':'Please enter make_model and registration_no of the Vehicle'},status=status.HTTP_400_BAD_REQUEST)