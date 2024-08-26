from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId
from flasgger import swag_from

# Import MongoDB connection
from app import mongo

bp = Blueprint('user_routes', __name__)

@bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'userName': {'type': 'string'},
                    'userEmail': {'type': 'string'},
                    'userPassword': {'type': 'string'},
                    'isAdmin': {'type': 'boolean'}
                },
                'required': ['userName', 'userEmail', 'userPassword']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'User registered successfully',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        },
        '400': {
            'description': 'Bad request',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        }
    }
})
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400

    user_name = data.get('userName')
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')
    is_admin = data.get('isAdmin', False)

    if not user_name or not user_email or not user_password:
        return jsonify({"message": "Missing required fields"}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
    
    user = {
        "userName": user_name,
        "userEmail": user_email,
        "userPassword": hashed_password,
        "savedList": [],
        "isAdmin": is_admin
    }
    mongo.db.users.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'userEmail': {'type': 'string'},
                    'userPassword': {'type': 'string'}
                },
                'required': ['userEmail', 'userPassword']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}, 'isAdmin': {'type': 'boolean'}}}
        },
        '401': {
            'description': 'Invalid email or password',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        }
    }
})
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"userEmail": data['userEmail']})
    if user and bcrypt.checkpw(data['userPassword'].encode('utf-8'), user['userPassword']):
        return jsonify({"message": "Login successful!", "isAdmin": user.get('isAdmin', False)}), 200
    return jsonify({"message": "Invalid email or password!"}), 401

@bp.route('/user/<user_id>', methods=['GET'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'User ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'User found',
            'schema': {
                'type': 'object',
                'properties': {
                    'userName': {'type': 'string'},
                    'userEmail': {'type': 'string'},
                    'savedList': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        '404': {
            'description': 'User not found',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        }
    }
})
def get_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({"message": "User not found!"}), 404
