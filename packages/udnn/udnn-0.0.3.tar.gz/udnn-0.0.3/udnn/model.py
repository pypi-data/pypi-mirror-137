import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):

    def __init__(self, scale=2, size=128, init=True):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(1, size, (10, 17), stride=(1, 1), padding=(4, 8))
        self.conv2 = nn.Conv2d(size, int(size/2), (7, 13), stride=(1, 1), padding=(3, 6))
        self.conv3 = nn.Conv2d(int(size/2), scale-1, (7, 13), stride=(1, 1), padding=(3, 6))
        if init:
            for b in range(0, int(self.conv1.weight.data.shape[0])):
                for c in range(0, int(self.conv1.weight.data.shape[1])):
                    for d in range(0, int(self.conv1.weight.data.shape[2])):
                        for e in range(0, int(self.conv1.weight.data.shape[3])):
                            self.conv1.weight.data[b][c][d][e] = torch.normal(torch.arange(0, 1), torch.arange(0.001, 0.0011, 0.001)).numpy()[0].astype(float)
            for f in range(0, len(self.conv1.bias.data)):
                self.conv1.bias.data[f] = 0
            for b in range(0, int(self.conv2.weight.data.shape[0])):
                for c in range(0, int(self.conv2.weight.data.shape[1])):
                    for d in range(0, int(self.conv2.weight.data.shape[2])):
                        for e in range(0, int(self.conv2.weight.data.shape[3])):
                            self.conv2.weight.data[b][c][d][e] = torch.normal(torch.arange(0, 1), torch.arange(0.001, 0.0011, 0.001)).numpy()[0].astype(float)
            for f in range(0, len(self.conv2.bias.data)):
                self.conv2.bias.data[f] = 0
            for b in range(0, int(self.conv3.weight.data.shape[0])):
                for c in range(0, int(self.conv3.weight.data.shape[1])):
                    for d in range(0, int(self.conv3.weight.data.shape[2])):
                        for e in range(0, int(self.conv3.weight.data.shape[3])):
                            self.conv3.weight.data[b][c][d][e] = torch.normal(torch.arange(0, 1), torch.arange(0.001, 0.0011, 0.001)).numpy()[0].astype(float)
            for f in range(0, len(self.conv3.bias.data)):
                self.conv3.bias.data[f] = 0

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        return self.conv3(x)
