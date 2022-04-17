from base.views import BaseAPIView, BaseViewSet
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from service import models as service_models

from . import models
from .serializers import (ServiceInputSerializer, ServiceSalonInputSerializer,
                          ServiceSalonSerializer, ServiceSerializer)
from account import models as account_models


class ServiceViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.Service.objects.filter()
    serializer_class = ServiceSerializer
    serializer_map = {
        "create": ServiceInputSerializer,
    }

    def partial_update(self, request, pk=None):
        response = {
            'message': 'Partial update function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ServiceSalonViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.ServiceSalon.objects.filter()
    # serializer_class = ServiceSalonInputSerializer
    serializer_map = {
        "list": ServiceSalonSerializer,
        "retrieve": ServiceSalonSerializer,
    }

    def list(self, request, *args, **kwargs):
        salon = request.user
        self.queryset = models.ServiceSalon.objects.filter(salon_id=salon.id)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # account = request.user
        # request.data["salon"] = account.id
        # return super().create(request, *args, **kwargs)

        account = request.user
        services = request.data
        for service_infor in services:
            service_id = service_infor.get("service")
            service_existed_in_salon = service_models.ServiceSalon.objects.filter(salon_id=account.id,
                                                                                  service_id=service_id).exists()
            if service_existed_in_salon:
                continue
            service_exist = service_models.Service.objects.filter(
                id=service_id).exists()
            if not service_exist:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Service doesn't exist",
                })
            price = service_infor.get("price")
            if not price:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Price is required",
                })
            models.ServiceSalon.objects.create(service_id=service_id, salon_id=account.id, price_amount=price.get(
                "amount"), currency=price.get("currency"))
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Create address success",
        })

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        if str(request.user.id) != instance.salon_id:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Permission denied",
            })
        return super().partial_update(request, pk)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
