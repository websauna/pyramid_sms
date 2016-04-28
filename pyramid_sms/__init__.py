# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from pyramid.util import DottedNameResolver

from .interfaces import SMSConfigurationError
from .interfaces import ISMSService


def includeme(config):
    resolver = DottedNameResolver()

    service_name = config.registry.settings.get("sms.service")
    if not service_name:
        raise SMSConfigurationError("sms.service setting missing")

    service_cls = resolver.resolve(service_name)
    if not service_cls:
        raise SMSConfigurationError("Not a valid sms.service: {}".format(service_name))

    config.registry.registerAdapter(factory=service_cls, required=(IRequest,), provided=ISMSService)


