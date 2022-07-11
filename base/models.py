import uuid
from typing import Any

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField, Manager
from django.utils import timezone
from django_prices.models import MoneyField as BaseMoneyField


class MoneyField(BaseMoneyField):
    serialize = False


class TimeStampedModel(models.Model):
    objects = Manager
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Photo(TimeStampedModel):
    url = models.URLField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class ModelWithMetadata(models.Model):
    private_metadata = JSONField(
        blank=True, null=True, default=dict, encoder=DjangoJSONEncoder
    )
    metadata = JSONField(blank=True, null=True, default=dict, encoder=DjangoJSONEncoder)

    class Meta:
        abstract = True

    def get_value_from_private_metadata(self, key: str, default: Any = None) -> Any:
        if not self.private_metadata:
            return default
        return self.private_metadata.get(key, default)

    def store_value_in_private_metadata(self, items: dict):
        if not self.private_metadata:
            self.private_metadata = {}
        self.private_metadata.update(items)

    def clear_private_metadata(self):
        self.private_metadata = {}

    def delete_value_from_private_metadata(self, key: str):
        if key in self.private_metadata:
            del self.private_metadata[key]

    def get_value_from_metadata(self, key: str, default: Any = None) -> Any:
        if not self.metadata:
            return default
        return self.metadata.get(key, default)

    def store_value_in_metadata(self, items: dict):
        if not self.metadata:
            self.metadata = {}
        self.metadata.update(items)

    def clear_metadata(self):
        self.metadata = {}

    def delete_value_from_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]
