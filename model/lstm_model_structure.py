import torch
import torch.nn as nn
import __main__

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

class SelfAttention(nn.Module):
    def __init__(self, input_dim):
        super(SelfAttention, self).__init__()
        self.input_dim = input_dim
        self.query = nn.Linear(input_dim, input_dim)
        self.key = nn.Linear(input_dim, input_dim)
        self.value = nn.Linear(input_dim, input_dim)
        self.softmax = nn.Softmax(dim=2)
        
    def forward(self, x):
        queries = self.query(x)
        keys = self.key(x)
        values = self.value(x)
        scores = torch.bmm(queries, keys.transpose(1, 2)) / (self.input_dim ** 0.5)
        attention = self.softmax(scores)
        weighted = torch.bmm(attention, values)
        return weighted


class LSTM(nn.Module):
    def __init__(self, input_size, embedding_dim, hidden_size, output_size, pad_idx, weigths):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.embedding = nn.Embedding(input_size, embedding_dim,  _weight = weigths, padding_idx = pad_idx)
        self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers=2, batch_first=True, dropout=0.25)
        self.attention = SelfAttention(hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sig = nn.Sigmoid()

    def forward(self, text):
        embedded = self.embedding(text)
        output, (hidden, cell) = self.lstm(embedded)
        output = self.attention(output)
        output = self.fc(output[:, -1, :])
        output = self.sig(output)
       
        return output

setattr(__main__, "LSTM", LSTM)
setattr(__main__, "SelfAttention", SelfAttention)
model = torch.load('model/data/lstm.pt', weights_only=False) # map_location=torch.device('cpu')
model.eval()
model = model.to(device)