import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

from src.lesson4.FeatureDataset import FeatureDataset
from src.lesson4.Net import Net

if __name__ == '__main__':
    train_set = FeatureDataset('bbc_train_csv.csv')
    test_set = FeatureDataset('bbc_test_csv.csv')
    print('Files read')
    len(train_set.X)

    train_loader = DataLoader(train_set, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=8, shuffle=True)
    print()
    net = Net(len(train_set.X[0]), 5)
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    EPOCHS = 5

    for epoch in range(EPOCHS):
        for features, labels in train_loader:
            net.zero_grad()
            output = net(features.float())
            loss = F.nll_loss(output, labels)
            loss.backward()
            optimizer.step()
        print(epoch, loss)

    correct = 0
    total = 0

    with torch.no_grad():
        for features, labels in test_loader:
            output = net(features.float())
            for idx, i in enumerate(output):
                if torch.argmax(i) == labels[idx]:
                    correct += 1
                total += 1

    print("Accuracy: ", round(correct / total, 3))
    print("Correct: ", correct, " | Total: ", total)
