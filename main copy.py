import socket
import time

HOST = "127.0.0.1"  
PORT = 8088

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def main():
    while True:
        conn, addr = s.accept()
        # conn.settimeout(10)
        with conn:
            print(f"Connected by {addr}")
            # time.sleep(10)
            res = create_response(conn)
            conn.sendall(res)
            # while True:
                # create_response(conn)
                # data = conn.recv(1024)
                # if not data:
                #     break
                # conn.sendall(data)
            conn.close()

def create_response(conn):
    body = '{"test": "ok", "pred": 2342}'

    # wfile = conn.makefile('wb')
    res = 'HTTP/1.1 200 OK\r\n' +\
        'Content-Type: application/json; charset=utf-8\r\n' +\
        f'Content-Length: {len(body)}\r\n\n' + body
    res = res.encode('utf-8')
    print(res)
    # status_line = f'HTTP/1.1 200 OK\r\n'
    # wfile.write(status_line.encode('utf-8'))
    # body = '{"test": "ok", "pred": 2342}'
    # body = body.encode('utf-8')
    # wfile.write(f'Content-Type: application/json\r\nContent-Length: {len(body)}\r\n'.encode('utf-8'))
    # wfile.write(res)
    # wfile.flush()
    # wfile.close()
    return res

if __name__ == '__main__':
    main()

