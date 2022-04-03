from account import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "address",
            "avatar",
            "email",
            "first_name",
            "gender",
            "is_active",
            "is_verified",
            "last_name",
            "phone_number",
            "total_completed_booking",
            "username",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "address",
            "avatar",
            "email",
            "first_name",
            "gender",
            "is_active",
            "is_verified",
            "last_name",
            "phone_number",
            "total_completed_booking",
            "username",
            "is_verified",
            "otp",
        ]
