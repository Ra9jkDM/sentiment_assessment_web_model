import json
from model.stream_preprocessing_cls import BackgroundProcessing, Task

def load_word_dict():
    word_dict = {}
    with open('model/data/word_dict.json', 'r') as f:
        word_dict = json.loads(f.read())
    return word_dict


word_dict = load_word_dict()
bg = BackgroundProcessing(word_dict, lambda x, row_name: print('Finish...'))


def add_task(data, func):
    task = Task(data, func)
    bg.add_task(task)