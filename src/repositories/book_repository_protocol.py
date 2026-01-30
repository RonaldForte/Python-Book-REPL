from typing import Protocol
from src.domain.book import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book:Book) -> str:
        ...

    def find_book_by_name(self, query:str) -> list[Book]:
        ...
        
    def edit_book_by_name(self, title:str, author:str, new_author:str|None=None, new_title:str|None=None) -> bool:
        ...
        
    def delete_book_by_name(self, title:str, author:str) -> bool:
        ...