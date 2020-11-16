import os
import pandas as pd
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")
    columns = ["title", "text", "class"]
    texts = []
    classes = []

    for directory in os.listdir("resources/bbc"):
        for filename in os.listdir("resources/bbc/" + directory):
            with open(os.path.join("resources/bbc", directory, filename)) as f:
                text = f.read()
                doc = nlp(text)
                words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
                string = ' '.join(words)

                texts.append(string)
                classes.append(directory)

    tfIdfVectorizer = TfidfVectorizer(use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(texts)
    df = pd.DataFrame(tfIdf.todense(), columns=tfIdfVectorizer.get_feature_names())
    mapping = {'business': 0, 'entertainment': 1, 'politics': 2, 'sport': 3, 'tech': 4}
    classes_mapped = [mapping.get(c) for c in classes]
    df['bbctext_class'] = classes_mapped
    msk = np.random.rand(len(df)) < 0.5

    train_df = df.sample(frac=0.5, random_state=1234)
    test_df = df.drop(train_df.index)

    train_df.to_csv('bbc_train_csv.csv', index=False, sep=';')
    test_df.to_csv('bbc_test_csv.csv', index=False, sep=';')
