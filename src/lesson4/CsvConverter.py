import os
import pandas as pd

if __name__ == '__main__':

    columns = ["title", "text", "class"]

    rows = []
    for directory in os.listdir("resources/bbc"):
        for filename in os.listdir("resources/bbc/" + directory):
            with open(os.path.join("resources/bbc", directory, filename)) as f:
                title = f.readline().replace('\n', ' ')
                lines = []
                for line in f:
                    lines.append(line.replace('\n', '').replace('\r', ''))
                text = ' '.join(lines)
                rows.append({'title': title, 'text': text, 'class': directory})

    df = pd.DataFrame(rows)

    df.to_csv('bbc_csv.csv', index=False, sep=';')
