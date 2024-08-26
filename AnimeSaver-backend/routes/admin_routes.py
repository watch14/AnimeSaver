from flask import Blueprint, jsonify, request
from functools import wraps

bp = Blueprint('admin_routes', __name__)

def get_mongo():
    from app import mongo
    return mongo

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_email = request.headers.get('User-Email')
        mongo = get_mongo()
        user = mongo.db.users.find_one({"userEmail": user_email})
        if not user or not user.get('isAdmin', False):
            return jsonify({"message": "Admin access required!"}), 403
        return f(*args, **kwargs)
    return decorator

@bp.route('/admin/data', methods=['GET'])
@admin_required
def admin_data():
    """
    Admin-only data
    ---
    tags:
      - Admin
    responses:
      200:
        description: Admin data
        schema:
          type: object
          properties:
            data:
              type: string
              description: Data available to admin
    """
    return jsonify({"data": "This is protected data for admins only!"}), 200
