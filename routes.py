from router import create_response, Router
from helpers.file_loader import get_file
from helpers.converter import to_dataframe

api = Router(prefix='/api') 

@api.get('/')
def main(conn, content):
    body = '{"version": "0.1", "name": "server for lstm lm", "status": "ok"}'
    res = create_response(200, 'OK', body)
    conn.sendall(res)

@api.post('/predict')
def predict(conn, content):
    pass

@api.post('/predict_table')
def predict_table(conn, content):
    file, extension = get_file(content)
    df = to_dataframe(file, extension)

    if type(df) != type(None):
            print(df.info())
            print(df.head())
    # bg multithreading work_enque


