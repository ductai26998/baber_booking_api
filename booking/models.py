from account.models import Salon, User
from base.models import TimeStampedModel
from django.db import models
from base.models import MoneyField
from django.conf import settings


class Booking(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=32)
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
