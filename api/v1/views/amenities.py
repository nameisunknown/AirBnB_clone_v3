#!/usr/bin/python3
"""This module handles all default RESTFul APIs for Amenity object"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities_list():
    """Returns a list of all amenities in a json representation"""

    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns an amenity by its id"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes am amenity using its id"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""

    try:
        amenity = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if 'name' not in amenity:
        abort(400, description="Missing name")

    new_amenity = Amenity(**amenity)

    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    try:
        new_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
