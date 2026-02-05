import json
from datetime import datetime
from domain.circulation import Circulation
from domain.book import Book


class BookCirculationService:

    # step 1: load books.json -> all current books as dicts
    # step 2: find book by title and author
    # step 3: check if available
    # step 4: if book is already unavailable, return False
    # if not set available to False, update last_checkout to now, save the list back to books.json
    # Step 5: log the checkout action to checkout_logs.json with title, author, action, timestamp APPENDING ONLY
    # finally return true if successful
    def __init__(
        self, book_repository, circulation_repository, filepath="circulation_logs.json"
    ):
        self.book_repository = book_repository
        self.circulation_repository = circulation_repository
        self.filepath = filepath

    def checkout_book(self, title: str, author: str) -> bool:
        books = self.book_repository.get_all_books()
        for book in books:
            if book.title == title and book.author == author:
                if not book.available:
                    return False
                book.available = False
                book.last_checkout = datetime.now().isoformat()
                self.book_repository.update_book(book)

                # log the checkout
                circulation = Circulation(
                    book_id=book.book_id,
                    title=book.title,
                    author=book.author,
                    action="checkout",
                    timestamp=datetime.now(),
                )
                self.circulation_repository.log_circulation(circulation)
                return True
        return False  # book not found

    def checkin_book(self, title: str, author: str) -> bool:
        books = self.book_repository.get_all_books()  # load all books

        # find the book we're checking in
        for book in books:
            if book.title == title and book.author == author:
                if book.available is True:  # already checked in
                    return False
                book.available = True
                book.last_checkout = None

                # save updated books using repository
                self.book_repository.update_book(book)

                # log the checkin
                circulation = Circulation(
                    book_id=book.book_id,
                    title=book.title,
                    author=book.author,
                    action="checkin",
                    timestamp=datetime.now(),
                )
                self.circulation_repository.log_circulation(circulation)

                return True
        return False  # book not found

    def get_all_circulation_logs(self) -> list[Circulation]:
        return self.circulation_repository.get_all_logs()
