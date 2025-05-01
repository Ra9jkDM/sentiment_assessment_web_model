import torch
from torch.utils.data import Dataset
import numpy as np
    

class SeriesDataset(Dataset):
    def __init__(self, inputs, targets):
        self.data = []

        for i, j in zip(inputs, targets):
            if len(i) > 0:
                self.data.append([i, j])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx][0], self.data[idx][1]


class SameLenDataLoader:
    def __init__(self, dataset, batch_size, tokens_length):
        self.dataset = dataset
        self.batch_size = batch_size
        self.tokens_length = tokens_length
        
        self.idx = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if len(self.dataset) >= self.idx:
            self.idx += self.batch_size
            last = min(self.idx, len(self.dataset))
            
            batch_range = range(self.idx - self.batch_size, last)
            data = [self.dataset[i] for i in batch_range]

            x = [i[0] for i in data]
            index = [i[1] for i in data]
            x = self._make_data_same_len(x)
            
            if type(x) != type(None):
                return torch.IntTensor(x), index
            else:
                raise StopIteration
        else:
            raise StopIteration


    def _make_data_same_len(self, batch):
        if len(batch) != 0:
            return set_text_len(batch, self.tokens_length)

def set_text_len(texts, max_len):
    array = np.zeros([len(texts), max_len])

    i = 0
    for value in texts:
        tmp = max_len-len(value)
        tmp = tmp if tmp > 0 else 0

        text = np.concatenate((value[:max_len], np.zeros(tmp)))
        array[i] = text
        i+=1

    return array 