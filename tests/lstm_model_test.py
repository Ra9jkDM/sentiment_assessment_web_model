from model.lstm_model import predict, predict_text
from model.stream_preprocessing_cls import Task, BackgroundProcessing, load_data
import json

def load_dict():
    word_dict = {}
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())
    return word_dict

bg = BackgroundProcessing(load_dict(), lambda x, row_name: print('Finish...'))

def test_predit_text():
    res = predict_text(bg, 'Что-то они перестали летать')
    print(res)

    assert res['clear_text'] == 'что то они перестать летать'
    assert res['pred'] == 0