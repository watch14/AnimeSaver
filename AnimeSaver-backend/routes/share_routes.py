from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flasgger import Swagger
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = os.getenv("MONGO_URL_ONLINE_ANIMESAVER")
mongo = PyMongo(app)

# Initialize Swagger
swagger = Swagger(app)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

shareable_links_db = {}

@app.route('/api/share-list', methods=['POST'])
def share_list():
    data = request.json
    user_id = data.get('userId')
    anime_list = data.get('animeList')

    # Generate a unique identifier for the shareable link
    link_id = str(uuid.uuid4())
    shareable_link = f"http://localhost:5000/shared-list/{link_id}"

    # Save the link_id and associated data
    shareable_links_db[link_id] = {
        'userId': user_id,
        'animeList': anime_list
    }

    return jsonify({"link": shareable_link})

@app.route('/shared-list/<link_id>', methods=['GET'])
def get_shared_list(link_id):
    data = shareable_links_db.get(link_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Link not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
