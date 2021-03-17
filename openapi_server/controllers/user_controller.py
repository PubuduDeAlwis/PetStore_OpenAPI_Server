#import connexion
#import six

from openapi_server.models.petstore import User # noqa: E501
from openapi_server.models.petstore import user_schema
from openapi_server.models.petstore import users_schema
from openapi_server.config import db
from openapi_server.config import connex_app
from flask import request, jsonify
from werkzeug.security import generate_password_hash
#from openapi_server import util

@connex_app.route('/v2/user', methods=['POST'])
def create_user():  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = generate_password_hash(request.json['password'], method='sha256')
    phone = request.json['phone']
    userstatus = request.json['userstatus']

    new_user = User(username, firstname, lastname, email, password, phone, userstatus)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)



def create_users_with_array_input(body):  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def create_users_with_list_input(body):  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'

@connex_app.route('/v2/user/<username>', methods=['DELETE'])
def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@connex_app.route('/v2/user/<username>', methods=['GET'])
def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing. 
    :type username: str

    :rtype: User
    """
    user = User.query.filter_by(username=username).first()
    return user_schema.jsonify(user)


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'

@connex_app.route('/v2/user/<username>', methods=['PUT'])
def update_user(username):  # noqa: E501
    """Updated user

    This can only be done by the logged in user. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    user = User.query.filter_by(username=username).first()
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = generate_password_hash(request.json['password'], method='sha256')
    phone = request.json['phone']
    userstatus = request.json['userstatus']

    user.username = username
    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.password = password
    user.phone = phone
    user.userstatus = userstatus

    db.session.commit()
    return user_schema.jsonify(user)
