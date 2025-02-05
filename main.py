import socket
import time
import pandas as pd
import io

# from router import requests_distributor
# from router import api
from routes import api


class WebServer:
    def __init__(self, host, port, requests_distributor_func):
        self.requests_distributor_func = requests_distributor_func
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        print(f'Create server on http://{host}:{port}/')

    def run(self):
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()

            with conn:
                 print(f"Connected by {addr}")
                 data, content = self._get_request(conn)
                 req_type, url = self._get_type_and_url(data)
                 self.requests_distributor_func(conn, req_type, url, content)
                 conn.close()

    def _get_request(self, conn):
        data = conn.recv(1024) 
        # print(data)

        content_len = int(self._substr(data, b'Content-Length:', b'\r\n'))
        # print('Content len', content_len)

        start = data.index(b'\r\n\r\n')
        content_len-=len(data) - start
        content = data[start:]

        while content_len > 0:
            tmp = conn.recv(1024) 
            content += tmp
            content_len -= len(tmp)
        
        return data[:start], content

    def _substr(self, text, start_str, end_str):
        if start_str in text:
            start = text.index(start_str)
            end = text.index(end_str, start)
            return text[start+len(start_str): end]
        else:
            return 0
    
    def _get_type_and_url(self, data):
        end = data.index(b'\r\n')
        data = data[:end].decode('utf-8')
        data = data.split(' ')
        return data[0], data[1]
    



if __name__ == '__main__':
    server = WebServer('127.0.0.1', 8088, api.requests_distributor)
    server.run()
    # clear port: 
    # fuser -k 8088/udp
    # fuser -k 8088/tcp
