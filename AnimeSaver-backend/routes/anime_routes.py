# anime_routes.py
from flask import Blueprint, jsonify, request
import requests
import os

# Define the Blueprint
anime_bp = Blueprint('anime_routes', __name__)

# API configuration
CLIENT_ID = os.getenv('MYANIMELIST_CLIENT_ID')
MYANIMELIST_API_URL = 'https://api.myanimelist.net/v2/anime'

@anime_bp.route('/search_anime', methods=['GET'])
def search_anime():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query parameter provided"}), 400

    url = f'{MYANIMELIST_API_URL}?q={query}&limit=10&fields=id,title,main_picture,synopsis,mean,num_episodes,start_date,end_date,genres,status'
    headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('data', [])
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
