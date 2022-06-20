from base import firebase

from .models import ConcatNotification


def send_notification_in_app(recipient, data_message):
    verb = data_message.pop("verb")
    ConcatNotification.objects.create(recipient=recipient, verb=verb, data=data_message)


def send_notify_single_recipient(recipient, data_message, in_app=True, send_push=True):
    verb = data_message.get("verb")
    if in_app:
        send_notification_in_app(recipient, data_message)
    if send_push:
        title = data_message.get("message_title", "")
        body = data_message.get("message_body", "")
        firebase.send_notify_multiple_recipient(
            recipients=[recipient],
            message_title=title,
            message_body=body,
            data_message=data_message,
        )
