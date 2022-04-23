from base.views import BaseAPIView, BaseViewSet
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from .serializers import (AddressSerializer, SalonRegisterInputSerializer,
                          SalonRegisterSerializer, SalonSerializer,
                          UserRegisterInputSerializer, UserRegisterSerializer,
                          UserSerializer, VerifyAccountSerializer)


class UserViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    serializer_map = {
        "list": UserSerializer,
        "retrieve": UserSerializer
    }
    permission_map = {
        "list": [IsAdminUser],
        "retrieve": [IsAuthenticated],
        "destroy": [IsAdminUser],
    }

    queryset = models.User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Permission denied",
            })
        return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
            if not user:
                return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "User is inactive",
            })
            user.is_active = False
            user.save()
            return Response({
                    "status": status.HTTP_200_OK,
                    "message": "User is deactivated",
                })
        except Exception as e:
            print(e)


class UserRegister(BaseAPIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterInputSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                username = serializer.data["username"]
                account = models.BaseUser.objects.get(username=username)
                account.is_active = True
                account.save()
                token = RefreshToken.for_user(account)
                response = UserRegisterSerializer(account)
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Registration successfully, check email to get otp",
                    "data": response.data,
                    "access_token": str(token.access_token),
                })
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Register error",
                "data": serializer.errors,
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": e,
            })


class VerifyOTP(BaseAPIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            instance = super().get_instance(request)
            if instance.is_verified:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "User is verified before",
                })
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                if instance.email != email:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid email",
                    })
                if instance.otp != otp:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "OTP wrong",
                    })
                instance.is_verified = True
                instance.save()

                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Verification successfully",
                    "data": serializer.data,
                })
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error verify",
                "errors": serializer.errors,
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": e,
            })


class LoginWithEmailOrUsername(APIView):
    def post(self, request):
        try:
            mixin_id = request.data.get("mixin_id")
            password = request.data.get("password")

            account = models.BaseUser.objects.filter(username=mixin_id).first()
            if not account:
                account = models.BaseUser.objects.filter(
                    email=mixin_id).first()
            if not account:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Email or username is not exist",
                })

            is_true_password = check_password(password, account.password)
            if not is_true_password:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
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
                "status": status.HTTP_200_OK,
                "message": "Login successfully",
                "data": serializer.data,
                "access_token": str(token.access_token),
            })
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": e,
            })


class SalonViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.Salon.objects.filter()
    serializer_class = SalonSerializer
    permission_map = {
        "destroy": [IsAdminUser],
    }

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

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Permission denied",
            })
        return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
            if not user:
                return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "User is inactive",
            })
            user.is_active = False
            user.save()
            return Response({
                    "status": status.HTTP_200_OK,
                    "message": "User is deactivated",
                })
        except Exception as e:
            print(e)

class SalonRegister(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            if not data.get("address"):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Address is required",
                })
            address_data = data.pop("address")
            serialize_account = SalonRegisterInputSerializer(data=data)
            serialize_address = AddressSerializer(data=address_data)
            if serialize_account.is_valid() and serialize_address.is_valid():
                serialize_account.validated_data
                serialize_account.save()
                username = serialize_account.data["username"]
                account = models.Salon.objects.get(username=username)
                account.is_salon = True
                account.is_active = True

                serialize_address.validated_data
                address = serialize_address.save()
                account.address = address
                account.save()
                token = RefreshToken.for_user(account)
                response = SalonRegisterSerializer(account)

                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Registration successfully, check email to get otp",
                    "data": response.data,
                    "access_token": str(token.access_token),
                })
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Register error",
                "data": serialize_account.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": e,
            })


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Address.objects.all()
    serializer_class = AddressSerializer


class AddressCreate(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = AddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Create address success",
                    "data": serializer.data,
                })
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Create address error",
                "data": serializer.errors,
            })
        except Exception as e:
            print(e)
