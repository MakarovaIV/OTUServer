from datetime import datetime


class HTTPResponse(object):
    def __init__(self):
        self.protocol = "HTTP/1.0"
        self.status_code = 200
        self.status = "OK"
        self.headers = {"Content-Type": "text/html; charset=utf-8",
                        "Content-Length": 0,
                        "Date": datetime.now().strftime('%a, %d %b %Y '
                                                        '%H:%M:%S GMT'),
                        "Server": "OtuServer",
                        "Connection": "close"
                        }
        self.binary_body = b''

    @staticmethod
    def resp_to_bytes(instance):
        result = "" + instance.protocol + " " \
                 + str(instance.status_code) + " " \
                 + instance.status + "\r\n"
        result += HTTPResponse.join_headers(instance.headers)
        result += "\r\n"
        result = result.encode()

        if len(instance.binary_body) > 0:
            result += instance.binary_body

        return result

    @staticmethod
    def join_headers(headers):
        result = ""
        for key, value in headers.items():
            result += str(key) + ": " + str(value) + "\r\n"
        return result
