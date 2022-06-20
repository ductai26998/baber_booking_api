from django.db import models


class CoreErrorCode:
    INVALID = "invalid"
    NOT_FOUND = "not_found"
    NOT_SUPPORT = "not_support"
    PROCESSING_ERROR = "processing_error"
    REQUIRED = "required"
    TIMEOUT = "timeout"
    TOO_SHORT = "too_short"
    UNIQUE = "unique"
    VERIFY_FAIL = "verify_fail"
    PERMISSION_DENIED = "permission_denied"


class NotificationVerbs(models.TextChoices):
    BOOKING_PLACED = "booking_placed"
    BOOKING_CONFIRMED = "booking_confirmed"
    BOOKING_CANCELED = "booking_canceled"
    BOOKING_REQUESTED_TO_COMPLETE = "booking_requested_to_complete"
    BOOKING_COMPLETED = "booking_completed"
