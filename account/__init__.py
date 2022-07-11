from base import CoreErrorCode
from django.db import models


class Gender(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class AccountErrorCode(CoreErrorCode):
    INACTIVE = "inactive"
