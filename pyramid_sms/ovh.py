import logging

try:
    import ovh
except:
    pass

from zope.interface import implementer

from .interfaces import ISMSService


logger = logging.getLogger(__name__)


@implementer(ISMSService)
class OvhService:
    """Send SMS using Ovh service."""

    def __init__(self, request):
        self.request = request

    def send_sms(self, receiver, text_body, sender, log_failure):
        """Asynchronous call to Ovh.

        We execute the actual SMS sending (calling Ovh HTTP API) in the Celery worker process, so that we do not block HTTP response head. This is especially important if we send more than one SMS message per HTTP request.
        """
        registry = self.request.registry

        application_key = registry.settings.get("sms.ovh_application_key")
        application_secret = registry.settings.get("sms.ovh_application_secret")
        consumer_key = registry.settings.get("sms.ovh_consumer_key")
        endpoint = registry.settings.get("sms.ovh_endpoint") or 'ovh-eu'
        has_settings = None not in (application_key, application_secret, consumer_key)
        if not has_settings:
            raise RuntimeError("Missing sms.ovh_application_key, sms.ovh_application_secret"
                               " and sms.ovh_consumer_key settings")

        logger.info("Sending OVH SMS to: %s, body: %s", receiver, text_body)

        if has_settings:
            try:
                client = ovh.Client(
                    endpoint,
                    application_key=application_key,
                    application_secret=application_secret,
                    consumer_key=consumer_key)
                ck = client.new_consumer_key_request()
                ck.add_recursive_rules(ovh.API_READ_WRITE, "/sms")
                res = client.get('/sms')
                url = '/sms/' + res[0] + '/jobs/'
                client.post(url,
                    charset='UTF-8',
                    coding='7bit',
                    message=text_body,
                    noStopClause=False,
                    priority='high',
                    receivers= [receiver],
                    senderForResponse=False,
                    validityPeriod=2880,
                    sender=sender
                )
            except Exception as e:
                if log_failure:
                    logger.error("Could not send SMS from %s to %s, content %s", sender, receiver, text_body)
                    logger.exception(e)
                else:
                    raise
