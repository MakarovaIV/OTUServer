import urllib.parse


class HTTPRequest(object):
    def __init__(self, byte_arr):
        raw_str = str(byte_arr, 'utf-8')
        lines = raw_str.split("\r\n")
        head_line = lines[0].split(" ")

        self.method = head_line[0]
        uri = head_line[1] if len(head_line) >= 1 else ""
        query_params_index = uri.find('?')
        if query_params_index != -1:
            self.uri = urllib.parse.unquote(uri[0:query_params_index])
            self.query_params = uri[query_params_index + 1:] \
                if len(uri) > query_params_index + 1 \
                else ""
        else:
            self.uri = urllib.parse.unquote(uri)
            self.query_params = ""

        self.protocol = head_line[2] if len(head_line) >= 2 else ""
        self.headers = HTTPRequest.parse_headers(lines[1:-1])

    @staticmethod
    def parse_headers(headers):
        headers_dict = {}
        for h in headers:
            temp = h.split(":", 1)
            key = temp[0]
            if len(key) == 0:
                continue
            value = temp[1] if len(temp) >= 1 else ""
            value = value.strip()
            headers_dict[key] = value
        return headers_dict
