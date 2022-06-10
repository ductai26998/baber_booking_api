from base import CoreErrorCode
from django.db import models


class BookingErrorCode(CoreErrorCode):
    pass


class BookingStatus(models.TextChoices):
    NEW = "new"
    CONFIRMED = "confirmed"
    CANCEL = "cancel"
    REQUEST_TO_COMPLETE = "request_to_complete"
    COMPLETED = "completed"
