import codecs
import os
import sys
import json
from typing import Optional

from .constant import MIME_TYPE_JSON, CHARSET, CHARSET_UTF8, STATUS_BAD_REQUEST, CONTENT_TYPE, CONTENT_LENGTH
from .cgi_response import respond

__all__ = ["CgiRequest"]


class CgiRequest:
    @staticmethod
    def _is_json() -> bool:
        content_type = os.environ.get(CONTENT_TYPE, None)
        if content_type is not None:
            return content_type.split(";", 1)[0].strip() == MIME_TYPE_JSON
        return False

    @staticmethod
    def _charset(default_encoding: str = CHARSET_UTF8) -> str:
        content_type = os.environ.get(CONTENT_TYPE, None)
        if content_type is not None:
            split_result = content_type.split(";", 1)
            if len(split_result) == 2:
                parameters = {}
                for parameter in split_result[1].split(";"):
                    attribute, parameters[attribute] = parameter.split("=")
                if CHARSET in parameters:
                    # technically the attribute value could be a quoted string that we should parse...
                    return str(parameters[CHARSET]).strip(" '\"\t\r\n")
        # return the default if no charset is passed. though not technically correct according to
        # standards, most characters we encounter here will be the same in UTF-8 as ASCII or
        # ISO-8859-1 (Western Latin 1)
        return default_encoding

    @staticmethod
    def get_query() -> Optional[dict]:
        # the type must be JSON
        if CgiRequest._is_json():
            # the length must be specified
            content_length = int(os.environ.get(CONTENT_LENGTH, 0))
            if content_length > 0:
                input_stream = codecs.getreader(CgiRequest._charset())(sys.stdin.buffer)
                input_json = input_stream.read(content_length)
                return json.loads(input_json)
        # this is just a base error - if we couldn't get a workable request
        respond(STATUS_BAD_REQUEST, f"Bad Request ({CONTENT_TYPE} must be {MIME_TYPE_JSON}, and {CONTENT_LENGTH} > 0)")
        return None
