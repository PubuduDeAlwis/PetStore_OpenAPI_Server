#import connexion
#import six

#from openapi_server.models.order import Order  # noqa: E501
#from openapi_server import util
from openapi_server.models.petstore import Order
from openapi_server.models.petstore import Status

from openapi_server.models.petstore import status_schema
from openapi_server.models.petstore import order_schema
from openapi_server.models.petstore import orders_schema

from openapi_server.config import connex_app
from openapi_server.config import db
from flask import request
from flask_restful import abort
from datetime import datetime


@connex_app.route('/v2/store/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):  # noqa: E501
    """Delete purchase order by ID

    For valid response try integer IDs with positive integer value.         Negative or non-integer values will generate API errors # noqa: E501

    :param order_id: ID of the order that needs to be deleted
    :type order_id: int

    :rtype: None
    """
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    return order_schema.jsonify(order)


@connex_app.route('/v2/store/order', methods=['GET'])
def get_inventory():  # noqa: E501
    """Returns pet inventories by status

    Returns a map of status codes to quantities # noqa: E501


    :rtype: Dict[str, int]
    """
    orders = Order.query.all()
    orders = orders_schema.dump(orders)
    return orders_schema.jsonify(orders)


@connex_app.route('/v2/store/order/<order_id>', methods=['GET'])
def get_order_by_id(order_id):  # noqa: E501
    """Find purchase order by ID

    For valid response try integer IDs with value &gt;&#x3D; 1 and &lt;&#x3D; 10.         Other values will generated exceptions # noqa: E501

    :param order_id: ID of pet that needs to be fetched
    :type order_id: int

    :rtype: Order
    """
    order = Order.query.get(order_id)

    return order_schema.jsonify(order)


@connex_app.route('/v2/store/order/status', methods=['POST'])
def add_order_status():
    dis = 'order status'
    value = request.json['value']
    status = Status.query.filter_by(value=value, dis=dis).first()

    if status:
        abort(409)
    else:
        new_status = Status(dis, value)
        db.session.add(new_status)
        db.session.commit()

        return status_schema.jsonify(new_status)


@connex_app.route('/v2/store/order', methods=['POST'])
def place_order():  # noqa: E501
    """Place an order for a pet

     # noqa: E501

    :param body: order placed for purchasing the pet
    :type body: dict | bytes

    :rtype: Order
    """
    pet_id = request.json['pet_id']
    quantity = request.json['quantity']
    shipdate = datetime.strptime(request.json['shipdate'], "%Y-%m-%d %H:%M:%S")
    complete = request.json['complete']
    status_value = request.json['status']

    status = Status.query.filter_by(value=status_value).first()
    status_id = status.id

    new_order = Order(pet_id, quantity, shipdate, complete, status_id)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)
