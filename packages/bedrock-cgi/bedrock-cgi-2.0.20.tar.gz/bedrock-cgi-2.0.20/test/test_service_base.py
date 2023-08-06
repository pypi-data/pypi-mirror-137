import os
from io import BytesIO
from unittest.mock import patch
from unittest import TestCase
import json

from bedrock_cgi.service_base import ServiceBase, REQUEST_METHOD, REQUEST_METHOD_POST
from bedrock_cgi.cgi_request import CONTENT_LENGTH, CONTENT_TYPE
from bedrock_cgi.constant import MIME_TYPE_JSON, CHARSET, CHARSET_UTF8, \
    EVENT_STATUS, EVENT_STATUS_OK, EVENT_STATUS_ERROR


# this is the actual function we want to call in the test
def handle_ok(event):
    event.ok({"OK": "OK"})


# a mockup so we can capture the response
class MockStdIO:
    def __init__(self, string:bytes = None):
        self.buffer = BytesIO() if string is None else BytesIO(string)

    def get_value(self, encoding:str = CHARSET_UTF8):
        return self.buffer.getvalue()


class TestServiceBase(TestCase):
    @staticmethod
    def _respond(request_obj: dict) -> bytes:
        os.environ[REQUEST_METHOD] = REQUEST_METHOD_POST
        os.environ[CONTENT_TYPE] = "{}; {}={}".format(MIME_TYPE_JSON, CHARSET, CHARSET_UTF8)
        request_string = json.dumps(request_obj, ensure_ascii=False).encode(CHARSET_UTF8)
        os.environ[CONTENT_LENGTH] = "{}".format(len(request_string))
        with patch("sys.stdin", new = MockStdIO(request_string)), patch("sys.stdout", new = MockStdIO()) as stdOut:
            ServiceBase.respond()
            return stdOut.get_value(CHARSET_UTF8)

    @staticmethod
    def _respond_obj(request_obj: dict) -> dict:
        response_text = TestServiceBase._respond(request_obj)
        response_text = response_text.decode(CHARSET_UTF8).split("\n\n")[1]
        return json.loads (response_text)

    def test_bedrock_cgi(self):
        assert TestServiceBase._respond_obj({"event": "ok"})[EVENT_STATUS] == EVENT_STATUS_OK
        assert TestServiceBase._respond_obj({"event": "obk"})[EVENT_STATUS] == EVENT_STATUS_ERROR
