import pytest
import src.services.book_service as book_service
from src.domain.book import Book
from tests.mocks.mock_book_repository import MockBookRepo


#unit test:
# testing the smallest piece of code possible usually an individual method
# 
#Testing best practices:
#- positive = test conditions when all inputs and all outputs are as expected
#- negative = tests conditions when inputs or outputs could be invalid. i.e. method expects int but str;
# check to see that method exceptions are handled gracefull
#
#- single-action = does my method work for a single record; CRUD operations
#- bulk = does my method work for multiple reacords
#- restricted-user testing = 

def test_get_all_books_positive(): #come up in QC: AAA = Arrange, Act, Assert
    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    books = svc.get_all_books()
    assert len(books) == 1
    
def test_find_book_name_negative():
    name = 3
    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    
    with pytest.raises(TypeError) as e:
        book = svc.find_book_by_name(name)  # noqa: F841
    assert str(e.value)


def test_add_book_positive():
    repo = MockBookRepo([])
    svc = book_service.BookService(repo)
    new_book = Book(title="Dune", author="Frank Herbert")

    book_id = svc.add_book(new_book)
    books = svc.get_all_books()

    assert book_id == new_book.book_id
    assert len(books) == 1
    assert books[0].title == "Dune"
    assert books[0].author == "Frank Herbert"


def test_find_book_name_positive():
    repo = MockBookRepo([Book(title="Dune", author="Frank Herbert")])
    svc = book_service.BookService(repo)

    results = svc.find_book_by_name("Dune")

    assert len(results) == 1
    assert results[0].title == "Dune"
    assert results[0].author == "Frank Herbert"


def test_edit_book_by_name_positive():
    repo = MockBookRepo([Book(title="Old Title", author="Old Author")])
    svc = book_service.BookService(repo)

    updated = svc.edit_book_by_name(
        title="Old Title",
        author="Old Author",
        new_title="New Title",
        new_author="New Author",
    )

    books = svc.get_all_books()

    assert updated is True
    assert len(books) == 1
    assert books[0].title == "New Title"
    assert books[0].author == "New Author"


def test_edit_book_by_name_not_found():
    repo = MockBookRepo([Book(title="Existing", author="Author")])
    svc = book_service.BookService(repo)

    updated = svc.edit_book_by_name(
        title="Missing",
        author="Author",
        new_title="New Title",
        new_author="New Author",
    )

    books = svc.get_all_books()

    assert updated is False
    assert len(books) == 1
    assert books[0].title == "Existing"
    assert books[0].author == "Author"


def test_delete_book_by_name_positive():
    repo = MockBookRepo([Book(title="Dune", author="Frank Herbert")])
    svc = book_service.BookService(repo)

    deleted = svc.delete_book_by_name("Dune", "Frank Herbert")
    books = svc.get_all_books()

    assert deleted is True
    assert len(books) == 0


def test_delete_book_by_name_not_found():
    repo = MockBookRepo([Book(title="Dune", author="Frank Herbert")])
    svc = book_service.BookService(repo)

    deleted = svc.delete_book_by_name("Missing", "Author")
    books = svc.get_all_books()

    assert deleted is False
    assert len(books) == 1