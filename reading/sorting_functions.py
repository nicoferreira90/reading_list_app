def reorder_books(book_list):
    index = 1
    for book in book_list:
        book.order = index
        book.save()
        index += 1

    return book_list
