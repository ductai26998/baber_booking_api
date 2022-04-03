from account import models
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = "__all__"
