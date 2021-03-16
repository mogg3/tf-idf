from compare import compare_books
from utils import save_books, get_documents, get_corpus


def main():
    save_books()
    book1, book2 = get_documents()
    corpus = get_corpus()
    estimate, cosine_similarity = compare_books(book1, book2, corpus)
    print("Estimate: ", estimate)
    print("Cosine similarity: ", cosine_similarity)


if __name__ == "__main__":
    main()
