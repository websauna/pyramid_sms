from zope.interface import Interface


class SMSConfigurationError(RuntimeError):
    """Missing INI settings."""


class ISMSService(Interface):
    """SMS service interface definition.

    All SMS services get request object through creation.
    """

    def send_sms(receiver: str, text_body: str, sender=None, log_failure=True):
        """
        :param receiver: Receiver's phone number as international format
        :param text_body: Outbound SMS body. Usually up to 1024 characters.
        :param sender: Envelope from number. Needs to be configured in the service. If none use default configured "sms.default_from".
        :param log_failure: If there is an exception from the SMS backend then log this.
        :param async: Force asynchronous operation through task subsystem. If ``None`` respect ``sms.async`` settings.
        """

