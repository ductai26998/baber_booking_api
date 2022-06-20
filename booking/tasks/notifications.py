from base import NotificationVerbs
from django.conf import settings
from django.utils import timezone
from notification.tasks import send_notify_single_recipient


def send_notify_to_user_about_booking_placed(booking):
    _send_notify_to_user_about_booking_placed(booking)
    _send_notify_to_salon_about_booking_placed(booking)


def _send_notify_to_user_about_booking_placed(booking):
    message_title = "New booking"
    message_body = (
        "You have just booked a haircut at %s. Please wait for the salon to confirm the booking."
        % booking.salon.salon_name
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_PLACED,
    }

    send_notify_single_recipient(
        recipient=booking.user,
        data_message=data_message,
    )


def _send_notify_to_salon_about_booking_placed(booking):
    message_title = "New booking"
    message_body = (
        "You have just received a booking of %s. Please confirm the booking in the booking history."
        % booking.user.username
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_PLACED,
    }

    send_notify_single_recipient(
        recipient=booking.salon,
        data_message=data_message,
    )
