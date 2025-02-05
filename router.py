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
    
    def get(self, url):
        return self._abs_func('GET', url)

    def post(self, url):
        return self._abs_func('POST', url)

    def _abs_func(self, req_type, url):
        def register(func):
            self.routes.append(Routes(req_type, self.prefix+url, func))
            def mapper(conn, *args, **kwargs):
                return func(conn, *args, **kwargs)
            return mapper
        return register

    def requests_distributor(self, conn, req_type, url, content):
        print(self.routes, req_type, url)
        for i in self.routes:
            if i.req_type.upper() == req_type.upper() and i.url == url:
                i.func(conn, content)
        else:
            res_404 = create_response(404, 'NotFound', '')
            conn.sendall(res_404)



def create_response(status, info, body):
    res = f'HTTP/1.1 {status} {info}\r\n' +\
        'Content-Type: application/json; charset=utf-8\r\n' +\
        f'Content-Length: {len(body)}\r\n\n' + body
    return res.encode('utf-8')
