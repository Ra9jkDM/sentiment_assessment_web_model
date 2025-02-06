from router import Router, create_response, create_response_file
from helpers.file_loader import get_file
from helpers.converter import to_dataframe, to_bytes
from model.model_service import add_task

api = Router(prefix='/api') 

@api.get('/')
def main(conn, content):
    body = '{"version": "0.2", "name": "server for lstm lm", "status": "ok"}'
    res = create_response(200, 'OK', body)
    conn.sendall(res)

@api.post('/predict')
def predict(conn, content):
    pass

@api.post('/predict_table', auto_close=False)
def predict_table(conn, content):
    file, extension = get_file(content)
    df = to_dataframe(file, extension)

    if type(df) != type(None):
        print(df.info())
        print(df.head())
        add_task(df, save_connection(conn)(return_results))
    else:
        res = create_response(404, 'Wrong file', '{"text": "Error loading file"}')
        conn.sendall(res)
        conn.close()


def save_connection(conn):
    def map_func(func):
        def mapper(*args, **kwargs):
            func(conn, *args, **kwargs)
        return mapper
    return map_func

def return_results(conn, data):
    print(type(data))
    tmp = to_bytes(data)
    print(tmp, len(tmp.getvalue()))
    print(tmp.getvalue(), type(tmp.getvalue()))
    res1 = create_response(200, 'OK', '{"text": "preprocessed file", "data":"file"}')
    res = create_response_file(200, 'OK', b'{"text": "stat ok", "file": "0"} END'+tmp.getvalue())
    print(res)
    conn.sendall(res)
    # conn.sendall(res1)
    conn.close()

    # addTask(task, conn) -> do task, send result, close conn
    # bg multithreading work_enque


