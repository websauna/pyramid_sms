=====
Usage
=====

Setting up addon
----------------

In your Pyramid ``__init__`` add:

.. code-block:: python

    config.include("pyramid_sms")



API functions
-------------

* :py:func:`pyramid_sms.outgoing.send_sms`

* :py:func:`pyramid_sms.outgoing.send_templated_sms`

* :py:func:`pyramid_sms.utils.normalize_us_phone_number`

* :py:func:`pyramid_sms.utils.normalize_international_phone_number`

Validators
----------

* :py:func:`pyramid_sms.validators.valid_us_phone_number`

* :py:func:`pyramid_sms.validators.valid_international_phone_number`

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

SMS login example
-----------------

`See this gist <https://gist.github.com/miohtama/69b5c365ec5e5ddd1d0b2ad2869460e8>`_ for a example how to implement Slack like "Magic link" like sign in with Websauna and Pyramid.

Testing
-------

In ``test.ini`` or relevant set up for your test cases, configure :py:class:`pyramid_sms.dummy.DummySMSService` backend according to :ref:`install`.

In your test case you can read back SMS sent to dummy backend.

Example:

.. code-block:: python


    import transaction
    from sqlalchemy.orm.session import Session

    from pyramid_sms.utils import get_sms_backend
    from splinter.driver import DriverAPI
    from websauna.system.user.models import User
    from websauna.wallet.models.confirmation import UserNewPhoneNumberConfirmation


    def test_ui_confirm_phone_number(require_phone_number, logged_in_wallet_user_browser: DriverAPI, dbsession: Session, mock_eth_service, test_request):
        """User needs a confirmed phone number before entering the wallet."""

        # Run functional tests against a Waitress web server running in another thread
        b = logged_in_wallet_user_browser
        b.find_by_css("#nav-wallet").click()

        assert b.is_element_present_by_css("#heading-new-phone-number")
        b.fill("phone_number", "+15551231234")
        b.find_by_css("button[type='submit']").click()

        # We arrived to SMS code verification page
        assert b.is_element_present_by_css("#heading-confirm-phone-number")

        # We have a notification that SMS code was sent
        assert b.is_element_present_by_css("#msg-phone-confirmation-send")

        # Peek into SMS code
        with transaction.manager:
            user = dbsession.query(User).first()
            confirmation = UserNewPhoneNumberConfirmation.get_pending_confirmation(user)
            sms_code = confirmation.other_data["sms_code"]

        # Get a dummy SMS backend that's configured in test fixtures
        backend = get_sms_backend(test_request)

        # Make sure code got out to the user
        msg = backend.get_last_message()
        assert sms_code in msg

        # Enter the code
        b.fill("code", sms_code)
        b.find_by_css("button[type='submit']").click()

        # We arrived to wallet overview
        assert b.is_element_present_by_css("#heading-wallet-overview")

        # We have a notification for phone number verified
        assert b.is_element_present_by_css("#msg-phone-confirmed")

