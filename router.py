
routes = []

def route(req_type, url):
    def register(func):
        global routes
        routes.append((req_type, url, func))
        def mapper(conn, *args, **kwargs):
            return func(conn, *args, **kwargs)
        return mapper
    return register

def requests_distributor(conn, req_type, url, content):
    for i in routes:
        if i[0].upper() == req_type.upper() and i[1] == url:
            i[2](conn, content)
    else:
        res_404 = create_response(404, 'NotFound', '')
        conn.sendall(res_404)

def create_response(status, info, body):
    res = f'HTTP/1.1 {status} {info}\r\n' +\
        'Content-Type: application/json; charset=utf-8\r\n' +\
        f'Content-Length: {len(body)}\r\n\n' + body
    return res.encode('utf-8')

@route('get', '/')
def main(conn, content):
    global routes
    print(routes)
    body = '{"status": "ok"}'
    res = create_response(200, 'OK', body)
    conn.sendall(res)