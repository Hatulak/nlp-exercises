import spacy
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import select, text
from sqlalchemy import Table, Column, Integer, String, MetaData

from src.lesson2.src.utils.config import config


def print_menu():
    print("MENU")
    print("1) Wyszukiwanie artykułów, które zawierają w abstrakcie wszystkie podane słowa")
    print("2) Wyszukiwanie artykułów, które zawierają w abstrakcie przynajmniej jedno z podanych słów")
    print("3) Wyszukiwanie artykułów,"
          " które zawierają przynajmniej jedno z podanych słów w dowolnym z pól tekstowych")
    print("4) Wyjście")
    print()
    print("Podaj numer: ")


def get_input_choise():
    try:
        return int(input())
    except ValueError:
        pass

def create_tokens(text_to_seach):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_to_seach)
    # filter stop words
    return [token.text for token in doc if not token.is_stop]

def main():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/nlp', echo=True)
    metadata = MetaData()
    articles = Table('article', metadata,
                     Column("paper_id", Integer, primary_key=True),
                     Column("paper_title", String),
                     Column("keywords", String),
                     Column("abstract", String),
                     Column("session", String),
                     Column("year", Integer))

    conn = engine.connect()
    # s = select([articles])
    # result = conn.execute(s)
    # [print(row) for row in result]

    # conn = psycopg2.connect(**params)
    #
    # cur = conn.cursor()

    while 1:
        print_menu()
        choise = get_input_choise()

        if choise not in [1, 2, 3, 4]:
            print("Wybór musi być liczbą całkowitą z zakresu 1-3")
            continue
        elif choise == 4:
            print("Zakończono")
            return

        print("Wprowadź słowa do wyszukania rozdzielone spacją")
        text_to_search = str(input())
        words_to_search = create_tokens(text_to_search)

        if choise == 1:
            query_words = " | ".join(words_to_search)
            s = text("SELECT ts_rank_cd(to_tsvector('english', ar.abstract), queryqq) AS rank, ar "
                     "FROM article ar, to_tsquery('english',:qw) queryqq "
                     "WHERE queryqq "
                     "@@ "
                     "to_tsvector('english', ar.abstract)"
                     "ORDER BY rank DESC")

            result = conn.execute(s, qw=query_words)
            [print(row) for row in result]
        elif choise == 2:
            query_words = " & ".join(words_to_search)
            s = text(
                "SELECT ts_rank_cd(to_tsvector('english', ar.abstract), queryqq) AS rank, ar "
                "FROM article ar, to_tsquery('english',:qw) queryqq "
                "WHERE queryqq "
                "@@ "
                "to_tsvector('english', ar.abstract)"
                "ORDER BY rank DESC")
            result = conn.execute(s, qw=query_words)
            [print(row) for row in result]
        elif choise == 3:
            query_words = " | ".join(words_to_search)
            s = text("SELECT ts_rank_cd(to_tsvector('english', ar.abstract), queryqq) AS rank, ar "
                     "FROM article ar, to_tsquery('english',:qw) queryqq "
                     "WHERE queryqq "
                     "@@ "
                     "to_tsvector('english', ar.paper_title || ar.keywords || ar.abstract || ar.session)"
                     "ORDER BY rank DESC")
            result = conn.execute(s, qw=query_words)
            [print(row) for row in result]


if __name__ == '__main__':
    main()
