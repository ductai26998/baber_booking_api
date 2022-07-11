from rest_framework import serializers

from .. import models


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConcatNotification
        fields = [
            "id",
            "verb",
            "unread",
            "data",
        ]
        depth = 1
