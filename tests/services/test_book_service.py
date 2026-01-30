import pytest
import src.services.book_service as book_service
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