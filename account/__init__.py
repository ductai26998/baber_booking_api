from django.db import models

class Gender(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"