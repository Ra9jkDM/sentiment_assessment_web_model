class Routes:
    def __init__(self, req_type, url, func):
        self.req_type = req_type
        self.url = url
        self.func = func

    def __repr__(self):
        return f'Routes({self.req_type}, {self.url}, func)'

class Router:
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.routes = []
    
    def get(self, url, auto_close=True):
        return self._abs_func('GET', url, auto_close)

    def post(self, url, auto_close=True):
        return self._abs_func('POST', url, auto_close)

    def _abs_func(self, req_type, url, auto_close=True):
        def register(func):
            self.routes.append(Routes(req_type, self.prefix+url, func))
            def mapper(conn, *args, **kwargs):
                func(conn, *args, **kwargs)
                return auto_close
            return mapper
        return register

    def requests_distributor(self, conn, req_type, url, content):
        print(self.routes, req_type, url)
        for i in self.routes:
            if i.req_type.upper() == req_type.upper() and i.url == url:
                return i.func(conn, content)
        else:
            res_404 = create_response(404, 'NotFound', '')
            conn.sendall(res_404)
            return True



def create_response(status, info, body):
    res = f'HTTP/1.1 {status} {info}\r\n' +\
        'Content-Type: application/json; charset=utf-8\r\n' +\
        f'Content-Length: '
    body = body.encode('utf-8')
    return res.encode('utf-8') + str(len(body)).encode('utf-8') + b'\r\n\n' + body

def create_response_file(status, info, json_body):
    res = b'HTTP/1.1 '+str(status).encode('utf-8')+b' '+str(info).encode('utf-8')+b'\r\n' +\
        b'Content-Type: application/json; charset=utf-8\r\n' +\
        b'Content-Length: '+str(len(json_body)).encode('utf-8')+b'\r\n\n' + json_body
    return res
