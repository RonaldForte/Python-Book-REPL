"""Service for cleaning book data."""

import pandas as pd
import numpy as np


class BookCleaningService:
    # Use the provided JSON dataset and complete the following:
    # Some string values may be, "" instead of null. Set these fields to NaN with numpy before you continue cleaning
    # Clamp publication year to the years of 1800-2026
    # Ensure average_rating, page_count, etc can't have impossible values
    # Normalize dates in 'last_checkout'
    # Ensure genres, languages, formats, and publishers have proper capitalization
    # Find and remove duplicate books with the same title/author

    # Drop rows with empty fields
    def clean(self, books: list[dict]) -> pd.DataFrame:
        # Step 0: create the DataFrame
        df = pd.DataFrame(books)

        # Step 1: normalize missing values
        df = df.replace(
            ["", "N/A", "Unknown"], np.nan
        )  # .replace replaces across entire dataframe

        # Step 2: clamp publication year
        # df['publication_year'] = pd.to_numeric(df['publication_year'], errors='coerce') #.to_numeric converts to numeric, errors='coerce' turns invalids into NaN
        numeric = [
            "page_count",
            "average_rating",
            "ratings_count",
            "price_usd",
            "sales_millions",
            "publication_year",
        ]  # adding to list so i can do this all at once
        for col in numeric:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )  # these will ensure correct numeric values

        # Step 3: Clamp impossible values
        df["page_count"] = df["page_count"].clip(lower=0)  # cant have neg pages
        df["average_rating"] = df["average_rating"].clip(
            lower=0, upper=5
        )  # ratings between 0 and 5
        df["ratings_count"] = df["ratings_count"].clip(lower=0)  # cant have neg ratings
        df["price_usd"] = df["price_usd"].clip(lower=0)  # cant have neg price
        df["publication_year"] = df["publication_year"].clip(
            lower=1800, upper=2026
        )  # clamping pub year
        df["sales_millions"] = df["sales_millions"].clip(lower=0)  # cant have neg sales

        # Step 4: Normalize dates in 'last_checkout'
        df["last_checkout"] = pd.to_datetime(
            df["last_checkout"], errors="coerce"
        )  # converting to datetime, errors='coerce' turns invalids into NaT

        # Step 5: capitalize categories
        capital = [
            "genre",
            "language",
            "format",
            "publisher",
        ]  # adding to list again to do it all in one go
        for col in capital:
            df[col] = (
                df[col].str.strip().str.capitalize()
            )  # remove whitespace and capitalize (online says capitalize() not title())

        # Step 6: remove duplicates
        df = df.drop_duplicates(
            subset=["title", "author"]
        )  # do i really need to comment this? lol

        # Step 7: drop rows with empty critical fields
        critical_columns = ["title", "author"]
        df = df.dropna(
            subset=critical_columns
        )  # subset specifies which columns to check for NaN. dropna() drops those rows

        return df
