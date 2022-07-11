from account import models
from rest_framework import serializers


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseUser
        fields = [
            "id",
            "email",
            "username",
            "is_active",
            "is_salon",
            "is_superuser",
        ]
