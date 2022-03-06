"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

api = Blueprint('api', __name__)

#enlace/api/hello
@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    print(user.email)

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token) 


@api.route("/user/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    # Accede a la identidad del usuario actual con get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if current_user != user.email:
        return jsonify(logged_in_as=current_user), 400
        
    return jsonify(user.serialize()), 200