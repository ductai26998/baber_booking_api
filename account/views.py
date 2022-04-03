from account.email import send_otp_to_email
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from . import models
from .serializers import (AddressSerializer, SalonSerializer,
                          UserRegisterSerializer, UserSerializer, VerifyAccountSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.filter()
    serializer_class = UserSerializer

    # def create(self, request):
    #     response = {'message': 'Create function is not offered in this path.'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['post'])
    # def register(self, request, *args, **kwargs):


class RegisterUserAPI(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_to_email(serializer.data["email"])
                return Response({
                    "status": 200,
                    "message": "Registration successfully, check email to get otp",
                    "data": serializer.data,
                })
            return Response({
                "status": 400,
                "message": "Register error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)

class VerifyOTPAPI(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user  = models.User.objects.get(email=email)
                if not user:
                    return Response({
                        "status": 400,
                        "message": "User is not exist",
                        "data": "invalid email",
                    })
                if user.otp != otp:
                    return Response({
                        "status": 400,
                        "message": "OTP wrong",
                        "data": "otp wrong",
                    })
                user.is_verified = True
                user.save()

                return Response({
                    "status": 200,
                    "message": "Verification successfully",
                    "data": serializer.data,
                })
            return Response({
                "status": 400,
                "message": "Error verify",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)

class SalonViewSet(viewsets.ModelViewSet):
    queryset = models.Salon.objects.filter()
    serializer_class = SalonSerializer

class RegisterSalonAPI(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_to_email(serializer.data["email"])
                return Response({
                    "status": 200,
                    "message": "Registration successfully, check email to get otp",
                    "data": serializer.data,
                })
            return Response({
                "status": 400,
                "message": "Register error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = AddressSerializer

class AddressCreate(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = AddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Create address success",
                    "data": serializer.data,
                })
            return Response({
                "status": 400,
                "message": "Create address error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)
