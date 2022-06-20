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
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_PLACED,
    }

    send_notify_single_recipient(
        recipient=booking.salon,
        data_message=data_message,
    )


def send_notify_to_user_about_booking_confirmed(booking):
    message_title = "Booking was confirmed"
    message_body = (
        "The booking at %s has just been confirmed by the salon. Please come to experience their service."
        % booking.salon.salon_name
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_CONFIRMED,
    }

    send_notify_single_recipient(
        recipient=booking.user,
        data_message=data_message,
    )


def send_notify_to_salon_about_booking_canceled_by_salon(booking):
    message_title = "Booking was canceled by salon"
    message_body = (
        "The salon %s is currently unable to fulfill this booking. Sorry for the inconvenience."
        % booking.salon.salon_name
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_CANCELED,
    }

    send_notify_single_recipient(
        recipient=booking.user,
        data_message=data_message,
    )


def send_notify_to_salon_about_booking_canceled_by_user(booking):
    message_title = "Booking was canceled by user"
    message_body = "The booking of %s was canceled by user." % booking.user.username
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_CANCELED,
    }

    send_notify_single_recipient(
        recipient=booking.salon,
        data_message=data_message,
    )


def send_notify_to_salon_about_booking_requested_to_complete(booking):
    message_title = "Booking was canceled by salon"
    message_body = (
        "Please confirm that you have completed the service experience and rated the salon %s."
        % booking.salon.salon_name
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_REQUESTED_TO_COMPLETE,
    }

    send_notify_single_recipient(
        recipient=booking.user,
        data_message=data_message,
    )


def send_notify_to_salon_about_booking_completed(booking):
    message_title = "Booking was completed"
    message_body = (
        "The booking at %s was completed. Thanks for using the our services."
        % booking.salon.salon_name
    )
    timezone.activate(settings.STR_TIMEZONE)
    data_message = {
        "message_title": message_title,
        "message_body": message_body,
        "screen_redirect": "booking:%s" % booking.id,
        "sended_at": timezone.localtime(timezone.now()).strftime("%H:%M:%S %d/%m/%Y"),
        "verb": NotificationVerbs.BOOKING_COMPLETED,
    }

    send_notify_single_recipient(
        recipient=booking.user,
        data_message=data_message,
    )
