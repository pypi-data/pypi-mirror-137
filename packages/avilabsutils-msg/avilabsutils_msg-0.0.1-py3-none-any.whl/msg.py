import os
from twilio.rest import Client
from cprint import danger_print
import sys


error_msg = """
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE environment variables are not set. To set the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN check https://www.twilio.com/console. To set TWILIO_PHONE buy a phone number and see it on https://console.twilio.com/us1/develop/phone-numbers/.
"""

if (
    "TWILIO_ACCOUNT_SID" not in os.environ
    or "TWILIO_AUTH_TOKEN" not in os.environ
    or "TWILIO_PHONE" not in os.environ
):
    danger_print(error_msg)
    sys.exit(1)

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOK = os.environ["TWILIO_AUTH_TOKEN"]
FROMNUM = os.environ["TWILIO_PHONE"]


def sms(tonum, content):
    """Send an SMS message.

    This function will send an SMS message. It uses the Twilio API to do this, which
    means you need a Twilio account.

    Args:
        tonum: The phone number to send the SMS to. This must be in the E.164 format.
        https://www.twilio.com/docs/glossary/what-e164. A US number should be in the format -
        +12223334444.
        content: The message content.
    """
    client = Client(SID, TOK)
    client.messages.create(body=content, from_=FROMNUM, to=tonum)
