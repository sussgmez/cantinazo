from django.conf import settings
from twilio.rest import Client


def send_whatsapp_message(to_number, body_text):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    if not to_number.startswith("whatsapp:"):
        to_number = "whatsapp:" + to_number

    message = client.messages.create(
        to=to_number, from_=settings.TWILIO_WHATSAPP_NUMBER, body=body_text
    )
    return message.sid
