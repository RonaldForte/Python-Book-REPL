import json
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol

class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str="books.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def find_book_by_name(self, query) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
    
    def edit_book_by_name(self, title:str, author:str, new_title:str|None=None, new_author:str|None=None) -> bool:
        books = self.get_all_books() #if current book matches the book we're finding
        for book in books:
            if book.title == title and book.author == author: #if the current book matches the book we're finding
                if new_title is not None: #if the user input a new title
                    book.title = new_title #set it
                if new_author is not None: #if the user input a new author
                    book.author = new_author

                with open(self.filepath,'w', encoding='utf-8') as f: #update books.json
                    json.dump([b.to_dict() for b in books], f, indent=2)
                    
                return True
        return False
    
    def delete_book_by_name(self, title:str, author:str) -> bool:
        books = self.get_all_books()
        updated_books = []
        
        deleted = False
        for book in books:
            if book.title == title and book.author == author and not deleted:
                deleted = True
                continue
            updated_books.append(book)
            
        if not deleted:
            return False
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in updated_books], f, indent=2)
            
        return True
            