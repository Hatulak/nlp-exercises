import pandas as pd
import numpy as np
import spacy

if __name__ == '__main__':
    df = pd.DataFrame(pd.read_csv('bbc_csv.csv', sep=';'))
    msk = np.random.rand(len(df)) < 0.5

    train = df.sample(frac=0.5, random_state=1234)
    test = df.drop(train.index)
