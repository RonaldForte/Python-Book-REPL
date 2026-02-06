from src.domain.book import Book


class MockBookRepo:
    def __init__(self, books: list[Book] | None = None):
        if books is None:
            books = [Book(title="test", author="author")]
        self._books = list(books)

    def get_all_books(self) -> list[Book]:
        return list(self._books)

    def add_book(self, book: Book) -> str:
        self._books.append(book)
        return book.book_id

    def find_book_by_name(self, query: str) -> list[Book]:
        return [b for b in self._books if b.title == query]

    def edit_book_by_name(
        self,
        title: str,
        author: str,
        new_title: str | None = None,
        new_author: str | None = None,
    ) -> bool:
        for book in self._books:
            if book.title == title and book.author == author:
                if new_title is not None:
                    book.title = new_title
                if new_author is not None:
                    book.author = new_author
                return True
        return False

    def delete_book_by_name(self, title: str, author: str) -> bool:
        for index, book in enumerate(self._books):
            if book.title == title and book.author == author:
                del self._books[index]
                return True
        return False