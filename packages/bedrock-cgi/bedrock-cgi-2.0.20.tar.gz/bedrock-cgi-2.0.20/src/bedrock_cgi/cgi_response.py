import sys
from .constant import MIME_TYPE_JSON, CHARSET, CHARSET_UTF8, \
    HEADER_STATUS, HEADER_CONTENT_TYPE, \
    REQUEST_METHOD_POST, REQUEST_METHOD_OPTIONS


def respond(header_status, response, encoding: str = CHARSET_UTF8):
    def write_encoded(string: str = ""):
        sys.stdout.buffer.write("{}\n".format(string).encode(encoding))

    # print the headers...
    write_encoded(f"{HEADER_STATUS}: {header_status}")
    write_encoded(f"{HEADER_CONTENT_TYPE}: {MIME_TYPE_JSON}; {CHARSET}={CHARSET_UTF8}")
    write_encoded("X-Content-Type-Options: nosniff")
    write_encoded("Access-Control-Allow-Origin: *")
    write_encoded("Access-Control-Allow-Headers: *")
    write_encoded(f"Access-Control-Allow-Methods: {REQUEST_METHOD_POST},{REQUEST_METHOD_OPTIONS}")
    write_encoded()

    # print the response, note that it is already encoded, so from here needs to be treated as raw bytes
    write_encoded(response)

    # NOTE, no further responses should be issued after this
