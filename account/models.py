from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from . import Gender


class Address(models.Model):
    alias = models.CharField(max_length=128, blank=True,
                             null=True, help_text="Bí danh. Có thể là tên,...")
    full_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(
        max_length=1024, blank=True, null=True, help_text="Địa chỉ cụ thể")
    province = models.CharField(max_length=128, help_text="Tỉnh")
    district = models.CharField(max_length=128, help_text="Quận/huyện")
    ward = models.CharField(max_length=128, blank=True,
                            null=True, help_text="Phường/xã")
    hamlet = models.CharField(
        max_length=128, blank=True, null=True, help_text="Thôn/xóm/ấp")
    street = models.CharField(
        max_length=256, blank=True, null=True, help_text="Đường")
    latitude = models.FloatField(blank=True, null=True, help_text="Vĩ độ")
    longitude = models.FloatField(blank=True, null=True, help_text="Kinh độ")


class UserManager(BaseUserManager):
    pass


class BaseUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    total_completed_booking = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'username'


class User(BaseUser):
    address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=6, choices=Gender.choices)

    class Meta:
        ordering = ('date_joined',)


class Salon(BaseUser):
    default_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL)
    addresses = models.ManyToManyField(
        Address, blank=True, related_name="user_addresses"
    )
    salon_name = models.CharField(max_length=255, unique=True)
    background_image = models.CharField(max_length=256, null=True, blank=True)
    vote_rate = models.FloatField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_joined',)
