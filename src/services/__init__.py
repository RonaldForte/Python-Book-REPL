from .book_generator_service import generate_books_json as generate_books
from .book_service import BookService  # noqa: F401

__all__ = ['generate_books']