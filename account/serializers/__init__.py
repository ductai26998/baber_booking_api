from rest_framework import serializers

from .address import AddressSerializer
from .salon import SalonSerializer
from .user import UserRegisterSerializer, UserSerializer


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
