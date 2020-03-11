from flask import Blueprint, url_for, redirect, request, jsonify

from project.server import db
from project.server.models import Restaurants, Clients, Menus

restaurants_blueprint = Blueprint("restaurants", __name__)


def get_restaurants():
    restaurants = Restaurants.query.all()  # -> select * from Students
    return jsonify(students=[restaurant.serializer for restaurant in restaurants])


def create_restaurant(request=None):
    client = Clients(name='PEPE')
    menu = Menus(name='Pollo a las Brasas')

    restaurant = Restaurants(None, # ->nulo
                             name=request.args.get('name'),
                             client=client.id,
                             menu=menu.id)
    db.session.add(restaurant)
    db.session.commit()

    return get_restaurants()


def delete_restaurant(request=None):
    restaurants = Restaurants.query.filter_by(
        name=request.args.get('name')).all()  # -> select * from Student where name=request...
    # .one()
    for restaurant in restaurants:
        db.session.delete(restaurant)
        db.session.commit()

    return get_restaurants()


def update_student(request=None):
    restaurants = Restaurants.query.filter_by(
        name=request.args.get('name')).all()  # -> select * from Student where name=request...
    for restaurant in restaurants:
        restaurant.name = 'Jose'
        db.session.commit()

    return get_restaurants()


# por pruebas esta post
@restaurants_blueprint.route("/restaurantes/", methods=["GET", "POST", "DELETE", "PUT"])
def list_restaurants_view():
    if request.method == 'GET':
        return get_restaurants()
    elif request.method == 'POST':
        return create_restaurant(request)
    elif request.method == 'DELETE':
        return delete_restaurant(request)
    else:
        return update_student(request)
