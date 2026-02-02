import numpy as np
import pandas as pd
from src.domain.book import Book

# Ground rules for numpy:
# 1. keep numpy in the service layer ONLY
#   -if you see numpy imports anywhere else, this is a design smell!
# 2. notice how methods take in books, and return normal datatypes NOT ndarrays
# 3. This service and numpy are isolated, this will keep out functions pure and tests clean


class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array(
            [b.price_usd for b in books], dtype=float
        )  # dtype specifies datatype (numpy)
        return float(prices.mean())

    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        ratings = np.array(
            [b.average_rating for b in books]
        )  # array for all avg ratings for all books
        counts = np.array([b.ratings_count for b in books])

        # what we have now:
        # books -> book objects
        # ratings -> numbers for All books
        # counts -> numbers for ALL books

        # filtered books contain all books that have at least 1000 ratings
        mask = counts >= min_ratings
        filteredBooks = np.array(books)[mask]
        # now scores is only the ratings for the filtered books. i.e. over 1000 ratings
        scores = ratings[mask]  # ratings for filtered books
        sorted_idx = np.argsort(
            -scores
        )  # sort descending (highest rating first)
        return filteredBooks[sorted_idx].tolist()[
            :limit
        ]  # top rated books

    # value score = rating * log(ratings_count) / price
    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array(
            [b.average_rating for b in books]
        )  # array for all avg ratings for all books
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books])  # array for price of each book

        scores = (ratings * np.log1p(counts)) / prices

        return {  # dictionary comprehension cause list wasn't enough to learn T-T
            book.book_id: float(score)  # output
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

    def top_rated_with_pandas(
        self, books: list, min_ratings: int = 1000, limit: int = 10
    ) -> list:
        df = pd.DataFrame(
            [
                {"book": b, "avg": b.average_rating, "count": b.ratings_count}
                for b in books
            ]
        )
        filtered = df[df["count"] >= min_ratings].sort_values("avg", ascending=False)
        return filtered["book"].tolist()[:limit]

    def value_scores_with_pandas(
        self, books: list, limit: int = 10
    ) -> dict[str, float]:
        df = pd.DataFrame(
            [
                {
                    "book_id": b.book_id,
                    "avg": b.average_rating,
                    "count": b.ratings_count,
                    "price": b.price_usd,
                }
                for b in books
            ]
        )
        df["score"] = df["avg"] * np.log1p(df["count"]) / df["price"]
        # set_index() sets book_id as the index
        # we do this because we want to end up with a dict[str, float]
        # where book_id is the key and the value score is the float
        # sometimes numpy works with float64, but we need to return float,
        # hence the defensive use of .astype()
        return (
            df.sort_values("score", ascending=False)
            .head(limit)
            .set_index("book_id")["score"]
            .astype(float)
            .to_dict()
        )

    def most_popular_by_year(self, books: list[Book], year) -> dict[int, Book]:
        df = pd.DataFrame(
            [
                {  # creating a dataframe populated with a books genre and last_checkout
                    "book": b,
                    "genre": b.genre,
                    "last_checkout": b.last_checkout,
                    "ratings_count": b.ratings_count,
                }
                for b in books  # for each book
            ]
        )
        df["last_checkout"] = pd.to_datetime(
            df["last_checkout"]
        )  # normalizing the date format for pandas (access to .dt.year, .dt.month, etc)

        df_year = df[
            df["last_checkout"].dt.year == int(year)
        ]  # pandas version of "if book.last_checkout.year == year:"

        if df_year.empty:  # if there are no books checked out that year
            return None  # return None allowed with Optional

        # Find the book with the highest ratings_count among those checked out in the year
        most_popular_book = df_year.sort_values("ratings_count", ascending=False).iloc[
            0
        ]["book"]

        return {int(year): most_popular_book}
