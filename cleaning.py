import os
import pickle


def remove_unwanted_text(lines):
    for i, line in enumerate(lines):
        if "*** START OF" in line or "***START OF" in line:
            start = i + 1
        if "*** END OF" in line or "***END OF" in line:
            end = len(lines) - i
    book = lines[start:-end:]
    print("Unwanted text from book body removed...")
    return book


def remove_line_br(book):
    book = [line for line in book if line != '\n']
    for i, line in enumerate(book):
        if "\n" in line:
            book[i] = line.rstrip("\n")
    print("Line breaks removed...")
    return book


def to_string(book):
    book_str = ""
    for line in book:
        book_str += line + " "
    print("Stringified...")
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
    print("Symbols removed...")
    return unsymboled_string


def to_word_list(book_string):
    print("Words listed...")
    return book_string.split(" ")


def no_blanks(word_list):
    no_blanks_word_list = []
    for word in word_list:
        if word != " ":
            no_blanks_word_list.append(word)
    for i, line in enumerate(no_blanks_word_list):
        if " " in line:
            no_blanks_word_list[i] = line.rstrip(" ")
    print("Blanks removed...")
    return no_blanks_word_list


def remove_one_letter_words(words_list):
    no_one_letter_words_list = [word for word in words_list if len(word) > 1]
    print("One letter words removed...")
    return no_one_letter_words_list


def remove_stopwords(word_list):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']
    no_stopwords_word_list = [word for word in word_list if word not in stopwords]
    print("Stopwords removed...")
    return no_stopwords_word_list


def clean_book(book_lines):
    data = remove_unwanted_text(book_lines)
    data = remove_line_br(data)
    data = to_string(data)
    data = no_symbols(data)
    data = to_word_list(data)
    data = no_blanks(data)
    data = remove_one_letter_words(data)
    cleaned_data = remove_stopwords(data)
    print("Cleaned!")
    return cleaned_data


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