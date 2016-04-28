"""Outgoing SMS API."""

import logging
import pkg_resources

from pyramid.renderers import render
from pyramid.settings import asbool

try:
    pkg_resources.get_distribution('websauna')
    from websauna.system.http import Request
    from websauna.system.task.celery import celery_app as celery
    from websauna.system.task import RequestAwareTask
    HAS_WEBSAUNA = False
except pkg_resources.DistributionNotFound:
    from pyramid.request import Request
    HAS_WEBSAUNA = False

from .interfaces import ISMSService
from .interfaces import SMSConfigurationError
from .events import SMSSent

logger = logging.getLogger(__name__)


def _send_sms(request, receiver, text_body, sender, log_failure):
    """Perform actual SMS outbound operation through a configured service."""
    service = request.registry.queryAdapter(request, ISMSService)

    if not service:
        raise SMSConfigurationError("No SMS backend configured")

    service.send_sms(receiver, text_body, sender, log_failure)


if HAS_WEBSAUNA:
    @celery.task(base=RequestAwareTask)
    def _send_sms_async(request, receiver, from_, text_body, log_failure):
        """Celery task to send asynchronously."""
        _send_sms(request, receiver, from_, text_body, log_failure)


def send_sms(request: Request, receiver: str, text_body: str, sender: str=None, log_failure: bool=True, async: bool=None, user_dialog: bool=False):
    """Send outgoing SMS message using the default configured SMS service.

    Example:

    .. code-block:: python

        def test_sms_view(request):
            '''Dummy view to simulate outgoing SMS.'''
            send_sms(request, "+15551231234", "Test message")

    :param receiver: Receiver's phone number as international format. You should normalize this number from all user input before passing in. See :py:mod:`pyramid_sms.utils` for examples.
    :param text_body: Outbound SMS body. Usually up to 1600 characters.
    :param sender: Envelope from number. Needs to be configured in the service. If none use default configured "sms.default_from".
    :param log_failure: If there is an exception from the SMS backend then log this using Python logging system. Otherwise raise the error as an exception.
    :param async: Force asynchronous operation through task subsystem. If ``None`` respect ``sms.async`` settings. If the operation is asynchronous, this function returns instantly and does not block HTTP request due to slow API calls to a third party service.
    :param user_dialog: This SMS is part of a dialog with a known user. Use this flag to log messages with the user in your conversation dashboard. Set ``False`` to two-factor auth tokens and such.

    :raise SMSConfigurationError: If configuration settings are missing
    """
    if async is None:
        async = request.registry.settings.get("sms.async")
        if async is None:
            raise SMSConfigurationError("sms.async setting not defined")
        async = asbool(async)

    if sender is None:
        sender = request.registry.settings.get("sms.default_sender")
        if not sender:
            raise SMSConfigurationError("sms.default_sender not configured")

    # https://www.twilio.com/help/faq/sms/does-twilio-support-concatenated-sms-messages-or-messages-over-160-characters
    if len(text_body) >= 1600:
        logger.warn("Too long SMS: %s", text_body)

    logger.info("Queuing sending SMS to: %s, body: %s", receiver, text_body)

    # Put the actual Twilio operation async queue
    if async:
        if not HAS_WEBSAUNA:
            raise SMSConfigurationError("Async operations are only supported with Websauna framework")
        _send_sms_async.apply_async(args=(request, receiver, text_body, sender, log_failure,))
    else:
        _send_sms(request, receiver, text_body, sender, log_failure)

    request.registry.notify(SMSSent(request, receiver, text_body, sender, user_dialog))


def send_templated_sms(request: Request, template: str, context: dict, receiver: str, sender: str=None, log_failure: bool=True, async: bool=None, user_dialog: bool=False):
    """Send out a SMS that is constructed using a page template.

    Same as :py:meth:`pyramid_sms.outgoing.send_sms`, but uses templates instead of hardcoded messages.

    :param request: HTTP request
    :param template: Template name. Like ``welcome_sms.txt.jinja``.
    :param context: Dictionary passed to template rendering engine
    """
    text_body = render(template, context, request=request)
    send_sms(request, receiver, text_body, sender, log_failure, async, user_dialog)
