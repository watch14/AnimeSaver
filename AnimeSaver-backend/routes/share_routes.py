# routes/share_routes.py
from flask import Blueprint, request, jsonify
import uuid

share_bp = Blueprint('share', __name__)

# Example in-memory store (replace with database in production)
shareable_links_db = {}

@share_bp.route('/share-list', methods=['POST'])
def share_list():
    data = request.json
    user_id = data.get('userId')
    anime_list = data.get('animeList')

    # Generate a unique identifier for the shareable link
    link_id = str(uuid.uuid4())
    shareable_link = f"http://localhost:5173/shared-list/{link_id}"

    # Save the link_id and associated data
    shareable_links_db[link_id] = {
        'userId': user_id,
        'animeList': anime_list
    }

    return jsonify({"link": shareable_link})

@share_bp.route('/shared-list/<link_id>', methods=['GET'])
def get_shared_list(link_id):
    # Retrieve the shared data from the store
    data = shareable_links_db.get(link_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Link not found"}), 404
