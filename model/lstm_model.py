import torch
from model.lstm_model_structure import model, device
from torch.utils.data import TensorDataset, DataLoader
from model.data_loaders import SameLenDataLoader, SeriesDataset
import numpy as np

TEXT_LEN = 10
MAX_BATCH_SIZE = 5
PRED = 'pred'


def predict(df, row_name):
    data_ds = SeriesDataset(df[row_name], df.index)
    data_loader = SameLenDataLoader(data_ds, batch_size=MAX_BATCH_SIZE, tokens_length=230, padding_idx=13335)

    with torch.no_grad():
        for X, index in data_loader:
            X = X.to(device)
            outputs = model(X)
            outputs = [i.argmax().cpu() for i in outputs]

            for idx, pred in zip(index, outputs):
                df.at[idx, PRED] = int(pred)

    df = df.drop([row_name], axis=1)

    if PRED in df.columns:
        json_data = {"rows_amount": df.shape[0], 
                    "positive": _get_result_amount(df, 1),
                    "negative": _get_result_amount(df, 0),
                    "unknown": int(df[PRED].isna().sum())}
    else:
         json_data = {"rows_amount": df.shape[0], 
                    "positive": 0,
                    "negative": 0,
                    "unknown": df.shape[0]}
    print(json_data)
    return df, json_data

def _get_result_amount(df, exodus):
    return int(df[(df[PRED]==exodus)].count()[PRED])

def predict_text(bg, text):
    clear_text, tokens = bg.preprocess_simple_text(text)
    output = -1

    if len(tokens) == 0:
        return {'text': text.replace('\'', '').replace('"', ''),
            'clear_text': clear_text,
            'pred': -1, 
            'pred_word': 'unknown'}
    with torch.no_grad():
        X = torch.IntTensor([tokens]).to(device)
        output = model(X)
        output = output.argmax().cpu()

    return {'text': text.replace('\'', '').replace('"', ''),
            'clear_text': clear_text,
            'pred': int(output), 
            'pred_word': 'positive' if output == 1 else 'negative'}

