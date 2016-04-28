=====
Usage
=====

Setting up Twilio
-----------------

In your Pyramid init add:

.. code-block:: python

    from pyramid_sms.twilio import TwilioSMSService
    from pyramid_sms.interfaces import ISMSService
    from pyramid.interfaces import IRequest


    config.registry.registerAdapter(factory=TwilioSMSService, required=(IRequest,), provided=ISMSService)

API functions
-------------

* :py:func:`pyramid_sms.outgoing.send_sms`

* :py:func:`pyramid_sms.outgoing.send_templated_sms`

* :py:func:`pyramid_sms.utils.normalize_us_phone_number`

Events
------

See :py:mod:`pyramid_sms.events`
