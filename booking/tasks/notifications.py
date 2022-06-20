from base import NotificationVerbs
from base.firebase import send_notify_multiple_recipient
from django.utils import timezone


def send_notify_to_user_about_booking_placed(booking):
    _send_notify_to_user_about_booking_placed(booking)
    _send_notify_to_salon_about_booking_placed(booking)


def _send_notify_to_user_about_booking_placed(booking):
    message_title = "New booking"
    message_body = (
        "You have just booked a haircut at %s. Please wait for the salon to confirm the booking."
        % booking.salon.salon_name
    )
    data_message = {
        "sended_at": timezone.now().strftime("%d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_PLACED,
    }

    send_notify_multiple_recipient(
        recipients=[booking.user],
        message_title=message_title,
        message_body=message_body,
        data_message=data_message,
    )


def _send_notify_to_salon_about_booking_placed(booking):
    message_title = "New booking"
    message_body = (
        "You have just received a booking of %s. Please confirm the booking in the booking history."
        % booking.user.username
    )
    data_message = {
        "sended_at": timezone.now(),
        "verb": NotificationVerbs.BOOKING_PLACED,
    }

    send_notify_multiple_recipient(
        recipients=[booking.salon],
        message_title=message_title,
        message_body=message_body,
        data_message=data_message,
    )
