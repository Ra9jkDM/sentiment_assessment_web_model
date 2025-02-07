import torch
from model.lstm_model_structure import model, device
from model.data_loaders import LenOrderDataset, OrderedDataLoader
import numpy as np

TEXT_LEN = 10
MAX_BATCH_SIZE = 5
MAX_TEXT_LEN = -1 # ToDo
PRED = 'pred'


def predict(df, row_name):
    data_ds = LenOrderDataset(df[row_name], df.index)
    data_loader = OrderedDataLoader(data_ds,  batch_size=MAX_BATCH_SIZE)

    with torch.no_grad():
        for X, index in data_loader:
            X = X.to(device)
            outputs = model(X)
            outputs = [i.argmax().cpu() for i in outputs]

            for idx, pred in zip(index, outputs):
                df.at[idx, PRED] = int(pred)

    df = df.drop([row_name], axis=1)
    json_data = {"rows_amount": df.shape[0], 
                "positive": _get_result_amount(df, 1),
                "negative": _get_result_amount(df, 0),
                "unknown": int(df[PRED].isna().sum())}
    return df, json_data

def _get_result_amount(df, exodus):
    return int(df[(df[PRED]==exodus)].count()[PRED])

def predict_text(bg, text):
    clear_text, tokens = bg.preprocess_simple_text(text)
    output = -1

    if len(tokens) == 0:
        return {'text': text,
            'clear_text': clear_text,
            'pred': -999, 
            'pred_word': 'unknown'}
    with torch.no_grad():
        X = torch.IntTensor([tokens]).to(device)
        output = model(X)
        output = output.argmax().cpu()

    return {'text': text,
            'clear_text': clear_text,
            'pred': int(output), 
            'pred_word': 'positive' if output == 1 else 'negative'}


    # remove some row
    # df[(df.row ==1)].count() # сформировать json для ответа
    # positive/negativ/unknown(если после обработки не осталось ни одного слова)