"""Dummy SMS service for testing."""
from zope.interface import implementer

from .interfaces import ISMSService


@implementer(ISMSService)
class DummySMSService:

    last_outgoing = None
    outgoing_count = 0

    def __init__(self, request):
        self.request = request

    def send_sms(self, receiver: str, text_body: str, sender=None, log_failure=True):
        # Store sent information in global variables, so that tests can verify it
        DummySMSService.last_outgoing = text_body
        DummySMSService.outgoing_count += 1
