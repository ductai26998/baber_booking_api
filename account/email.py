import random
from django.core.mail import send_mail
from django.conf import settings
from . import models


def send_otp_to_email(email: str):
    subject = "Mã xác thực tài khoản BB"
    otp = str(random.randint(100000, 999999))
    message = "Mã xác thực của bạn là %s" % otp
    from_email = settings.EMAIL_HOST
    # send_mail(subject, message, from_email, [email])
    user = models.User.objects.get(email=email)
    user.otp = otp
    user.save()
