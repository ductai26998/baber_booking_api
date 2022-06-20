from base.views import BaseViewSet
from notification.serializers import NotificationSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .. import NotificationErrorCode, models


class NotificationViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ConcatNotification.objects.active()
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        try:
            account = request.user
            filter_query = request.query_params.get("read", "")
            queryset = account.concat_notifications.active()
            if filter_query == "true":
                queryset = queryset.read()
            elif filter_query == "false":
                queryset = queryset.unread()
            self.queryset = queryset
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "detail": "Can not get notifications in app",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, *args, **kwargs):
        noti = self.get_object()
        if request.user.id != noti.recipient.id:
            return Response(
                {
                    "code": NotificationErrorCode.PERMISSION_DENIED,
                    "detail": "Permission denied",
                    "messages": "Permission denied",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            noti = self.get_object()
            if request.user.id != noti.recipient.id:
                return Response(
                    {
                        "code": NotificationErrorCode.PERMISSION_DENIED,
                        "detail": "Permission denied",
                        "messages": "Permission denied",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            noti.deleted = True
            noti.save(update_fields=("deleted",))
            return Response(
                {
                    "detail": "Notification was removed",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not remove the notification",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["delete"], url_path="deleteAll")
    def deleteAll(self, request, *args, **kwargs):
        try:
            models.ConcatNotification.objects.delete_all(request.user)
            return Response(
                {
                    "detail": "Removed all of notifications of you",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not remove all notifications of you",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"], url_path="markAsRead")
    def mark_as_read(self, request, *args, **kwargs):
        try:
            noti = self.get_object()
            if request.user.id != noti.recipient.id:
                return Response(
                    {
                        "code": NotificationErrorCode.PERMISSION_DENIED,
                        "detail": "Permission denied",
                        "messages": "Permission denied",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            noti.mark_as_read()
            return Response(
                {
                    "detail": "Changed status of the notification to read",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not change the notification status",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="markAllAsRead")
    def mark_all_as_read(self, request, *args, **kwargs):
        try:
            models.ConcatNotification.objects.read_all(request.user)
            return Response(
                {
                    "detail": "Changed status of all notification to read",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not change the all of notification status",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"], url_path="markAsUnread")
    def mark_as_unread(self, request, *args, **kwargs):
        try:
            noti = self.get_object()
            if request.user.id != noti.recipient.id:
                return Response(
                    {
                        "code": NotificationErrorCode.PERMISSION_DENIED,
                        "detail": "Permission denied",
                        "messages": "Permission denied",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            noti.mark_as_unread()
            return Response(
                {
                    "detail": "Changed status of the notification to unread",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not change the notification status",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="markAllAsUnread")
    def mark_all_as_unread(self, request, *args, **kwargs):
        try:
            models.ConcatNotification.objects.unread_all(request.user)
            return Response(
                {
                    "detail": "Changed status of all notification to unread",
                }
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Can not change the all of notification status",
                    "code": NotificationErrorCode.PROCESSING_ERROR,
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
