import json


class HTTPRequest(object):
    def __init__(self, raw_data_str):
        lines = raw_data_str.split("\r\n")
        head_line = lines[0].split(" ")

        self.method = head_line[0]
        self.uri = head_line[1] if len(head_line) >= 1 else ""
        self.protocol = head_line[2] if len(head_line) >= 2 else ""
        self.headers = HTTPRequest.parse_headers(lines[1:-1])
        self.body = ""

    @staticmethod
    def parse_headers(headers):
        dict = {}
        for h in headers:
            temp = h.split(":", 1)
            key = temp[0]
            if len(key) == 0:
                continue
            value = temp[1] if len(temp) >= 1 else ""
            value = value.strip()
            dict[key] = value
        return dict
