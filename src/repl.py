from src.services import book_analytics_service
from src.services import generate_books, generate_bad_books
from src.domain.book import Book
from src.services.book_service import BookService
from src.repositories.book_repository import BookRepository
from src.services.book_analytics_service import BookAnalyticsService
from src.services.book_cleaning_service import BookCleaningService
from src.services.book_visualization_service import BookVisualization
import requests


class BookREPL:
    def __init__(
        self, book_svc, book_analytics_svc, book_cleaning_svc, book_visual_svc
    ):  # "constructor"
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc
        self.book_cleaning_svc = book_cleaning_svc
        self.book_visual_svc = book_visual_svc

    def start(self):
        print("Welcome to the book app! Type 'help' for a list of commands!")
        while self.running:
            cmd = input(">>>").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == "exit":
            self.running = False
            print("Goodbye!")
        elif cmd == "getAllRecords":
            self.get_all_records()
        elif cmd == "addBook":
            self.add_book()
        elif cmd == "findByName":
            self.find_book_by_name()
        #elif cmd == "getJoke":
        #    self.get_joke()
        elif cmd == "editByName":
            self.edit_book_by_name()
        elif cmd == "deleteByName":
            self.delete_book_by_name()
        elif cmd == "getAveragePrice":
            self.get_average_price()
        elif cmd == "getTopBooks":
            self.get_top_books()
        elif cmd == "getValueScores":
            self.get_value_scores()
        elif cmd == "getMedianByGenre":
            self.get_median_price_by_genre()
        elif cmd == "getPriceStdDev":
            self.get_price_std_dev()
        elif cmd == "getBestBookByYear":
            self.most_popular_by_year()
        elif cmd == "cleanBooks":
            self.clean_books()        
        elif cmd == 'generateBadBooks':
            self.generate_bad_books()
        elif cmd == "plotCommonGenres":
            self.plot_common_genres()      
        elif cmd == "help":
            print('Available commands: addBook, getAllRecords, findByName, editByName, deleteByName, getAveragePrice, getTopBooks, getValueScores, getMedianByGenre, getPriceStdDev, getBestBookByYear, cleanBooks, generateBadBooks, plotCommonGenres, help, exit')
        else:
            print("Please use a valid command!")

    #def get_joke(self):
    #    try:
    #        url = "https://api.chucknorris.io/jokes/random"
    #        response = requests.get(url, timeout=5)
    #        response.raise_for_status()
    #        print(response.json()["value"])
    #    except requests.exceptions.Timeout:
    #        print("Request timed out.")
    #    except requests.exceptions.HTTPError as e:
    #        print(f"HTTP Error: {e}")
    #    except requests.exceptions.RequestException as e:
    #        print(f"Something else went wrong: {e}")

    def find_book_by_name(self):
        query = input("Please enter book name: ")
        books = self.book_svc.find_book_by_name(query)
        print(books)

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print("Enter Book Details:")
            title = input("Title: ")
            author = input("Author: ")
            book = Book(title=title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")

    def edit_book_by_name(self):
        print("What book would you like to edit?")
        title = input("Enter the Title: ")
        author = input("Enter the Author: ")
        print("What would you like to change the Title to? Enter: The new name/no")
        new_title = input("Enter the New Title: ")
        print("What would you like to change the author to? Enter: The new name/no")
        new_author = input("Enter the New Author: ")

        if new_author.lower() == "no":
            new_author = None
        if new_title.lower() == "no":
            new_title = None

        updated = self.book_svc.edit_book_by_name(
            title=title, author=author, new_title=new_title, new_author=new_author
        )

        if updated:
            print("Book successfully updated!")
        else:
            print("Book not found.")

    def delete_book_by_name(self):
        print("What book would you like to delete?")
        title = input("Enter the Title: ")
        author = input("Enter the Author: ")
        deleted = self.book_svc.delete_book_by_name(title, author)

        if deleted:
            print("Book deleted successfully!")
        else:
            print("Book not found")

    def get_average_price(self):
        books = self.book_svc.get_all_books()
        avg_price = self.book_analytics_svc.average_price(books)
        print(avg_price)

    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_rated_books = self.book_analytics_svc.top_rated(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores(books)
        print(value_scores)

    def get_median_price_by_genre(self):
        books = self.book_svc.get_all_books()
        median_by_genre = self.book_analytics_svc.median_price_by_genre(books)
        print(median_by_genre)

    def get_price_std_dev(self):
        books = self.book_svc.get_all_books()
        std_dev = self.book_analytics_svc.price_std_dev(books)
        print(f"Price Standard Deviation: ${std_dev:.2f}")

    def most_popular_by_year(self):
        year = input("Please enter a year:")
        books = self.book_analytics_svc.most_popular_by_year(
            self.book_svc.get_all_books(), year
        )
        print(books)

    def clean_books(self):
        import json

        # Load raw data from dirty file
        with open("books_dirty.json", "r", encoding="utf-8") as f:
            raw_books = json.load(f)
        # Clean
        cleaned_df = self.book_cleaning_svc.clean(raw_books)
        # Convert back to list of dicts
        cleaned_books = cleaned_df.to_dict("records")
        # Convert Timestamps to strings for JSON serialization
        for book in cleaned_books:
            if "last_checkout" in book:
                book["last_checkout"] = book["last_checkout"].isoformat()
        # Save back to clean file
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(cleaned_books, f, indent=2)
        print("Books cleaned and saved to books.json.")
    
    def generate_bad_books(self):
        generate_bad_books()
        print('Bad books generated to books_dirty.json.')
        
    def plot_common_genres(self):
        books = self.book_svc.get_all_books()
        self.book_visual_svc.plot_genre_counts(books)


if __name__ == "__main__":
    generate_books()
    repo = BookRepository("books.json")
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    book_cleaning_service = BookCleaningService()
    book_visual_service = BookVisualization()
    repl = BookREPL(book_service, book_analytics_service, book_cleaning_service, book_visual_service)
    repl.start()
