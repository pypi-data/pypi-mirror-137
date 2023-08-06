import typing

from django.conf import settings
from twilio.rest import Client


class TwilioProviderWrapper:
    # Client() Rely on env variable to determine the Twilio SID/Token
    client = Client()

    def send_message(self, phone_number: typing.Text, verification_code: typing.Text):
        if settings.TWILIO_MESSAGING_SERVICE_ID:
            self.client.messages.create(
                body=f"{verification_code} is your verification code.",
                messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_ID,
                to=phone_number,
            )
        else:
            self.client.verify.services(
                settings.OTP_TWILIO_SERVICE
            ).verifications.create(
                to=phone_number, custom_code=verification_code, channel="sms"
            )
