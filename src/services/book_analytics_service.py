import numpy as np
from src.domain.book import Book

# Ground rules for numpy:
# 1. keep numpy in the service layer ONLY
#   -if you see numpy imports anywhere else, this is a design smell!
# 2. notice how methods take in books, and return normal datatypes NOT ndarrays
# 3. This service and numpy are isolated, this will keep out functions pure and tests clean

class BookAnalyticsService:
    
    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype=float) #dtype specifies datatype (numpy)
        return float(prices.mean())
    
    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        ratings = np.array([b.average_rating for b in books]) #array for all avg ratings for all books
        counts = np.array([b.ratings_count for b in books])
        
        # what we have now:
        # books -> book objects
        # ratings -> numbers for All books
        # counts -> numbers for ALL books
        
        # filtered books contain all books that have at least 1000 ratings
        mask = counts >= min_ratings
        filteredBooks = np.array(books)[mask]
        # now scores is only the ratings for the filtered books. i.e. over 1000 ratings
        scores = ratings[mask][::-1] #this is a view of ratings with mask applied
        sorted_idx = np.argsort(scores) #gives us a sorting index we can use (array of all the indexes of all the arrays of all the books)
        return filteredBooks[sorted_idx].tolist()[:limit] #sorted_idx is basically another mask. limit meaning param so top 10 ratings
    
    #value score = rating * log(ratings_count) / price
    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books]) #array for all avg ratings for all books
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books]) #array for price of each book
        
        scores = (ratings * np.log1p(counts)) / prices
        
        return { #dictionary comprehension cause list wasn't enough to learn T-T
            book.book_id: float(score) #output
            for book, score in zip(books, scores) 
            # zip() iterates through both lists in parallel
            # paring each book with its corresponding score
            # zip() will stop automatically if one list is shorter
            # - if the same key appears mroe than once, later entries overwrites earlier ones
        }
    
    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:
        # Create a dictionary to store books grouped by genre
        genre_books = {}
        
        for book in books:
            if book.genre not in genre_books:
                genre_books[book.genre] = []
            genre_books[book.genre].append(book)
        
        # Compute median price for each genre
        result = {}
        
        for genre, books_in_genre in genre_books.items():
            # Extract prices for this genre into a numpy array
            prices = np.array([b.price_usd for b in books_in_genre])
            median_price = float(np.median(prices))
            result[genre] = median_price
            # np.median() handles all edge cases:
            # - Single element: returns that element
            # - Even number of elements: returns average of two middle values
            # - Odd number of elements: returns middle value
        return result
    
    def price_std_dev(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype=float)
        return float(np.std(prices))
        # np.std() computes standard deviation
        # ddof=0 = population std dev
        # ddof=1 = sample std dev (divides by n-1 instead of n)
        # (ddof=0) on default
