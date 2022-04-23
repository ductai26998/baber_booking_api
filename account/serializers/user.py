from account import models
from account.email import send_otp_to_email
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "id",
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
            "is_salon",
            "is_superuser",
            "first_name",
            "last_name",
        ]


class UserRegisterInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "address",
            "avatar",
            "email",
            "first_name",
            "gender",
            "last_name",
            "phone_number",
            "username",
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


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "id",
            "address",
            "avatar",
            "email",
            "first_name",
            "gender",
            "is_active",
            "last_name",
            "phone_number",
            "total_completed_booking",
            "username",
            "is_verified",
            "is_salon",
            "is_superuser",
            "first_name",
            "last_name",
        ]
