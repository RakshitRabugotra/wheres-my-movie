# Use MultiLabelBinarizer to one-hot encode the genres
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# For instant search results from the database
from rapidfuzz import process as rapid_process, fuzz as rapid_fuzz
from logger import logger
import pandas as pd
import os
import re

api_key = os.environ.get("MOVIE_DB_API_KEY") or ""


class MovieRecommender:
    # The default path to the recommendations file
    path_to_movies = r"./ml-20m/movies.csv"
    # The poster api base URL
    poster_image_base_url = "http://image.tmdb.org/t/p/w500/"
    poster_api_base = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key
    poster_search = "&query={0}&year={1}"

    def __init__(self, movies: pd.DataFrame):
        """
        Recommender initializer
        """
        print("Reading data...")
        # Split genres into individual words
        movies["genres"] = movies["genres"].str.split("|")
        # Fill N/A values
        movies["tags"] = movies["tags"].fillna("")
        # Fill N/A values for the ratings
        # median_rating = movies['rating'].mean()
        movies["rating"] = movies["rating"].fillna(0)
        print("Read complete! Processing data")
        # Start add features
        mlb_genres = MultiLabelBinarizer()
        genres_matrix = mlb_genres.fit_transform(movies["genres"])

        # One-hot encode tags
        movies["tags"] = movies["tags"].str.split("|")
        mlb_tags = MultiLabelBinarizer()
        tags_matrix = mlb_tags.fit_transform(movies["tags"])

        # Combine all features into a single DataFrame
        features = pd.DataFrame(
            genres_matrix, index=movies["movieId"], columns=mlb_genres.classes_
        )
        tags_df = pd.DataFrame(
            tags_matrix, index=movies["movieId"], columns=mlb_tags.classes_
        )
        features = features.join(tags_df)
        # Add the rating as a feature
        features["rating"] = movies["rating"].values
        print("Processing complete...")

        # The steps are complete, so copy the relevant information
        self.movies = movies
        self.features = features
        # Initialize the rest of the model
        self.cosine_sim_df = self.__initialize_model()

    def recommend_movies(self, movie_titles: list[str], n_recommendations=5):
        """
        Make Movie Recommendations
        """
        # Get movieIds for the three movies
        movie_ids = [self.__get_movie_id(title) for title in movie_titles]

        if None in movie_ids:
            return "One or more movie titles not found in the dataset."

        # Compute the average similarity score for these three movies
        avg_similarity_scores = self.cosine_sim_df.loc[movie_ids].mean(axis=0)

        # Sort by similarity scores in descending order
        similar_movies = avg_similarity_scores.sort_values(ascending=False)

        # Exclude the movies provided by the user
        similar_movies = similar_movies.drop(movie_ids)

        # Get the top n recommended movies
        recommended_movie_ids = similar_movies.head(n_recommendations).index
        recommended_titles = self.movies[
            self.movies["movieId"].isin(recommended_movie_ids)
        ]

        # Add the image with the movie
        recommended_titles["image"] = recommended_titles["title"].apply(
            lambda title: self.__fetch_movie_poster(title)
        )

        # Sort the filtered DataFrame by rating in descending order
        return recommended_titles.sort_values(by="rating", ascending=False)

    def search_movies(self, title_query: str, limit=5):
        """
        Searches the DataFrame for a match in movie title, considering both similarity
        and movie popularity/rating.
        """
        movie_titles = self.movies["title"].tolist()

        # Use rapidfuzz to find similar movie titles
        similar_titles = rapid_process.extract(
            title_query, movie_titles, scorer=rapid_fuzz.ratio, limit=limit * 2
        )

        # Extract corresponding rows from the DataFrame based on the similar titles
        results = self.movies[
            self.movies["title"].isin([title for title, score, _ in similar_titles])
        ]

        # Add similarity scores to the results DataFrame
        results["similarity"] = results["title"].apply(
            lambda x: next(score for title, score, _ in similar_titles if title == x)
        )

        # Rank the results by a combination of similarity score and rating
        results["ranking_score"] = results["similarity"] * 0.7 + results["rating"] * 0.3

        # Sort results by ranking_score
        results = results.sort_values(by="ranking_score", ascending=False)

        # Limit the number of results to return
        return results.head(limit)

    def __fetch_movie_poster(self, movieTitle: str):
        """
        Fetches the Movie poster of the movie searched using 'themoviedb' API
        """
        title, year = self.__reformat_title(movieTitle)

        endpoint = (
            MovieRecommender.poster_api_base
            + MovieRecommender.poster_search.format(title, year)
        )
        # Get the response from the endpoint
        try:
            response = requests.get(endpoint)
            poster_path = (
                MovieRecommender.poster_image_base_url
                + response.json()["results"][0]["poster_path"]
            )
            return poster_path
        except Exception as e:
            logger.error(
                f"Error while fetching movie poster for title: '{movieTitle}' | error: {e}"
            )
            return None

    def __reformat_title(self, original_title: str):
        # Check if the title is in the format "Thing, The (1982)"
        match = re.match(r"^(.*),\s*The\s+\((\d{4})\)$", original_title)
        if match:
            title, year = match.groups()
            return title, int(year)

        # Check if the title is in the format "Gone Girl (2014)" or "Frailty (2001)"
        match = re.match(r"^(.*)\s+\((\d{4})\)$", original_title)
        if match:
            title, year = match.groups()
            return title, int(year)

        return "", 2020

    def __initialize_model(self):
        """
        Build the Content-Based Recommender Model
        """
        print("Initializing model predictors...")
        # Calculate the cosine similarity matrix
        cosine_sim = cosine_similarity(self.features)
        # Convert the cosine similarity matrix to a DataFrame for easier handling
        cosine_sim_df = pd.DataFrame(
            cosine_sim, index=self.movies["movieId"], columns=self.movies["movieId"]
        )
        print("Initializing complete...")
        return cosine_sim_df

    def __get_movie_id(self, title):
        """
        Function to get movieId from title
        """
        try:
            return self.movies[self.movies["title"] == title]["movieId"].values[0]
        except IndexError:
            return None


if __name__ == "__main__":

    recommender = MovieRecommender()

    # Example: Get recommendations based on three movies
    user_movies = [
        "Conjuring, The (2013)",
        "Lights Out (2013)",
        "Seven (a.k.a. Se7en) (1995)",
        "Avengers, The (2012)",
    ]
    recommendations = recommender.recommend_movies(user_movies, n_recommendations=25)
    print("Recommended movies:\n", recommendations)
