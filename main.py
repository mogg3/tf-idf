from compare import compare_books
from utils import save_books, get_documents, get_corpus


def main():
    save_books()
    book1, book2 = get_documents()
    corpus = get_corpus()
    appreciation, cosine_similarity = compare_books(book1, book2, corpus)
    print("Appreciation: ", appreciation)
    print("Cosine similarity: ", cosine_similarity)


main()
