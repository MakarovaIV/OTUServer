class HTTPRequest(object):
    def __init__(self, raw_data_str):
        self.method = ""
        self.uri = ""
        self.protocol = ""
        self.headers = {}
        self.body = ""