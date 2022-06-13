from account.serializers.salon import SalonBaseViewSerializer
from account.serializers.user import UserBaseViewSerializer
from base.serializers import MoneyField
from booking import models
from rest_framework import serializers


class BookingServiceSerializer(serializers.ModelSerializer):
    price = MoneyField()

    class Meta:
        model = models.BookingService
        fields = [
            "id",
            "service",
            "price",
        ]
        depth = 1


class BookingSerializer(serializers.ModelSerializer):
    total_net = MoneyField()
    booking_services = BookingServiceSerializer(many=True, read_only=True)
    user = UserBaseViewSerializer(read_only=True)
    salon = SalonBaseViewSerializer(read_only=True)

    class Meta:
        model = models.Booking
        fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "salon",
            "status",
            "total_net",
            "booking_services",
        ]
        depth = 1


class BookingCreateInputSerializer(serializers.Serializer):
    salon_id = serializers.CharField()
    service_ids = serializers.ListField(child=serializers.CharField())
