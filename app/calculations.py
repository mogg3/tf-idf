import math
import os


def calculate_tf(book):
    tf = {}
    for word in book:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for key in tf:
        tf[key] = tf[key]/len(book)
    print("tf calculated")
    return tf


def calculate_df(book, corpus):
    df = {}
    print("Calculating df....")
    for i, word in enumerate(book):
        df[word] = 0
        for corpus_document in corpus:
            if word in corpus_document:
                df[word] += 1
    print("df calculated")
    return df


def calculate_idf(df):
    n = len(os.listdir('app/corpus'))
    for key in df:
        df[key] = math.log(n/(df[key]+1), 10)
    idf = df
    print("idf calculated")
    return idf


def calculate_tf_idf(tf, idf):
    tf_idf = {}
    for key in tf:
        tf_idf[key] = tf[key] * idf[key]
    print("tfidf calculated")
    print("-"*20)
    return tf_idf


def get_total_vocab(book1, book2, corpus):
    total_vocab = []
    for corpus_document in corpus:
        total_vocab += corpus_document
    total_vocab += book1 + book2
    return list(set(total_vocab))


def vectorize_book(current_book, total_vocab):
    book_vector = []
    for word in total_vocab:
        if word in current_book:
            current_tfidf = current_book[word]
            value = current_tfidf
        else:
            value = 0

        book_vector.append(value)
    print("Book vectorized")
    print("-"*20)
    return book_vector


def calculate_cosine_similarity(a, b):
    dot_product = sum([a[i]*b[i] for i in range(len(a))])
    absolute = math.sqrt(sum([i**2 for i in a]) * sum([i**2 for i in b]))
    print("Cosine similarity calculated")
    print("-"*20)
    return math.degrees(math.acos(dot_product/absolute))