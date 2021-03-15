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
    #titles = [result.find_element_by_class_name("title").text for result in results]

    # for i, book in enumerate(titles):
    #     print(f"{i + 1}. " + book)

    #choice = int(input("What book were you thinking of?(1-25): "))

    chosen_book = results[j+1]
    chosen_book.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Plain Text UTF-8'))).click()
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
    #data = remove_unwanted_text(book_lines)
    #data = remove_line_br(data)
    #data = to_string(data)
    data = no_symbols(book_lines)
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


def get_cleaned_books():
    cleaned_books = []
    for i in range(2):
        with open(f"documents/book{i + 1}.py", 'rb') as file:
            cleaned_book = pickle.load(file)
        cleaned_books.append(cleaned_book)
    return cleaned_books


def get_books():
    for i in range(2):
        #search = input("Search: ")
        book_lines = get_book("twilight", i)
        cleaned = clean_book(book_lines)
        with open(f'documents/book{i+1}.py', 'wb') as file:
            pickle.dump(cleaned, file)


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


def get_corpus():
    corpus_list = []
    for file in os.listdir('./corpus'):
        with open('./corpus/' + file, 'rb') as book_file:
            book_file = pickle.load(book_file)
            corpus_list.append(book_file)
    return corpus_list


def calculate_df(book, corpus):
    df = {}
    for i, word in enumerate(book):
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


def compare_books(book1, book2, corpus):
    tf1 = calculate_tf(book1)
    df1 = calculate_df(book1, corpus)
    idf1 = calculate_idf(df1)
    tf_idf1 = calculate_tf_idf(tf1, idf1)
    tf_idf1 = sorted(tf_idf1.items(), key=lambda kv: kv[1], reverse=True)
    tf_idf1 = dict(tf_idf1)
    print("TF-IDF 1: ", tf_idf1)

    tf2 = calculate_tf(book2)
    df2 = calculate_df(book2, corpus)
    idf2 = calculate_idf(df2)
    tf_idf2 = calculate_tf_idf(tf2, idf2)
    tf_idf2 = sorted(tf_idf2.items(), key=lambda kv: kv[1], reverse=True)
    tf_idf2 = dict(tf_idf2)
    print("TF-IDF 2: ", tf_idf2)


def main():
    c1 = 'To the aspiring student of Nietzsche, however, it ought not to be necessary to become an immediate convert ' \
         'in order to be interested in the treasure of thought which Nietzsche here lavishes upon us.'
    c2 = 'For such a man it will be quite difficult enough to regard the questions raised in this work as actual ' \
         'problems. Once, however, he has succeeded in doing this, and has given his imagination time to play round ' \
         'these questions _as_ problems, the particular turn or twist that Nietzsche gives to their elucidation, may ' \
         'then perhaps strike him, not only as valuable, but as absolutely necessary.'

    # c1_c = clean_book(c1)
    # print(f"Document 1: {c1_c}")
    # c2_c = clean_book(c2)
    # print(f"Document 2: {c2_c}")

    corpus = get_corpus()
    books = get_cleaned_books()
    book1 = books[0]
    book2 = books[1]
    compare_books(book1, book2, corpus)


if __name__ == '__main__':
    main()