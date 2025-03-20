import pytest
import json
from model.stream_preprocessing_cls import Task, BackgroundProcessing, load_data

def load_dict():
    word_dict = {}
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())
    return word_dict

def test_add_two_tasks():
    try:
        data = load_data(f'tests/test_data/test_ml_3.xlsx', 'xlsx')
        task = Task(data, lambda *args, **kwargs: print('End function'))

        word_dict = load_dict()

        bg = BackgroundProcessing(word_dict, lambda x, row_name: print('Finish...'))
        bg.add_task(task)
        print('First task added')
        bg.add_task(task)
        print('All tasks added')
    except:
        pytest.fail('Unexpected error')
