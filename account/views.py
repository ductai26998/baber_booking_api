from urllib.parse import unquote

import requests
from base.views import BaseAPIView, BaseViewSet
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from service import models as service_models

from account.serializers.user import UserUpdateSerializer

from . import AccountErrorCode, models
from .serializers import (
    AddressSerializer,
    SalonRegisterInputSerializer,
    SalonRegisterSerializer,
    SalonSerializer,
    UserRegisterInputSerializer,
    UserRegisterSerializer,
    UserSerializer,
    VerifyAccountSerializer,
)


class UserViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    serializer_map = {
        "list": UserSerializer,
        "retrieve": UserSerializer,
        "partial_update": UserUpdateSerializer,
    }
    permission_map = {
        "list": [IsAdminUser],
        "retrieve": [IsAuthenticated],
        "destroy": [IsAdminUser],
    }

    queryset = models.User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request):
        response = {
            "code": AccountErrorCode.NOT_FOUND,
            "message": "Create function is not offered in this path.",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if str(request.user.id) != pk:
            response = {
                "code": AccountErrorCode.PERMISSION_DENIED,
                "message": "Permission denied",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
            if not user:
                return Response(
                    {
                        "code": AccountErrorCode.INACTIVE,
                        "message": "User is inactive",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_active = False
            user.save()
            return Response(
                {
                    "message": "User is deactivated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Deactivation failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class UserRegister(BaseAPIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterInputSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                email = serializer.data["email"]
                account = models.User.objects.get(email=email)
                account.is_active = True
                account.save()
                token = RefreshToken.for_user(account)
                response = UserRegisterSerializer(account)
                return Response(
                    {
                        "message": "Registration successfully, check email to get otp",
                        "data": response.data,
                        "access_token": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register user failed",
                    "errors": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serializer._errors,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register user failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class VerifyOTP(BaseAPIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            instance = super().get_instance(request)
            if instance.is_verified:
                return Response(
                    {
                        "code": AccountErrorCode.VERIFY_FAIL,
                        "message": "User is verified before",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data["email"]
                otp = serializer.data["otp"]
                if instance.email != email:
                    return Response(
                        {
                            "code": AccountErrorCode.INVALID,
                            "message": "Invalid email",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if instance.otp != otp:
                    return Response(
                        {
                            "code": AccountErrorCode.INVALID,
                            "message": "OTP wrong",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                instance.is_verified = True
                instance.save()

                return Response(
                    {
                        "message": "Verification successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.VERIFY_FAIL,
                    "message": "OTP verification failed",
                    "errors": serializer._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serializer._errors,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.VERIFY_FAIL,
                    "message": "OTP verification failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class LoginWithEmailOrUsername(APIView):
    def post(self, request):
        try:
            mixin_id = request.data.get("mixin_id")
            password = request.data.get("password")

            account = models.BaseUser.objects.filter(username=mixin_id).first()
            if not account:
                account = models.BaseUser.objects.filter(email=mixin_id).first()
            if not account:
                return Response(
                    {
                        "code": AccountErrorCode.NOT_FOUND,
                        "message": "Email or username is not exist",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_true_password = check_password(password, account.password)
            if not is_true_password:
                return Response(
                    {
                        "code": AccountErrorCode.VERIFY_FAIL,
                        "message": "Password is wrong",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken.for_user(account)
            if account.is_salon:
                salon = models.Salon.objects.get(id=account.id)
                serializer = SalonSerializer(salon)
            else:
                user = models.User.objects.get(id=account.id)
                serializer = UserSerializer(user)
            return Response(
                {
                    "message": "Login successfully",
                    "data": serializer.data,
                    "access_token": str(token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.VERIFY_FAIL,
                    "message": "Login failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


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
        queryset = models.Salon.objects.filter(salon_name__icontains=search_query)

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
        response = {
            "code": AccountErrorCode.NOT_FOUND,
            "message": "Create function is not offered in this path.",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response(
                {
                    "code": AccountErrorCode.PERMISSION_DENIED,
                    "message": "Permission denied",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
            if not user:
                return Response(
                    {
                        "code": AccountErrorCode.INACTIVE,
                        "message": "User is inactive",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_active = False
            user.save()
            return Response(
                {
                    "message": "User is deactivated",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Deactivation failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class SalonRegister(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            address_url = data.get("address_url")
            if not address_url or address_url.strip() == "":
                return Response(
                    {
                        "code": AccountErrorCode.REQUIRED,
                        "message": "Address url is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serialize_account = SalonRegisterInputSerializer(data=data)
            if serialize_account.is_valid():
                serialize_account.validated_data
                serialize_account.save()
                email = serialize_account.data["email"]
                account = models.Salon.objects.get(email=email)
                account.is_salon = True
                account.is_active = True

                # create address
                address = Address()
                address.set_address_from_url(address_url)
                account_address = models.Address.objects.create(
                    address=address.address,
                    province=address.province,
                    district=address.district,
                    ward=address.ward,
                    hamlet=address.hamlet,
                    lat=address.lat,
                    lng=address.lng,
                    position_url=address.position_url,
                )

                account.address = account_address
                account.save()
                token = RefreshToken.for_user(account)
                response = SalonRegisterSerializer(account)

                return Response(
                    {
                        "message": "Registration successfully, check email to get otp",
                        "data": response.data,
                        "access_token": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register salon failed",
                    "errors": serialize_account._errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serialize_account._errors,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register salon failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class Address:
    @classmethod
    def __init__(self, *args, **kwargs):
        self.address = kwargs.get("address")
        self.province = kwargs.get("province")
        self.district = kwargs.get("district")
        self.ward = kwargs.get("ward")
        self.hamlet = kwargs.get("hamlet")
        self.lat = kwargs.get("lat")
        self.lng = kwargs.get("lng")
        self.position_url = kwargs.get("position_url")

    @classmethod
    def set_address_from_url(self, url: str):
        if not url:
            return
        self.position_url = url
        url = self.get_origin_url_from_short_url(url)
        url = unquote(url)
        url = url.replace("https://www.google.com/maps/place/", "")
        types = url.split("/")
        self.address = types[0].replace("+", " ")
        sub_addresses = self.address.split(", ")
        length_address = len(sub_addresses)
        if length_address >= 2:
            self.province = sub_addresses[-2]
            if length_address >= 3:
                self.district = sub_addresses[-3]
                if length_address >= 4:
                    self.ward = sub_addresses[-4]
                    if length_address >= 5:
                        self.hamlet = sub_addresses[-5]

        location = types[1].replace("@", "").split(",")
        self.lat = location[0]
        self.lng = location[1]

    @classmethod
    def get_origin_url_from_short_url(self, url: str):
        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True)
        return resp.url


# class AddressViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.Address.objects.all()
#     serializer_class = AddressSerializer


class AddressUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            account = request.user
            data = request.data
            address_url = data.get("address_url")
            if address_url.strip() == "":
                return Response(
                    {
                        "code": AccountErrorCode.REQUIRED,
                        "message": "Address url is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            address = Address()
            address.set_address_from_url(address_url)
            current_address = account.address

            current_address.address = address.address
            current_address.province = address.province
            current_address.district = address.district
            current_address.ward = address.ward
            current_address.hamlet = address.hamlet
            current_address.lat = float(
                address.lat,
            )
            current_address.lng = float(
                address.lng,
            )
            current_address.position_url = address.position_url
            current_address.save()

            serializer = AddressSerializer(current_address)
            return Response(
                {
                    "message": "Update address successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Update address failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


# class GetServicesOfSalon(APIView):
#     def get(self, request):
#         try:
#             salon_id = request.data.get("salon_id")
#             services = service_models.ServiceSalon.objects.filter(salon_id=salon_id)
#             # queryset = self.filter_queryset(self.get_queryset())

#             # page = self.paginate_queryset(queryset)
#             # if page is not None:
#             #     serializer = self.get_serializer(page, many=True)
#             #     return self.get_paginated_response(serializer.data)

#             # serializer = self.get_serializer(queryset, many=True)
#             # return Response(serializer.data)
#             print(services)
#             return Response(
#                 {
#                     "message": "Get services of salon successfully",
#                     "data": services,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "code": AccountErrorCode.PROCESSING_ERROR,
#                     "message": "Can not get the services of salon",
#                     "errors": e.args,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#                 exception=e,
#             )
