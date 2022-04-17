from base.serializers import MoneyField
from service import models
from rest_framework import serializers


class ServiceInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = [
            "name",
            "gender",
        ]


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = [
            "id",
            "name",
            "gender",
        ]


class ServiceSalonInputSerializer(serializers.ModelSerializer):
    price = MoneyField()

    class Meta:
        model = models.ServiceSalon
        fields = [
            "salon",
            "service",
            "price",
        ]

    # def __init__(self, *args, **kwargs):
    #     many = kwargs.pop('many', True)
    #     super(ServiceSalonInputSerializer, self).__init__(
    #         many=many, *args, **kwargs)


class ServiceSalonSerializer(serializers.ModelSerializer):
    price = MoneyField()

    class Meta:
        model = models.ServiceSalon
        fields = [
            "id",
            "service",
            "price",
        ]
        depth = 1
