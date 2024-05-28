#!/usr/bin/python3
"""This module contanis routes for /status and /stats"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of an API"""

    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return the number of each objects by type"""

    classes = {"users": User, "places": Place, "cities": City,
               "states": State, "amenities": Amenity, "reviews": Review}
    new_dict = {}
    for key, value in classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)
