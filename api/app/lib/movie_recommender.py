# Use MultiLabelBinarizer to one-hot encode the genres
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# For instant search results from the database
from rapidfuzz import process as rapid_process, fuzz as rapid_fuzz
import pandas as pd


class MovieRecommender:
    # The default path to the recommendations file
    path_to_movies = r"./ml-20m/movies.csv"

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
        # Sort the filtered DataFrame by rating in descending order
        return recommended_titles.sort_values(by="rating", ascending=False)

    def search_movies(self, title_query: str, limit=5):
        """
        Searches the DataFrame for a match in movie title
        """
        movie_titles = self.movies["title"].tolist()

        # Use rapidfuzz to find similar movie titles
        similar_titles = rapid_process.extract(
            title_query, movie_titles, scorer=rapid_fuzz.ratio, limit=limit
        )

        # Extract corresponding rows from the DataFrame based on the similar titles
        results = self.movies[
            self.movies["title"].isin([title for title, score, _ in similar_titles])
        ]

        # Add similarity scores to the results DataFrame
        results["similarity"] = results["title"].apply(
            lambda x: next(score for title, score, _ in similar_titles if title == x)
        )

        # Sort results by similarity
        results = results.sort_values(by="similarity", ascending=False)

        return results

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
