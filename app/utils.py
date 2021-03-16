import os
import pickle

from cleaning import clean_book
from scraping import get_book


def get_documents():
    with open("app/documents/book1.py", "rb") as book1:
        book1 = pickle.load(book1)
    with open("app/documents/book2.py", "rb") as book2:
        book2 = pickle.load(book2)
    return book1, book2


def save_books():
    for i in range(2):
        search = input("Search: ")
        print("Searching...")
        book_lines = get_book(search, i)
        cleaned = clean_book(book_lines)
        with open(f'app/documents/book{i+1}.py', 'wb') as file:
            pickle.dump(cleaned, file)


def get_corpus():
    corpus_list = []
    for file in os.listdir('app/corpus'):
        with open('app/corpus/' + file, 'rb') as book_file:
            book_file = pickle.load(book_file)
            corpus_list.append(book_file)
    return corpus_list