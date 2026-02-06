try:
	from .book_generator_service import generate_books_json as generate_books
except Exception:
	generate_books = None

try:
	from .book_generator_bad_data_service import generate_books as generate_bad_books
except Exception:
	generate_bad_books = None

from .book_service import BookService  # noqa: F401

__all__ = ["generate_books", "generate_bad_books"]
