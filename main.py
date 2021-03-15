import math
import os
import pickle
import time

import nltk
from nltk.stem import WordNetLemmatizer
from selenium import webdriver
from selenium import webdriver  # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions


def get_book(title, j):
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # driver = webdriver.Chrome('./chromedriver', options=option)
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://www.gutenberg.org/')
    search_field = driver.find_element_by_id('menu-book-search')
    search_field.send_keys(title.lower())
    search_field.send_keys(Keys.RETURN)
    results = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'booklink')))
    titles = [result.find_element_by_class_name("title").text for result in results]

    for i, book in enumerate(titles):
        print(f"{i + 1}. " + book)

    choice = int(input("What book were you thinking of?(1-25): "))

    chosen_book = results[choice+1]
    chosen_book.click()
    text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Plain Text UTF-8')))
    text.click()
    time.sleep(5)
    book_text = driver.page_source
    with open(f"documents/book{j+1}.py", "w") as text_file:
        text_file.write(book_text)
    with open(f"documents/book{j+1}.py", "r") as text_file:
        book_lines = text_file.readlines()
    return book_lines


def remove_unwanted_text(lines):
    for i, line in enumerate(lines):
        if "*** START OF" in line or "***START OF" in line:
            start = i + 1
        if "*** END OF" in line or "***END OF" in line:
            end = len(lines) - i
    book = lines[start:-end:]
    return book


def remove_line_br(book):
    book = [line for line in book if line != '\n']
    for i, line in enumerate(book):
        if "\n" in line:
            book[i] = line.rstrip("\n")
    return book


def to_string(book):
    book_str = ""
    for line in book:
        book_str += line + " "
    return book_str


def no_symbols(book_string):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    unsymboled_string = ""
    for character in book_string:
        if character == "'":
            unsymboled_string += ""
        elif character not in alphabet:
            unsymboled_string += " "
        else:
            unsymboled_string += character.lower()
    return unsymboled_string


def to_word_list(book_string):
    return book_string.split(" ")


def no_blanks(word_list):
    no_blanks_word_list = []
    for word in word_list:
        if word != " ":
            no_blanks_word_list.append(word)
    for i, line in enumerate(no_blanks_word_list):
        if " " in line:
            no_blanks_word_list[i] = line.rstrip(" ")
    return no_blanks_word_list


def remove_one_letter_words(words_list):
    no_one_letter_words_list = [word for word in words_list if len(word) > 1]
    return no_one_letter_words_list


def remove_stopwords(word_list):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']
    no_stopwords_word_list = [word for word in word_list if word not in stopwords]
    return no_stopwords_word_list


def lemmatize(words_list):
    pass


def clean_book(book_lines):
    data = remove_unwanted_text(book_lines)
    data = remove_line_br(data)
    data = to_string(data)
    data = no_symbols(data)
    data = to_word_list(data)
    data = no_blanks(data)
    data = remove_one_letter_words(data)
    data = remove_stopwords(data)
    return data


def corpus_clean():
    for book_file in os.listdir('./corpus'):
        with open('./corpus/'+book_file, 'r', encoding='utf-8') as file:
            book = file.readlines()
            book = remove_unwanted_text(book)
            book = remove_line_br(book)
            book = to_string(book)
            book = no_symbols(book)
            book = to_word_list(book)
            book = no_blanks(book)
            book = remove_one_letter_words(book)
            book = remove_stopwords(book)
            with open('./corpus/'+book_file, 'wb') as file:
                pickle.dump(book, file)


def get_documents():
    with open("documents/book1.py", "rb") as book1:
        book1 = pickle.load(book1)
    with open("documents/book2.py", "rb") as book2:
        book2 = pickle.load(book2)
    return book1, book2


def save_books():
    for i in range(2):
        search = input("Search: ")
        book_lines = get_book(search, i)
        cleaned = clean_book(book_lines)
        with open(f'documents/book{i+1}.py', 'wb') as file:
            pickle.dump(cleaned, file)


def get_corpus():
    corpus_list = []
    for file in os.listdir('./corpus'):
        with open('./corpus/' + file, 'rb') as book_file:
            book_file = pickle.load(book_file)
            corpus_list.append(book_file)
    return corpus_list


def calculate_tf(book):
    tf = {}
    for word in book:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for key in tf:
        tf[key] = tf[key]/len(book)
    return tf


def calculate_df(book, corpus):
    df = {}
    for word in book:
        df[word] = 0
        for corpus_document in corpus:
            if word in corpus_document:
                df[word] += 1
    return df


def calculate_idf(df):
    n = len(os.listdir('./corpus'))
    for key in df:
        df[key] = math.log(n/(df[key]+1), 10)
    idf = df
    return idf


def calculate_tf_idf(tf, idf):
    tf_idf = {}
    for key in tf:
        tf_idf[key] = tf[key] * idf[key]
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

    return book_vector


def get_cosine_similarity(a, b):
    print("Len a = ", len(a))
    print("Len b = ", len(b))

    dot_product = sum([a[i]*b[i] for i in range(len(a))])
    absolute = math.sqrt(sum([i**2 for i in a]) * sum([i**2 for i in b]))

    return math.degrees(math.acos(dot_product/absolute))


def compare_books(book1, book2, corpus):
    tf1 = calculate_tf(book1)
    print("tf1 calculated")
    df1 = calculate_df(book1, corpus)
    print("df1 calculated")
    idf1 = calculate_idf(df1)
    print("idf1 calculated")
    tf_idf1 = calculate_tf_idf(tf1, idf1)
    print("tf_idf1 calculated")

    tf2 = calculate_tf(book2)
    print("tf2 calculated")
    df2 = calculate_df(book2, corpus)
    print("df2 calculated")
    idf2 = calculate_idf(df2)
    print("idf2 calculated")
    tf_idf2 = calculate_tf_idf(tf2, idf2)
    print("tf_idf2 calculated")

    total_vocab = get_total_vocab(book1, book2, corpus)
    print("vocabulary calculated")

    book1_vector = vectorize_book(tf_idf1, total_vocab)
    print("book vecter 1 calculated")
    book2_vector = vectorize_book(tf_idf2, total_vocab)
    print("book vecter 2 calculated")
    cosine_similarity = get_cosine_similarity(book1_vector, book2_vector)
    print(cosine_similarity)


def main():
    save_books()
    book1, book2 = get_documents()
    corpus = get_corpus()
    compare_books(book1, book1, corpus)


main()
