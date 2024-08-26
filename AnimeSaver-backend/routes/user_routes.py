from flask import Blueprint, jsonify, request
import bcrypt
from bson.objectid import ObjectId
from flasgger import swag_from
from app import mongo

bp = Blueprint('user_routes', __name__)

def get_mongo():
    from app import mongo
    return mongo

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

    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
    
    user = {
        "userName": user_name,
        "userEmail": user_email,
        "userPassword": hashed_password,
        "savedList": [],
        "isAdmin": is_admin
    }
    mongo = get_mongo()
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
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')

    mongo = get_mongo()
    user = mongo.db.users.find_one({"userEmail": user_email})
    if user and bcrypt.checkpw(user_password.encode('utf-8'), user['userPassword']):
        return jsonify({"message": "Login successful!", "isAdmin": user.get('isAdmin', False)}), 200
    return jsonify({"message": "Invalid email or password!"}), 401

def serialize_document(doc):
    """Helper function to serialize MongoDB documents."""
    doc["_id"] = str(doc["_id"])  # Ensure _id is serialized as a string
    if isinstance(doc.get("userPassword"), bytes):
        doc["userPassword"] = doc["userPassword"].decode("utf-8")  # Convert bytes to string
    return doc

@bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: User's ID
    responses:
      200:
        description: User found
        schema:
          id: User
          properties:
            userName:
              type: string
              description: User's name
            userEmail:
              type: string
              description: User's email
            savedList:
              type: array
              items:
                type: string
            _id:
              type: string
              description: User ID
      404:
        description: User not found
    """
    try:
        mongo = get_mongo()
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify(serialize_document(user))
        return jsonify({"message": "User not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - User
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            type: object
            properties:
              userName:
                type: string
                description: User's name
              userEmail:
                type: string
                description: User's email
              savedList:
                type: array
                items:
                  type: string
                description: List of saved anime IDs
              _id:
                type: string
                description: User ID
      500:
        description: Internal server error
    """
    try:
        mongo = get_mongo()
        users = mongo.db.users.find()
        users_list = []

        for user in users:
            user_doc = {
                "userName": user.get("userName"),
                "userEmail": user.get("userEmail"),
                "userPassword": str(user.get("userPassword")),
                "savedList": user.get("savedList", []),
                "_id": str(user["_id"]) 
            }
            users_list.append(user_doc)

        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/user/<user_id>', methods=['PUT'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'User ID'
        },
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
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'User updated successfully',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        },
        '400': {
            'description': 'Bad request',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        },
        '404': {
            'description': 'User not found',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        }
    }
})
def update_user(user_id):
    data = request.get_json()
    mongo = get_mongo()

    if not data:
        return jsonify({"message": "No JSON data provided"}), 400

    user_update = {}
    if 'userName' in data:
        user_update['userName'] = data['userName']
    if 'userEmail' in data:
        user_update['userEmail'] = data['userEmail']
    if 'userPassword' in data:
        user_update['userPassword'] = bcrypt.hashpw(data['userPassword'].encode('utf-8'), bcrypt.gensalt())
    if 'isAdmin' in data:
        user_update['isAdmin'] = data['isAdmin']

    result = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_update})

    if result.modified_count:
        return jsonify({"message": "User updated successfully!"}), 200
    return jsonify({"message": "User not found or no changes made!"}), 404

@bp.route('/user/<user_id>', methods=['DELETE'])
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
            'description': 'User deleted successfully',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        },
        '404': {
            'description': 'User not found',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        }
    }
})
def delete_user(user_id):
    mongo = get_mongo()
    result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count:
        return jsonify({"message": "User deleted successfully!"}), 200
    return jsonify({"message": "User not found!"}), 404
