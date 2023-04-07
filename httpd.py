import logging
from threading import Thread

from server import HttpServer
from request import HTTPRequest
from response import HTTPResponse

server = None


def process_req(str):
    req = HTTPRequest(str)
    if req.method == "":
        res = HTTPResponse()
        server.send_resp(res.resp_to_str())


def handle_req_str(str):
    thread = Thread(target=process_req, args=(str,))
    thread.start()


if __name__ == '__main__':
    try:
        server = HttpServer('127.0.0.1', 8000, 0.1, 1, 5, handle_req_str)
        server.connect()
    except Exception:
        logging.exception("Unexpected error")
        server.close()
    except KeyboardInterrupt:
        logging.exception("Interrupted by user")
        server.close()

