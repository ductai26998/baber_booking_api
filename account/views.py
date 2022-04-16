from base.views import BaseAPIView
from core import ResponseStatusCode
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from .serializers import (AddressSerializer, SalonRegisterSerializer,
                          SalonSerializer, UserRegisterSerializer,
                          UserSerializer, VerifyAccountSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_ResponseStatusCode.ERROR_BAD_REQUEST)


class UserRegister(BaseAPIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                username = serializer.data["username"]
                account = models.BaseUser.objects.get(username=username)
                account.is_active = True
                account.save()
                token = RefreshToken.for_user(account)
                return Response({
                    "status": ResponseStatusCode.SUCCESS,
                    "message": "Registration successfully, check email to get otp",
                    "data": serializer.data,
                    "access_token": str(token.access_token),
                })
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Register error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)


class UserVerifyOTP(BaseAPIView):
    @transaction.atomic
    def post(self, request):
        # super().post(request)
        try:
            super().post(request)
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                account = models.BaseUser.objects.get(email=email)
                if not account:
                    return Response({
                        "status": ResponseStatusCode.ERROR,
                        "message": "User is not exist",
                        "data": "invalid email",
                    })
                if account.otp != otp:
                    return Response({
                        "status": ResponseStatusCode.ERROR,
                        "message": "OTP wrong",
                        "data": "otp wrong",
                    })
                account.is_verified = True
                account.save()

                return Response({
                    "status": ResponseStatusCode.SUCCESS,
                    "message": "Verification successfully",
                    "data": serializer.data,
                })
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Error verify",
                "data": serializer.errors,
            })
        except Exception as e:
            return Response({
                "status": ResponseStatusCode.ERROR,
                "errors": e,
            })


class LoginWithEmailOrUsername(APIView):
    def post(self, request):
        mixin_id = request.data.get("mixin_id")
        password = request.data.get("password")

        account = models.BaseUser.objects.filter(username=mixin_id).first()
        if not account:
            account = models.BaseUser.objects.filter(email=mixin_id).first()
        if not account:
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Email or username is not exist",
            })

        is_true_password = check_password(password, account.password)
        if not is_true_password:
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Password is wrong",
            })

        token = RefreshToken.for_user(account)
        if account.is_salon:
            salon = models.Salon.objects.get(id=account.id)
            serializer = SalonSerializer(salon)
        else:
            user = models.User.objects.get(id=account.id)
            serializer = UserSerializer(user)
        return Response({
            "status": ResponseStatusCode.SUCCESS,
            "message": "Login successfully",
            "data": serializer.data,
            "access_token": str(token.access_token),
        })


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
            serializer = SalonRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                username = serializer.data["username"]
                account = models.Salon.objects.get(username=username)
                account.is_salon = True
                account.is_active = True
                account.save()
                token = RefreshToken.for_user(account)
                return Response({
                    "status": ResponseStatusCode.SUCCESS,
                    "message": "Registration successfully, check email to get otp",
                    "data": serializer.data,
                    "access_token": str(token.access_token),
                })
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Register error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)


class SalonVerifyOTP(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                salon = models.Salon.objects.get(email=email)
                if not salon:
                    return Response({
                        "status": ResponseStatusCode.ERROR,
                        "message": "Salon is not exist",
                        "data": "invalid email",
                    })
                if salon.otp != otp:
                    return Response({
                        "status": ResponseStatusCode.ERROR,
                        "message": "OTP wrong",
                        "data": "otp wrong",
                    })
                salon.is_verified = True
                salon.save()

                return Response({
                    "status": ResponseStatusCode.SUCCESS,
                    "message": "Verification successfully",
                    "data": serializer.data,
                })
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Error verify",
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
                    "status": ResponseStatusCode.SUCCESS,
                    "message": "Create address success",
                    "data": serializer.data,
                })
            return Response({
                "status": ResponseStatusCode.ERROR,
                "message": "Create address error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)
