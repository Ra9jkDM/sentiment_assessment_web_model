import json
from model.stream_preprocessing_cls import BackgroundProcessing, Task
from helpers.file_loader import load_word_dict
from model.lstm_model import predict, predict_text

word_dict = load_word_dict()
bg = BackgroundProcessing(word_dict, predict)


def add_task(data, func):
    task = Task(data, func)
    bg.add_task(task)

def predict_one_text(text):
    result = predict_text(bg, text)
    return result