from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .serializers import (AddressSerializer, SalonSerializer,
                          UserRegisterSerializer, UserSerializer,
                          VerifyAccountSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
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


class UserVerifyOTP(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = models.User.objects.get(email=email)
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

    def list(self, request):
        search_query = request.query_params.get("q", "")
        sort_query = request.query_params.get("sort", "")
        queryset = models.Salon.objects.filter(
            salon_name__icontains=search_query)

        if sort_query:
            try:
                if sort_query.startswith("-"):
                    models.Salon._meta.get_field(sort_query[1:])
                else:
                    models.Salon._meta.get_field(sort_query)
                queryset = queryset.order_by(sort_query)

            except:
                pass
        self.queryset = queryset
        return super().list(request)


class SalonRegister(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
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
