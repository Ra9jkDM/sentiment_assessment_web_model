import requests
import json
import pandas as pd
import io

API = 'http://127.0.0.1:8088/api/'

def get():
    r = requests.get(API)
    print(r)
    print(r.content)

def post(data):
    r = requests.post(API+'pred', data=data)
    print(r)
    print(r.content)

def post_file():
    file = {'upload_f': open('files/test_ml_3.xlsx', 'rb')} # csv
    r = requests.post(API+'predict_table', files=file, data={"text": "some text"}, timeout=10*60) # in seconds
    print(r)
    data = r.content
    print(data)
    sep = b'END'
    start = data.index(sep)
    print(json.loads(data[:start]))

    file = data[start+len(sep):]
    df = pd.read_excel(io.BytesIO(file), engine="openpyxl")
    print(df.info())
    print(df)
    df.to_excel('trash/test_pre.xlsx')


def main():
    # get()
    # post({'test': 'OK'})
    post_file()

if __name__ == '__main__':
    main()