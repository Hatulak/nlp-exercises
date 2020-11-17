import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

from src.lesson4.FeatureDataset import FeatureDataset
from src.lesson4.Net import Net
from sklearn.metrics import confusion_matrix

if __name__ == '__main__':
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("running on GPU")
    else:
        device = torch.device("cpu")
        print("running on CPU")

    train_set = FeatureDataset('bbc_train_csv.csv')
    test_set = FeatureDataset('bbc_test_csv.csv')
    print('Files read')
    len(train_set.X)

    train_loader = DataLoader(train_set, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=8, shuffle=True)
    print()
    net = Net(len(train_set.X[0]), 5).to(device)
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    EPOCHS = 5

    for epoch in range(EPOCHS):
        for features, labels in train_loader:
            feat = features.float().to(device)
            lab = labels.to(device)
            net.zero_grad()
            output = net(feat)
            loss = F.nll_loss(output, lab)
            loss.backward()
            optimizer.step()
        print(epoch, loss)

    correct = 0
    total = 0
    predicted = []
    true = []

    with torch.no_grad():
        for features, labels in test_loader:
            feat = features.float().to(device)
            lab = labels.to(device)
            output = net(feat)
            for idx, i in enumerate(output):
                predicted.append(torch.argmax(i))
                true.append(labels[idx])
                if torch.argmax(i) == labels[idx]:
                    correct += 1
                total += 1

    print("Accuracy: ", round(correct / total, 3))
    print("Correct: ", correct, " | Wrong: ", total-correct, " | Total: ", total)
    cf = confusion_matrix([index.item() for index in true],
                          [index.item() for index in predicted])
    cf_df = pd.DataFrame(cf, index=['business', 'entertainment', 'politics', 'sport', 'tech'],
                 columns=['business', 'entertainment', 'politics', 'sport', 'tech'])
    print(cf_df)