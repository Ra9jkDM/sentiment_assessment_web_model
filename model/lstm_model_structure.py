import torch
import torch.nn as nn
from torch.nn import Embedding, Linear
import __main__

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

class LSTM(nn.Module):
    def __init__(self, input_size, embedding_dim, hidden_size, output_size, pad_idx, weigths):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.embedding = Embedding(input_size, embedding_dim,  _weight = weigths, padding_idx = pad_idx)
        self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers=2, batch_first=True, dropout=0.25)
        self.fc = Linear(hidden_size, output_size)
        self.sig = nn.Sigmoid()

    def forward(self, text):
        embedded = self.embedding(text)
        output, (hidden, cell) = self.lstm(embedded)
        output = self.fc(output[:, -1, :])
        output = self.sig(output)
       
        return output

setattr(__main__, "LSTM", LSTM)
model = torch.load('model/data/e5_lstm_web.pt', weights_only=False)
model.eval()
model = model.to(device)