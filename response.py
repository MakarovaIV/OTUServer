class HTTPResponse(object):
    def __init__(self):
        self.protocol = "HTTP/2.0"
        self.status_code = 200
        self.status = "OK"
        self.headers = {"Content-Type": "text/html; charset=utf-8"}
        self.body = ""

    @staticmethod
    def to_str(instance):
        result = "" + instance.protocol + " " + str(instance.status_code) + " " + instance.status + "\r\n"
        result += HTTPResponse.join_headers(instance.headers)
        result += "\r\n"
        result += instance.body
        result += "\r\n"
        return result

    @staticmethod
    def join_headers(headers):
        result = ""
        for key, value in headers.items():
            result += str(key) + ": " + str(value) + "\r\n"
        return result

    @staticmethod
    def resp_to_str():
        return "HTTP/2.0 200 OK\r\nCache-Control: " \
               "max-age=0, must-revalidate, no-cache, " \
               "no-store, public, s-maxage=0\r\nCf-Cache-Status: DYNAMIC\r\n" \
               "Cf-Ray: 5ad91d75bda5cd02-EWR\r\n" \
               "Cf-Request-Id: 03bb90bd950000cd02cb1dd200000001\r\n" \
               "Content-Type: application/json\r\n" \
               "Date: Sat, 04 Jul 2020 13:15:27 GMT\r\n" \
               "Expect-Ct: max-age=604800, " \
               "report-uri=\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\"\r\n" \
               "Server: cloudflare\r\n" \
               "Set-Cookie: __cfduid=d032175648e90373f1271c27a0e5b55d71593868527; " \
               "expires=Mon, 03-Aug-20 13:15:27 GMT; path=/; " \
               "domain=.icanhazdadjoke.com; HttpOnly; SameSite=Lax\r\n" \
               "Strict-Transport-Security: max-age=15552000; " \
               "includeSubDomains\r\nX-Content-Type-Options: nosniff\r\n" \
               "X-Frame-Options: DENY\r\nX-Xss-Protection: 1; " \
               "mode=block\r\n\r\n{\r\n  \"id\":\"NZDlb299Uf\",\r\n  " \
               "\"joke\":\"Where do sheep go to get their hair cut? The baa-baa shop.\",\r\n  " \
               "\"status\":200\r\n}"
