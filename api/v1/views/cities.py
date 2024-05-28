#!/usr/bin/python3
"""This module handles all default RESTFul APIs for City object"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_cities(state_id):
    """Returns a list of cities of a specific state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities_list = [city.to_dict() for city in state.cities]

    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Return a city by its id"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city using its id"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city that is a part of a specific state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        city = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'name' not in city:
        abort(400, description="Missing name")

    new_city = City(**city)
    new_city.state_id = state_id

    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        new_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
