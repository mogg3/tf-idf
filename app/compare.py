from app.calculations import calculate_tf, calculate_df, calculate_idf, calculate_tf_idf, get_total_vocab, vectorize_book, \
    calculate_cosine_similarity


def compare_books(book1, book2, corpus):
    tf1 = calculate_tf(book1)
    df1 = calculate_df(book1, corpus)
    idf1 = calculate_idf(df1)
    tf_idf1 = calculate_tf_idf(tf1, idf1)

    tf2 = calculate_tf(book2)
    df2 = calculate_df(book2, corpus)
    idf2 = calculate_idf(df2)
    tf_idf2 = calculate_tf_idf(tf2, idf2)

    total_vocab = get_total_vocab(book1, book2, corpus)
    book1_vector = vectorize_book(tf_idf1, total_vocab)
    book2_vector = vectorize_book(tf_idf2, total_vocab)
    cosine_similarity = calculate_cosine_similarity(book1_vector, book2_vector)

    estimate = None

    if cosine_similarity == 0:
        estimate = "Böckerna är likadana"
    elif 0 < cosine_similarity <= 10:
        estimate = "Böckerna har väldigt många likheter"
    elif 10 < cosine_similarity <= 45:
        estimate = "Böckerna har många likheter"
    elif 45 < cosine_similarity <= 60:
        estimate = "Böckerna har vissa likheter"
    elif 60 < cosine_similarity <= 80:
        estimate = "Böckerna har få likheter"
    elif 80 < cosine_similarity:
        estimate = "Böckerna har väldigt få likheter"
    return estimate, cosine_similarity
