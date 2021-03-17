#import connexion
#import six

#from openapi_server.models.api_response import ApiResponse  # noqa: E501
from openapi_server.models.petstore import Pet
from openapi_server.models.petstore import Status
from openapi_server.models.petstore import Category
from openapi_server.models.petstore import Tag
from openapi_server.models.petstore import PhotoURL

from openapi_server.models.petstore import pet_schema
from openapi_server.models.petstore import pets_schema
from openapi_server.models.petstore import status_schema
from openapi_server.models.petstore import category_schema
from openapi_server.models.petstore import tag_schema
from openapi_server.config import db

from openapi_server.models.petstore import photourls_schema
from openapi_server.config import connex_app
from flask import request, jsonify
from flask_restful import abort
#from openapi_server import util


@connex_app.route('/v2/pet/status', methods=['POST'])
def add_pet_status():   # noqa: E501
    """add new pet status to the store

    :return:
    """
    dis = 'pet status in the store'
    value = request.json['value']
    status = Status.query.filter_by(value=value, dis=dis).first()

    if status:
        abort(409)
    else:
        new_status = Status(dis, value)
        db.session.add(new_status)
        db.session.commit()

        return status_schema.jsonify(new_status)


@connex_app.route('/v2/pet/category', methods=['POST'])
def add_pet_category():
    cat_name = request.json['cat_name']
    category = Category.query.filter_by(cat_name=cat_name).first()

    if category:
        abort(409)
    else:
        new_category = Category(cat_name)
        db.session.add(new_category)
        db.session.commit()

        return category_schema.jsonify(new_category)


@connex_app.route('/v2/pet/tag', methods=['POST'])
def add_pet_tag():
    tag_name = request.json['tag_name']
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    if tag:
        abort(409)
    else:
        new_tag = Tag(tag_name)
        db.session.add(new_tag)
        db.session.commit()

        return tag_schema.jsonify(new_tag)


@connex_app.route('/v2/pet/tagging', methods=['POST'])
def pet_tagging():
    pet_id = request.json['pet_id']
    tag_name = request.json['tag_name']
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    pet = Pet.query.get(pet_id)

    tag.tags.append(pet)
    db.session.commit()

    return "Tagging Success!"


@connex_app.route('/v2/pet', methods=['POST'])
def add_pet():  # noqa: E501
    """Add a new pet to the store

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: None
    """
    pet_name = request.json['pet_name']
    category_value = request.json['category']
    status_value = request.json['status']
    dis = 'pet status in the store'
    status = Status.query.filter_by(value=status_value, dis=dis).first()
    status_id = status.id
    category = Category.query.filter_by(cat_name=category_value).first()
    cat_id = category.id
    new_pet = Pet(pet_name, cat_id, status_id)
    db.session.add(new_pet)
    db.session.commit()

    return pet_schema.jsonify(new_pet)


@connex_app.route('/v2/pet/<pet_id>', methods=['DELETE'])
def delete_pet(pet_id):  # noqa: E501
    """Deletes a pet

     # noqa: E501
    :param pet_id: Pet id to delete
    :type pet_id: int
    :param api_key: 
    :type api_key: str

    :rtype: None
    """
    pet = Pet.query.get(pet_id)
    photourls = PhotoURL.query.filter_by(pet_id=pet_id).all()
    for i in photourls:
        db.session.delete(i)
    db.session.delete(pet)
    db.session.commit()

    return pet_schema.jsonify(pet)


@connex_app.route('/v2/pet/status', methods=['GET'])
def find_pets_by_status():  # noqa: E501
    """Finds Pets by status

    Multiple status values can be provided with comma separated strings # noqa: E501

    :param status: Status values that need to be considered for filter
    :type status: List[str]

    :rtype: List[Pet]
    """
    value = request.json['value']
    dis = 'pet status in the store'

    status = Status.query.filter_by(value=value, dis=dis).first()
    if not status:
        abort(404)

    else:
        status_id = status.id
        pets_with_status = Pet.query.filter_by(status_id=status_id)

        return pets_schema.jsonify(pets_with_status)


@connex_app.route('/v2/pet/tagging/<tag_name>', methods=['GET'])
def find_pets_by_tags(tag_name):  # noqa: E501
    """Finds Pets by tags

    Muliple tags can be provided with comma separated strings. Use         tag1, tag2, tag3 for testing. # noqa: E501

    :param tags: Tags to filter by
    :type tags: List[str]

    :rtype: List[Pet]
    """
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    pets = Pet.query.with_parent(tag)
    pets = pets_schema.dump(pets)

    return pets_schema.jsonify(pets)


@connex_app.route('/v2/pet/<pet_id>')
def get_pet_by_id(pet_id):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param pet_id: ID of pet to return
    :type pet_id: int

    :rtype: Pet
    """
    pet = Pet.query.get(pet_id)

    return pet_schema.jsonify(pet)


@connex_app.route('/v2/pet', methods=['PUT'])
def update_pet():  # noqa: E501
    """Update an existing pet

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: None
    """
    pet_id = request.json['pet_id']
    pet_name = request.json['pet_name']
    category_value = request.json['category_value']
    status_value = request.json['status_value']
    dis = 'pet status in the store'

    status = Status.query.filter_by(value=status_value, dis=dis).first()
    status_id = status.id
    category = Category.query.filter_by(cat_name=category_value).first()
    category_id = category.id

    pet = Pet.query.get(pet_id)
    pet.pet_name = pet_name
    pet.category_id = category_id
    pet.status_id = status_id

    db.session.commit()
    return pet_schema.jsonify(pet)


@connex_app.route('/v2/pet/<pet_id>', methods=['PUT'])
def update_pet_with_form(pet_id):  # noqa: E501
    """Updates a pet in the store with form data

     # noqa: E501

    :param pet_id: ID of pet that needs to be updated
    :type pet_id: int
    :param name: Updated name of the pet
    :type name: str
    :param status: Updated status of the pet
    :type status: str

    :rtype: None
    """
    pet = Pet.query.get(pet_id)
    pet_name = request.form['pet_name']
    category_value = request.form['category_value']
    status_value = request.form['status_value']
    dis = 'pet status in the store'

    status = Status.query.filter_by(value=status_value, dis=dis).first()
    status_id = status.id
    category = Category.query.filter_by(cat_name=category_value).first()
    category_id = category.id

    pet.pet_name = pet_name
    pet.category_id = category_id
    pet.status_id = status_id

    db.session.commit()

    return pet_schema.jsonify(pet)


@connex_app.route('/v2/pet/<pet_id>/photourls', methods=['POST'])
def upload_file(pet_id):  # noqa: E501
    """uploads an image

     # noqa: E501

    :param pet_id: ID of pet to update
    :type pet_id: int
    :param additional_metadata: Additional data to pass to server
    :type additional_metadata: str
    :param file: file to upload
    :type file: str

    :rtype: ApiResponse
    """
    if request.data:
        jdata = request.get_json()
        for i in range(len(jdata['photourls'])):
            photourl =str(jdata['photourls'][i]['photourl'])
            newurl = PhotoURL(photourl, pet_id)
            db.session.add(newurl)
        db.session.commit()
        return "urls added"
    else:
        return "nothing"

