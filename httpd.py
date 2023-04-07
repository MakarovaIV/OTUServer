import logging
from threading import Thread

from server import HttpServer
from request import HTTPRequest
from response import HTTPResponse

server = None


def process_req(str):
    req = HTTPRequest(str)
    if req.method == "GET":
        res = HTTPResponse()
        res.body = "<html>" \
                   "<body>" \
                   "<h1>Hello, World!</h1>" \
                   "</body>" \
                   "</html>"
        server.send_resp(HTTPResponse.to_str(res))
        # server.send_resp(HTTPResponse.resp_to_str())


def handle_req_str(req_str):
    thread = Thread(target=process_req, args=(req_str,))
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

