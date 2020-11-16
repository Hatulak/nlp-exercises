import pandas as pd
import torch
from pandas import DataFrame
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler


class FeatureDataset(Dataset):

    def __init__(self, filename):
        data = pd.read_csv(filename, sep=';')
        x = data.iloc[0:len(data.index), 0:len(data.columns) - 1].values
        y = data.iloc[0:len(data.index), len(data.columns) - 1].values

        sc = StandardScaler()
        self.X = torch.tensor(sc.fit_transform(x))
        self.Y = torch.tensor(y)

    def __len__(self):
        return len(self.Y)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]
