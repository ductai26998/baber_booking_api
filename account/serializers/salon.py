from account import models
from account.email import send_otp_to_email
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
            "username",
        ]


class SalonRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Salon
        fields = [
            "default_address",
            "avatar",
            "email",
            "salon_name",
            "phone_number",
            "username",
            "is_verified",
            "otp",
            "password",
        ]

    def save(self, **kwargs):
        super().save(**kwargs)

        password = self.validated_data['password']
        instance = self.instance
        instance.set_password(password)
        instance.save()
        email = self.validated_data['email']
        send_otp_to_email(instance, email)
