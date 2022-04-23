from base.views import BaseAPIView, BaseViewSet
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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

    serializer_map = {"list": UserSerializer, "retrieve": UserSerializer}
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
                username = serializer.data["username"]
                account = models.User.objects.get(username=username)
                account.is_active = True
                account.save()
                token = RefreshToken.for_user(account)
                response = UserRegisterSerializer(account)
                return Response(
                    {
                        "message": "Registration successfully, check email to get otp",
                        "account": response.data,
                        "access_token": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register user failed",
                    "errors": serializer.error_messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serializer.errors,
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
                        "account": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.VERIFY_FAIL,
                    "message": "OTP verification failed",
                    "errors": serializer.error_messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serializer.errors,
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
                    "account": serializer.data,
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
            if not data.get("address"):
                return Response(
                    {
                        "status": AccountErrorCode.REQUIRED,
                        "message": "Address is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
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

                return Response(
                    {
                        "message": "Registration successfully, check email to get otp",
                        "account": response.data,
                        "access_token": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Register salon failed",
                    "errors": serialize_account.error_messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serialize_account.errors,
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
                return Response(
                    {
                        "message": "Create address successfully",
                        "account": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Create address failed",
                    "errors": serializer.error_messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=serializer.errors,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "message": "Create address failed",
                    "errors": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )
