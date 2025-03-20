import pytest
import requests
import json
import pandas as pd
import io

API = 'http://127.0.0.1:8089/api/'

# @pytest.skip(allow_module_level=True)

def to_dict(req):
    return json.loads(req.text.replace("'", '"'))

def test_server_info():
    r = requests.get(API)

    print(r)
    print(r.content)

    assert r.status_code == 200
    assert to_dict(r)['status'] == 'ok'

@pytest.mark.parametrize("text", [('Когда же мой рабочий день кончится?'), 
                                ('some english text')])
def test_predict_simple_text(text):
    r = requests.post(API+'predict', json={'text': text})
    
    print(r)
    print(r.text)

    assert r.status_code == 200
    res = to_dict(r)
    assert res['text'] == text
    assert 'pred' in res

# @pytest.mark.skip()
@pytest.mark.parametrize("text", [('\''), ('"'), (""), ("\"'\"'")])
def test_pred_text(text):
    # example1 = json.dumps({'text': '"апвап\''}).encode('utf-8').decode('utf-8')
    # example2 = json.dumps({'text': '"апвап\''}).encode('utf-8').decode('unicode_escape')
    # print(example1, example2)
    # print(example2[len('{"text": "'):-2])

    r = requests.post(API+'predict', json={'text': text})
    print(r.text)
    assert r.status_code == 200

def get_file(res):
    sep = b'END'
    data = res.content
    start = data.index(sep)

    text = json.loads(data[:start].decode('utf-8').replace('\'', '"'))
    file = data[start+len(sep):]

    return text, file

def open_file(file):
    df = pd.read_excel(io.BytesIO(file), engine="openpyxl")
    # df.to_excel('trash/test_pre.xlsx')

@pytest.mark.parametrize("filename", [('one_row.csv'), ('one_row_en.csv'),
                                     ('empty.csv'), ('empty.txt'), 
                                    ('one_value.xlsx'), ('one_value_en.xlsx'), 
                                    ('test_ml_3.xlsx'), ('test_ml_3.csv')])
def test_pred_file(filename):
    file = {'upload_f': open(f'tests/test_data/{filename}', 'rb')}
    r = requests.post(API+'predict_table', files=file, timeout=1*60)
    print(r.text)
    if r.status_code != 404:
        text, file = get_file(r)

        print(text)
        for i in ['negative', 'positive', 'rows_amount', 'unknown']:
            assert i in text
        
        try:
            open_file(file)
        except:
            raise Exception('Can not open file in pandas')
