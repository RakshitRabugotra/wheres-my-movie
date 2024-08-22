from flask import Blueprint, request

# Custom modules
from app.utils.responses import Success
from app.utils.responses import BadRequestException
from app import movie_recommender


"""
The APIs for getting movie information
"""
movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/search", methods=["GET"])
def search():
    title = request.args.get("q")
    limit = request.args.get("n", default="5")
    # If the title is not valid, return
    if not title or len(title) == 0:
        return BadRequestException("title is invalid").response
    # Return the response from the recommender
    results = movie_recommender.search_movies(title, int(limit))
    return Success(
        msg="Movies matching the search", payload=results.to_dict(orient="records")
    ).response


@movies_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    API endpoint to get the recommendation based on titles

    :required:
    titles: list[str]
    count: int
    """
    # Get the data passed from the forms
    titles = request.json["titles"]
    count = request.json["count"]
    # filterNA = request.form.get('filterNA')
    # Return the response from the recommender
    movies_df = movie_recommender.recommend_movies(
        map(str, titles), n_recommendations=int(count)
    )
    return Success(
        msg="Recommendations", payload=movies_df.to_dict(orient="records")
    ).response
