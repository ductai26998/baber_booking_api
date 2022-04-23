from account import models
from account.email import send_otp_to_email
from rest_framework import serializers


class SalonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Salon
        fields = [
            "id",
            "avatar",
            "background_image",
            "address",
            "email",
            "is_active",
            "is_closed",
            "is_verified",
            "phone_number",
            "salon_name",
            "total_completed_booking",
            "vote_rate",
            "username",
            "first_name",
            "last_name",
            "is_salon",
            "is_superuser",
        ]


class SalonRegisterInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Salon
        fields = [
            "avatar",
            "email",
            "salon_name",
            "phone_number",
            "username",
            "first_name",
            "last_name",
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


class SalonRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Salon
        fields = [
            "id",
            "avatar",
            "email",
            "salon_name",
            "phone_number",
            "username",
            "is_verified",
            "address",
            "first_name",
            "last_name",
            "is_salon",
            "is_superuser",
        ]
