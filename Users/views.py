from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import *
from django.utils import timezone
from .utils import send_otp
from django.contrib.auth import authenticate

class SendOTP(APIView):
    def post(self,request):
        mobile_number = request.data['mobile_number']
        resp = send_otp(mobile_number)
        if resp['Success']:
            otp_obj = Otp()
            otp_obj.value = resp['otp']
            otp_obj.phone_number = mobile_number
            otp_obj.save()
            return Response({'message':'OTP Sent successfully'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message':resp['error']},status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
        otp = request.data['otp']
        mobile_number = request.data['mobile_number']
        otp_objs = Otp.objects.filter(phone_number=mobile_number)
        try:
            if str(otp_objs[0].value) == str(otp) and timezone.now() < otp_objs[0].valid_upto:
                existing_user = User.objects.filter(mobile_number=mobile_number)
                if len(existing_user)==0:
                    try:
                        user_object = User()
                        first_name = request.data['first_name']
                        last_name = request.data['last_name']
                        user_object.username=mobile_number
                        user_object.mobile_number=mobile_number
                        user_object.first_name = first_name
                        user_object.last_name = last_name
                        serializer = RegisterSerializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        user_object.save()
                        user = user_object        
                    except KeyError:
                        return Response({'message':'Please enter your First Name and Last Name !!'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.get(mobile_number=mobile_number)
                refresh = RefreshToken.for_user(user)
                serializer = RegisterSerializer(user)
                Otp.objects.get(value = otp).delete()
                return Response({"success": True, "message": "Login successful",
                                'payload': serializer.data,
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'Invalid OTP'},status=status.HTTP_400_BAD_REQUEST)
        except IndexError:
            return Response({'message':'Please generate the OTP again !!'},status=status.HTTP_400_BAD_REQUEST)

class LoginAdmin(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = RegisterSerializer(user)
            return Response({"success": True, "message": "Login successful",
                            'payload': serializer.data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)