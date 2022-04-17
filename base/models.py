import uuid

from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django_prices.models import MoneyField as BaseMoneyField


class TimeStampedModel(models.Model):
    objects = Manager
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class MoneyField(BaseMoneyField):
    serialize = False
