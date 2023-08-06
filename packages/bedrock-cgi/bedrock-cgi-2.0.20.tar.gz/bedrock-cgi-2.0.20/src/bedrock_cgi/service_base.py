import os
from .constant import STATUS_OK, STATUS_UNSUPPORTED_REQUEST_METHOD, \
    REQUEST_METHOD, REQUEST_METHOD_POST, REQUEST_METHOD_OPTIONS
from .cgi_response import respond
from .event import Event

__all__ = ["ServiceBase"]


class ServiceBase:
    @staticmethod
    def _do_post(method):
        # TODO look for a schema, validate events, and filter events
        Event().handle()

    @staticmethod
    def _do_options(method):
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS
        # TODO may want to actually check the request headers to confirm they are allowed
        respond(STATUS_OK, method)

    @staticmethod
    def _do_unsupported(method):
        # this is just a base error - if we couldn't get a workable request
        respond(STATUS_UNSUPPORTED_REQUEST_METHOD, "Unsupported Request ('{}' must be '{}' or '{}', received '{}')".format(REQUEST_METHOD, REQUEST_METHOD_POST, REQUEST_METHOD_OPTIONS, method))

    @staticmethod
    def respond():
        # we only respond to 'post' events so that HTTPS can mask exchanges, and 'options' for CORS
        switcher = {REQUEST_METHOD_POST: ServiceBase._do_post, REQUEST_METHOD_OPTIONS: ServiceBase._do_options}
        method = os.environ.get(REQUEST_METHOD, None)
        switcher.get(method, ServiceBase._do_unsupported)(method)
