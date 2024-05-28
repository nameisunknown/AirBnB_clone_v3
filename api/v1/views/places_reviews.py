#!/usr/bin/python3
"""This module handles all default RESTFul APIs for Review object"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def place_reviews(place_id):
    """Returns a list of reviews of a specific place"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]

    return jsonify(reviews_list), 200


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Return a review by its id"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review using its id"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new review that is a related to a specific place"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        review_data = request.get_json()
        if review_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, review_data['user_id'])

    if not user:
        abort(404)

    if 'text' not in review_data:
        abort(400, description="Missing text")

    new_review = Review(**review_data)
    new_review.place_id = place_id

    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        new_data = request.get_json()
        if new_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200
