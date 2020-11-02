import spacy
from collections import Counter

def main():
    nlp = spacy.load("en_core_web_sm")

    with open("text.txt", 'r') as f:
        text = f.read()

    doc = nlp(text)

    sentences = [s for s in doc.sents]
    print("Number of sentences in text.txt: " + str(len(sentences)))

    tokens = [t for t in doc if t.is_alpha]
    print("Number of tokens in text.txt: " + str(len(tokens)))

    print("Avg number of words in sentence: " + str(len(tokens)/len(sentences)))

    nouns = [t for t in tokens if t.pos_ == 'NOUN']
    print("Number of nouns: " + str(len(nouns)))

    adjectives = [t for t in tokens if t.pos_ == 'ADJ']
    print("Number of adjectives: " + str(len(adjectives)))

    verbs = [t for t in tokens if t.pos_ == 'VERB']
    print("Number of verbs: " + str(len(verbs)))

    adverbs = [t for t in tokens if t.pos_ == 'ADV']
    print("Number of adverbs: " + str(len(adverbs)))

    tokens_lemma_nouns = [t.lemma_ for t in tokens if t.pos_ == 'NOUN']

    top5 = Counter(tokens_lemma_nouns).most_common(5)
    print("Top 5 most common nouns with number of occurrences: " + str(top5))

    top2 = [t[0] for t in top5[:2]]

    print("Adjectives for 2 most common nouns: " + str(top2))
    for top in top2:
        for adjective in adjectives:
            if adjective.head.lemma_ == top:
                print(adjective.text, adjective.head)




if __name__ == '__main__':
    main()