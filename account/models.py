from typing import Any

from base.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Gender


class Address(TimeStampedModel):
    alias = models.CharField(
        max_length=128, blank=True, null=True, help_text="Bí danh. Có thể là tên,..."
    )
    address = models.CharField(
        max_length=1024, blank=True, null=True, help_text="Địa chỉ cụ thể"
    )
    province = models.CharField(max_length=128, blank=True, null=True, help_text="Tỉnh")
    city = models.CharField(
        max_length=128, blank=True, null=True, help_text="Thành phố"
    )
    district = models.CharField(max_length=128, help_text="Quận/huyện")
    ward = models.CharField(
        max_length=128, blank=True, null=True, help_text="Phường/xã"
    )
    hamlet = models.CharField(
        max_length=128, blank=True, null=True, help_text="Thôn/xóm/ấp"
    )
    street = models.CharField(max_length=256, blank=True, null=True, help_text="Đường")
    latitude = models.FloatField(blank=True, null=True, help_text="Vĩ độ")
    longitude = models.FloatField(blank=True, null=True, help_text="Kinh độ")


class UserManager(BaseUserManager):
    pass


class UserQueryset(models.QuerySet):
    def filter(self: models.QuerySet, *args: Any, **kwargs: Any) -> models.QuerySet:
        # if "type" is not in kwargs, default: hide orders with type RETURN
        if all(key.startswith("is_active") is False for key in kwargs.keys()):
            kwargs["is_active"] = True
        return super().filter(*args, **kwargs)

    def all(self) -> models.QuerySet:
        # Hidden type: RETURN
        return self.filter()


class BaseUser(AbstractUser, TimeStampedModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        blank=True,
        null=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_completed_booking = models.PositiveIntegerField(default=0)
    is_salon = models.BooleanField(default=False)
    address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    objects = UserQueryset.as_manager()
    USERNAME_FIELD = "username"


class User(BaseUser):
    gender = models.CharField(
        max_length=6, choices=Gender.choices, blank=True, null=True
    )

    class Meta:
        ordering = ("date_joined",)


class Salon(BaseUser):
    salon_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    background_image = models.CharField(max_length=256, null=True, blank=True)
    vote_rate = models.FloatField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    description = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        ordering = ("date_joined",)
