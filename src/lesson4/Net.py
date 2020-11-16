import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self, inputs_num, outputs_num):
        super().__init__()
        self.layer1 = nn.Linear(inputs_num, 1024)
        self.layer2 = nn.Linear(1024, 128)
        self.layer3 = nn.Linear(128, outputs_num)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.layer3(x)

        return F.log_softmax(x, dim=1)
