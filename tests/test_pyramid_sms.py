from pytest import fixture
from pyramid.httpexceptions import HTTPOk
from pyramid.interfaces import IRequest
from pyramid import testing
from webtest import TestApp

from pyramid_sms.dummy import DummySMSService
from pyramid_sms.interfaces import ISMSService
from pyramid_sms.outgoing import send_sms


def sms_view_test(request):
    """Dummy view to simulate outgoing SMS."""

    send_sms(request, "+15551234", "Test message")

    # Check DummyService recorded this
    service = request.registry.queryAdapter(request, ISMSService)
    assert service.last_outgoing == "Test message"
    return HTTPOk()


@fixture
def sms_app(request):

    config = testing.setUp()
    config.set_default_csrf_options(require_csrf=True)
    config.add_route("test-sms", "/test-sms")
    config.add_view(sms_view_test, route_name="test-sms")
    config.registry.registerAdapter(factory=DummySMSService, required=(IRequest,), provided=ISMSService)
    config.registry.settings["sms.default_sender"] = "+15551231234"
    config.registry.settings["sms.async"] = "false"

    def teardown():
        testing.tearDown()

    app = TestApp(config.make_wsgi_app())
    return app


def test_sms(sms_app: TestApp):
    resp = sms_app.get("/test-sms")
    assert resp.status_code == 200

