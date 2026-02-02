import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.domain.book import Book

class BookVisualization:
    # Create a bar chart that shows which genres are most common
    def plot_genre_counts(self, books: list[Book]) -> None:
        df = pd.DataFrame([{
            "genre" : b.genre
        } for b in books])
        
        counts = df["genre"].value_counts()
        counts.plot(kind="bar", title="Most Common Genres")
        plt.show()
    
    #Create a bar chart that shows which genres tend to be rated highest
    #- Use a Bayesion Average: 
    #weighted_rating = (ratings_count / (ratings_count + m)) * average_rating+ (m / (ratings_count + m)) * global_average + average_rating = books rating
    #ratings_count = number of ratings
    #global_average = mean rating of all books
    #m = minimum ratings threshold (50-100 recommended)
   
    def plot_high_rated_genre(self, books: list[Book]) -> None:
        df = pd.DataFrame(books)
        
        genre_stats = (
            df.groupby("genre").agg(avg_rating=("average_rating", "mean"), ratings_count=("ratings_count", "sum"))
            .reset_index()
        )
        
        global_avg = ((df["average_rating"] * df["ratings_count"]).sum() / df["ratings_count"].sum())
        
        m = 50 #min ratings treshold
        genre_stats["bayesian_avg"] = (
            (genre_stats["avg_rating"] * genre_stats["ratings_count"] + global_avg * m) / (genre_stats['ratings_count'] + m)
        )
        
        genre_stats = genre_stats.set_index("genre")
        genre_stats["bayesian_avg"].plot(kind="bar", title="Highest Rated Genres (Bayesian Average)")
        plt.ylabel("Bayesian Average Rating")
        plt.show()
        
    #- Create a scatter plot that shows if higher priced books have better ratings
    def plot_price_vs_rating(self, books: list[Book]) -> None:
        df = pd.DataFrame(books)
        
        plt.scatter(df["price_usd"], df["average_rating"], alpha=.6) #price being x, rating = y, alpha so we can see overlapping points
        plt.xlabel("Price (USD)")
        plt.ylabel("Average Rating")
        plt.title("Book Price vs Avergae Rating")
        plt.show()
        
    #- Create a line chart that shows books released by year
    def plot_books_by_year(self, books: list[Book]) -> None:
        df = pd.DataFrame(books)
        
        books_per_year = df.groupby("publication_year").size()
        
        books_per_year.plot(kind="line")
        plt.xlabel("Year")
        plt.ylabel("Number Of Books Published")
        plt.title("Books Published by Year")
        plt.show()
    #- Create a pie chart that shows our checked in vs available books
    