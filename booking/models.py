from account.models import Salon, User
from base.models import MoneyField, TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils import timezone
from service.models import Service

from . import BookingStatus


class Booking(TimeStampedModel):
    updated_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(
        max_length=32, choices=BookingStatus.choices, default=BookingStatus.NEW
    )
    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )
    total_net = MoneyField(amount_field="total_net_amount", currency_field="currency")


class BookingService(TimeStampedModel):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booking_services"
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, related_name="booking_services", null=True
    )
    price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )
    price = MoneyField(amount_field="price_amount", currency_field="currency")
