import requests
import json
import pandas as pd
import io

import asyncio

API = 'http://127.0.0.1:8089/api/'

def get():
    r = requests.get(API)
    print(r)
    print(r.content)

def post(data):
    r = requests.post(API+'pred', data=data)
    print(r)
    print(r.content)

def post_text():
    # r = requests.post(API+'predict', json={'text': 'Когда же мой рабочий день кончится?'})
    r = requests.post(API+'predict', json={'text': 'обучение не очень'})
    print(r)
    print(r.content)
    data = r.text #.decode('utf-8')
    print(data)

def post_file():
    file = {'upload_f': open('files/test_ml_3.xlsx', 'rb')} # csv
    file = {'upload_f': open('files/example_2.csv', 'rb')} # csv
    # file = {'upload_f': open('tests/test_data/one_value.xlsx', 'rb')} # csv
    # file = {'upload_f': open('tests/test_data/empty.csv', 'rb')} # csv
    r = requests.post(API+'predict_table', files=file, data={"text": "some text"}, timeout=10*60) # in seconds
    print(r)
    data = r.content
    # print(data)
    sep = b'END'
    start = data.index(sep)
    print(json.loads(data[:start].decode('utf-8').replace('\'', '"')))

    file = data[start+len(sep):]
    df = pd.read_excel(io.BytesIO(file), engine="openpyxl")
    print(df.info())
    print(df)
    df.to_excel('trash/test_pre.xlsx')


def main():
    # get()
    # post({'test': 'OK'})

    post_text()
    post_file()
    post_text()

async def async_main():
    await asyncio.to_thread(post_file)
    # await asyncio.to_thread(post_text)

if __name__ == '__main__':
    # main()
    asyncio.run(async_main())