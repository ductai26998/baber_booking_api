from account.serializers.user import UserUpdateSerializer
from base.views import BaseAPIView, BaseViewSet
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import (
    UserRegisterInputSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from . import AccountErrorCode, models


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
