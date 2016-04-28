import logging

from twilio.rest import TwilioRestClient
from zope.interface import implementer

from .interfaces import ISMSService


logger = logging.getLogger(__name__)


@implementer(ISMSService)
class TwilioService:
    """Send SMS using Twilio service."""

    def __init__(self, request):
        self.request = request

    def send_sms(self, receiver, text_body, sender, log_failure):
        """Asynchronous call to Twilio.

        We execute the actual SMS sending (calling Twilio HTTP API) in the Celery worker process, so that we do not block HTTP response head. This is especially important if we send more than one SMS message per HTTP request.
        """
        registry = self.request.registry

        account = registry.settings.get("sms.twilio_account")
        token = registry.settings.get("sms.twilio_token")

        if (not account) or (not token):
            raise RuntimeError("Missing sms.twilio_account and sms.twilio_token settings")

        logger.info("Sending Twilio SMS to: %s, body: %s", receiver, text_body)

        if account and token:
            try:
                client = TwilioRestClient(account, token)
                client.messages.create(to=receiver, from_=sender, body=text_body)
            except Exception as e:
                if log_failure:
                    logger.error("Could not send SMS from %s to %s, content %s", sender, receiver, text_body)
                    logger.exception(e)
                else:
                    raise


