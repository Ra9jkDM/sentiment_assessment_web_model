import socket
import time
import pandas as pd
import io

HOST = "127.0.0.1"  
PORT = 8089

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
            data, content = get_all_data(conn)
            # data = conn.recv(1024)
            print(data)
            data = data.decode('utf-8')
            data = data.split(' ')
            requests_distributor(conn, data[0], data[1], content)

            conn.close()

def get_all_data(conn):
    data = conn.recv(1024) 
    print(data)
    text = b'Content-Length:'
    start = data.index(text)
    end = data.index(b'\r\n', start)
    content_len = int(data[start+len(text): end])
    print('Content len', content_len)
    # get content len then read all

    start = data.index(b'\r\n\r\n')
    content_len-=len(data) - start
    content = data[start:]
    while content_len > 0:
        tmp = conn.recv(1024) 
        content += tmp
        content_len -= len(tmp)
        print(content_len)
    
    return data[:start], content


def requests_distributor(conn, req_type, url, content):
    print('Request: ', req_type, url)

    if url == '/pred':
        res = create_response()
        conn.sendall(res)
        print(len(content))

        extension = get_file_type(content)
        content = content[content.index(b'\r\n\r\n', 4):]
        df = None
        if extension == 'xlsx':
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        elif extension == 'csv':
            df = pd.read_csv(io.BytesIO(content))

        if type(df) != type(None):
            print(df.info())
            print(df.head())
        
    else:
        res = response_404()
        conn.sendall(res)

def get_file_type(content):
    start_str = b'filename="'
    start = content.index(start_str)
    end = content.index(b'"\r\n\r\n', start)
    file_type = content[start + len(start_str): end]
    return file_type.decode('utf-8').split('.')[-1]

def create_response():
    body = '{"test": "ok", "pred": 2342}'

    res = 'HTTP/1.1 200 OK\r\n' +\
        'Content-Type: application/json; charset=utf-8\r\n' +\
        f'Content-Length: {len(body)}\r\n\n' + body
    res = res.encode('utf-8')
    print(res)
    return res

def response_404():
    res = 'HTTP/1.1 404 NotFound\r\n' +\
        'Content-Type: text/html; charset=utf-8\r\n' +\
        f'Content-Length: 0\r\n\n'
    res = res.encode('utf-8')
    return res

if __name__ == '__main__':
    main()
    # clear port: 
    # fuser -k 8088/udp
    # fuser -k 8088/tcp
