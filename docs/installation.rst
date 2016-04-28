.. highlight:: shell

============
Installation
============

Installing Python package
-------------------------

Python 3.x required.

At the command line:

.. code-block:: console

    pip install "pyramid_sms[twilio]"

Configuring outbound SMS with Twilio
------------------------------------

In your Pyramid ``INI`` settings you can have

.. code-block:: ini

    # Choose your SMS backend
    sms.service = pyramid_sms.twilio.TwilioService

    # Use this in test.ini for your unit test run
    # sms.service = pyramid_sms.dummy.DummySMSService

    # Twilio SMS number we have bought
    sms.default_sender = +555123123

    # Use Celery tasks fro async operating.
    # If true doesn't block HTTP response.
    # Requires Websauna.
    sms.async = false

    # Account SID in Twilio account settings
    sms.twilio_account = xxx

    # Auth Token in Twilio account settings
    sms.twilio_token = yyy
