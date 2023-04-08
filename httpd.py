import argparse
import logging
import mimetypes
import os.path
from concurrent.futures import ThreadPoolExecutor


from server import HttpServer
from request import HTTPRequest
from response import HTTPResponse

server = None


def process_req(bytes_arr):
    req = HTTPRequest(bytes_arr)

    if req.method == "GET" or req.method == "HEAD":
        req_handler(req)
    else:
        res = HTTPResponse()
        res.status_code = 405
        res.status = "Method Not Allowed"

        server.send_resp(HTTPResponse.resp_to_bytes(res))


def req_handler(req):
    path = os.path.abspath(doc_root + req.uri)
    is_head_request = req.method == "HEAD"

    if os.path.exists(path) and "../" not in req.uri:
        if os.path.isfile(path) and not req.uri.endswith("/"):
            tmp_body = ""
            res = HTTPResponse()
            with open(path, 'rb') as data:
                tmp_body = data.read()

            _, file_extension = os.path.splitext(path)
            content_type = mimetypes.types_map[file_extension]

            res.headers["Content-Type"] = content_type
            res.headers["Content-Length"] = len(tmp_body)

            if not is_head_request:
                res.binary_body = tmp_body

            server.send_resp(HTTPResponse.resp_to_bytes(res), is_head_request)
        elif is_index(path):
            res = HTTPResponse()
            body = b'<html>Directory index file</html>\n'
            res.headers["Content-Type"] = "text/html"
            res.headers["Content-Length"] = len(body)

            if not is_head_request:
                res.binary_body = body

            server.send_resp(HTTPResponse.resp_to_bytes(res), is_head_request)
        else:
            res = HTTPResponse()
            res.status_code = 404
            res.status = "NOT FOUND"
            server.send_resp(HTTPResponse.resp_to_bytes(res), is_head_request)
    else:
        res = HTTPResponse()
        res.status_code = 404
        res.status = "NOT FOUND"
        server.send_resp(HTTPResponse.resp_to_bytes(res), is_head_request)


def is_index(path):
    if os.path.isdir(path):
        list_files = os.listdir(path)
        return 'index.html' in list_files
    else:
        return False


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-a', '--address',
                            type=str,
                            default="127.0.0.1",
                            help='Server address')
    arg_parser.add_argument('-p', '--port',
                            type=int,
                            default=8080,
                            help='Server port')
    arg_parser.add_argument('-w', '--num_of_workers',
                            type=int,
                            default=20,
                            help='Number of workers')
    arg_parser.add_argument('-r', '--doc_root',
                            type=str,
                            default='tests',
                            help='Document root')
    args = arg_parser.parse_args()

    address = args.address
    port = args.port
    num_of_workers = args.num_of_workers
    doc_root = args.doc_root

    try:
        executor = ThreadPoolExecutor(max_workers=num_of_workers)
        server = HttpServer(args.address,
                            args.port)

        server.on_new_req = lambda bytes_array: \
            executor.submit(process_req, bytes_array)
        server.connect()
    except Exception:
        logging.exception("Unexpected error")
        server.close()
    except KeyboardInterrupt:
        logging.exception("Interrupted by user")
        server.close()
