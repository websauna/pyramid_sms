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

Configuring Twilio
------------------

In your Pyramid ``INI`` settings you can have

.. code-block:: console

    # Twilio SMS number we have bought
    sms.default_sender = +555123123

    # Use Celery tasks fro async operating.
    # If true doesn't block HTTP response.
    # Requires Websauna.
    sms.async = false

    # Account SID in Twilio account settings
    sms.twilio_accout = xxx

    # Auth Token in Twilio account settings
    sms.twilio_token = yyy
