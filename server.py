import socket


class HttpServer(object):
    def __init__(self,
                 host,
                 port,
                 socket_timeout,
                 reconnect_delay,
                 reconnect_max_attempts,
                 on_new_req):
        self.host = host
        self.port = port
        self.socket_timeout = socket_timeout
        self.reconnect_delay = reconnect_delay
        self.reconnect_max_attempts = reconnect_max_attempts
        self._socket = None
        self.conn = None
        self.on_new_req = on_new_req
        self.max_len = 1024

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
            while True:
                conn, _ = self._socket.accept()
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
        # data = conn.recv(1)
        data = b''
        while True:
            if len(data) > self.max_len:
                break
            byte = conn.recv(1)
            data += byte
            if len(data) > 3:
                rn = data[-4:]
                if "\r\n\r\n" in str(rn, 'utf-8'):
                    break
        self.on_new_req(str(data, 'utf-8'))

    def send_resp(self, resp_data):
        if resp_data:
            self.conn.sendall(bytes(resp_data, 'utf-8'))
            print("Send bytes")
