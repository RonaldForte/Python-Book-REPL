from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.book import Book

class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all_books()

    def add_book(self, book:Book) -> str:
        return self.repo.add_book(book)

    def find_book_by_name(self, query:str) -> list[Book]:
        if not isinstance(query, str):
            raise TypeError('Expected str, got something else.')
        return self.repo.find_book_by_name(query)
    
    def edit_book_by_name(self, title:str, author:str, new_title:str|None=None, new_author:str|None=None) -> bool:
        return self.repo.edit_book_by_name(title, author, new_title, new_author)
    
    def delete_book_by_name(self, title:str, author:str) -> bool:
        return self.repo.delete_book_by_name(title, author)
    
    