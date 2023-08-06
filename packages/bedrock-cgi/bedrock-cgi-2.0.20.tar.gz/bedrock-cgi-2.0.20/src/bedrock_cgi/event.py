import json
import time
import inspect
import types
import typing

from .constant import *
from .cgi_request import CgiRequest
from .cgi_response import respond

__all__ = ["Event"]

"""
Common Gateway Interface - this joins the Server Base and event handling of the Java version of
Bedrock.
"""


class Event:
    def __init__(self):
        self.query = CgiRequest.get_query()
        self.startTime = time.time_ns()

    def _respond(self, status: str, response_name: str, response: typing.Union[list, dict, str]):
        bedrock_response = {EVENT_STATUS: status, EVENT_QUERY: self.query, EVENT_RESPONSE_TIME_NS: time.time_ns() - self.startTime}
        if response is not None:
            bedrock_response[response_name] = response
        respond(STATUS_OK, json.dumps(bedrock_response, ensure_ascii=False))

    def ok(self, response: typing.Union[list, dict, str]):
        self._respond(EVENT_STATUS_OK, EVENT_RESPONSE, response)

    def error(self, description: typing.Union[list, dict, str]):
        self._respond(EVENT_STATUS_ERROR, EVENT_STATUS_ERROR, description)

    def handle(self, call_frame: types.FrameType = None):
        try:
            if self.query is not None:
                if EVENT in self.query:
                    event_name = str(self.query[EVENT])
                    event_handler = f"handle_{event_name.lower()}"

                    # find the call frame that includes the handler function we are looking for
                    if call_frame is None:
                        # get the globals from the top-level calling frame
                        frame = inspect.currentframe()
                        while (event_handler not in frame.f_globals) and (frame.f_back is not None):
                            frame = frame.f_back
                        call_frame = frame.f_globals

                    # if we found the handler, let's do it
                    if event_handler in call_frame:
                        # the handler is expected to call cgi.ok or cgi.error on the instance
                        call_frame[event_handler](self)
                    else:
                        self.error(f"No handler found for '{EVENT}' ({event_name})")
                else:
                    self.error(f"Missing '{EVENT}'")
        except Exception as exception:
            self.error_on_exception(exception)

    def error_on_exception(self, exception: BaseException):
        trace = [f"({type(exception).__name__}) {exception}"]
        tb = exception.__traceback__
        while tb is not None:
            trace.append(f"({tb.tb_frame.f_code.co_name}) {tb.tb_frame.f_code.co_filename}, line {tb.tb_lineno}")
            tb = tb.tb_next
        self.error(trace)
