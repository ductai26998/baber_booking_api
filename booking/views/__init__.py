from functools import reduce

from account import models as account_models
from base.views import BaseViewSet
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .. import BookingErrorCode, models
from ..serializers import BookingCreateInputSerializer, BookingSerializer


class BookingViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.Booking.objects.filter()
    serializer_class = BookingSerializer
    serializer_map = {
        "create": BookingCreateInputSerializer,
    }

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            salon_id = data["salon_id"]
            service_ids = data["service_ids"]
            salon = account_models.Salon.objects.filter(id=salon_id).first()
            if not salon:
                return Response(
                    {
                        "code": BookingErrorCode.NOT_FOUND,
                        "messages": "The salon %s is not found" % salon_id,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            salon_services = salon.services.filter(service__in=service_ids)
            for service_id in service_ids:
                if service_id not in [
                    str(salon_service.service.id) for salon_service in salon_services
                ]:
                    return Response(
                        {
                            "code": BookingErrorCode.NOT_FOUND,
                            "messages": "The salon has not a service with id=%s"
                            % service_id,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            total_net_amount = reduce(
                lambda x, y: x + y,
                [salon_service.price_amount for salon_service in salon_services],
                0,
            )
            booking = models.Booking.objects.create(
                user_id=user.id, salon=salon, total_net_amount=total_net_amount
            )
            booking_services = []

            for salon_service in salon_services:
                booking_services.append(
                    models.BookingService(
                        booking=booking,
                        service=salon_service.service,
                    )
                )
            models.BookingService.objects.bulk_create(booking_services)
            response = BookingSerializer(booking)
            return Response(
                {
                    "detail": "Create booking successful",
                    "data": response.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "code": BookingErrorCode.PROCESSING_ERROR,
                    "detail": "Create booking failed",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
