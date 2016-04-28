=====
Usage
=====

Setting up Twilio
-----------------

In your Pyramid ``__init__`` add:

.. code-block:: python

    config.include("pyramid_sms")



API functions
-------------

* :py:func:`pyramid_sms.outgoing.send_sms`

* :py:func:`pyramid_sms.outgoing.send_templated_sms`

* :py:func:`pyramid_sms.utils.normalize_us_phone_number`

Events
------

See :py:mod:`pyramid_sms.events`


Self-contained command line script example
------------------------------------------

No INI settings file needed, you can copy-paste into Python shell:

.. code-block:: python

    from zope.interface import implementer

    from pyramid.registry import Registry
    from pyramid.interfaces import IRequest

    from pyramid_sms.utils import normalize_us_phone_number
    from pyramid_sms.outgoing import send_sms
    from pyramid_sms.twilio import TwilioService
    from pyramid_sms.interfaces import ISMSService

    registry = Registry()
    settings = registry.settings = dict()

    # Twilio SMS number we have bought
    settings["sms.default_sender"] = "+15551231234"

    # Use Celery tasks fro async operating.
    # If true doesn't block HTTP response.
    # Requires Websauna.
    settings["sms.async"] = False

    # Account SID in Twilio account settings
    settings["sms.twilio_account"] = "xxx"

    # Auth Token in Twilio account settings
    settings["sms.twilio_token"] = "yyy"

    # Set up service backend
    registry.registerAdapter(factory=TwilioService, required=(IRequest,), provided=ISMSService)

    # Use request interface for send_sms
    @implementer(IRequest)
    class DummyRequest:
        registry = registry

    request = DummyRequest()
    to = normalize_us_phone_number("808 111 2222")
    send_sms(request, to, "Hello there")
