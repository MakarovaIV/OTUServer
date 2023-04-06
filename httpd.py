import logging
import socket
import time


class NetworkError:
    pass


class HttpServer(object):
    def __init__(self,
                 host,
                 port,
                 socket_timeout,
                 reconnect_delay,
                 reconnect_max_attempts):
        self.host = host
        self.port = port
        self.socket_timeout = socket_timeout
        self.reconnect_delay = reconnect_delay
        self.reconnect_max_attempts = reconnect_max_attempts
        self._socket = None

    def close(self):
        self._socket.close()
        self._socket = None

    def connect(self):
        try:
            if self._socket:
                self._socket.close()
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self._socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self.host, self.port))
            self._socket.listen(1)
            # self._socket.settimeout(self.socket_timeout)
            # self._socket.connect((self.host, self.port))
            # self._socket.settimeout(None)
            while True:
                conn, _ = self._socket.accept()
                try:
                    self.handle_conn(conn)
                except Exception as e:
                    print('Client serving failed', e)
        except socket.error as e:
            raise e
        finally:
            if self._socket:
                self._socket.close()

    def handle_conn(self, conn):
        # req = self.parse_request(conn)
        # self.handle_request(req)
        data = conn.recv(1)
        if data:
            conn.sendall(bytes("HTTP/2.0 200 OK\r\nCache-Control: max-age=0, must-revalidate, no-cache, no-store, public, s-maxage=0\r\nCf-Cache-Status: DYNAMIC\r\nCf-Ray: 5ad91d75bda5cd02-EWR\r\nCf-Request-Id: 03bb90bd950000cd02cb1dd200000001\r\nContent-Type: application/json\r\nDate: Sat, 04 Jul 2020 13:15:27 GMT\r\nExpect-Ct: max-age=604800, report-uri=\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\"\r\nServer: cloudflare\r\nSet-Cookie: __cfduid=d032175648e90373f1271c27a0e5b55d71593868527; expires=Mon, 03-Aug-20 13:15:27 GMT; path=/; domain=.icanhazdadjoke.com; HttpOnly; SameSite=Lax\r\nStrict-Transport-Security: max-age=15552000; includeSubDomains\r\nX-Content-Type-Options: nosniff\r\nX-Frame-Options: DENY\r\nX-Xss-Protection: 1; mode=block\r\n\r\n{\r\n  \"id\":\"NZDlb299Uf\",\r\n  \"joke\":\"Where do sheep go to get their hair cut? The baa-baa shop.\",\r\n  \"status\":200\r\n}", 'utf-8'))
            print("Send bytes")


if __name__ == '__main__':
    try:
        serv = HttpServer('127.0.0.1', 8000, 0.1, 1, 5)
        serv.connect()
    except Exception:
        logging.exception("Unexpected error")
        serv.close()
    except KeyboardInterrupt:
        logging.exception("Interrupted by user")
        serv.close()
