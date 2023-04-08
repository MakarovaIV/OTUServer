import socket


class HttpServer(object):
    def __init__(self,
                 host,
                 port):
        self.host = host
        self.port = port
        self.socket_timeout = 1
        self.reconnect_delay = 1
        self.reconnect_max_attempts = 5
        self._socket = None
        self.conn = None
        self.on_new_req = None
        self.max_len = 1024 * 1024

    def close(self):
        self._socket.close()
        self._socket = None

    def connect(self):
        try:
            if self._socket:
                self._socket.close()
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self.host, self.port))
            self._socket.listen(1)
            while True:
                conn, _ = self._socket.accept()
                conn.settimeout(self.socket_timeout)
                self.conn = conn
                try:
                    self.listen_data(conn)
                except Exception as e:
                    print('Client serving failed', e)
        except socket.error as e:
            raise e
        finally:
            if self._socket:
                self._socket.close()

    def listen_data(self, conn):
        data = b''
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(1024)
            data += chunk
            if not chunk:
                raise ConnectionError
        self.on_new_req(data)

    def send_resp(self, resp_data, close_con=False):
        if resp_data:
            self.conn.sendall(resp_data)
            if close_con:
                self.conn.close()
