from account import models
from rest_framework import serializers


class SalonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Salon
        fields = [
            "avatar",
            "addresses",
            "background_image",
            "default_address",
            "email",
            "is_active",
            "is_closed",
            "is_verified",
            "phone_number",
            "salon_name",
            "total_completed_booking",
            "vote_rate",
        ]
