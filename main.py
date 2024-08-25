from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__)
CLIENT_ID = 'dfe48b7bb1e8af63efd5cd846dee89db'
WATCHLIST_FILE = 'watchlist.json'

def search_anime(query):
    try:
        url = f'https://api.myanimelist.net/v2/anime?q={query}&limit=10&fields=id,title,main_picture,synopsis,mean,num_episodes,start_date,end_date,genres,status'
        headers = {'X-MAL-CLIENT-ID': CLIENT_ID}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.RequestException as e:
        return []

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_watchlist(anime_list):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(anime_list, f, indent=4)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    results = search_anime(query)
    return jsonify(results)

@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'GET':
        return jsonify(load_watchlist())
    
    if request.method == 'POST':
        anime_data = request.json
        watchlist = load_watchlist()
        if not any(anime['id'] == anime_data['id'] for anime in watchlist):
            watchlist.append(anime_data)
            save_watchlist(watchlist)
            return jsonify({'message': f"{anime_data['title']} added to watchlist!"})
        return jsonify({'message': 'This anime is already in your watchlist.'}), 400

@app.route('/watchlist/<int:anime_id>', methods=['DELETE'])
def remove_from_watchlist(anime_id):
    watchlist = load_watchlist()
    updated_list = [anime for anime in watchlist if anime['id'] != anime_id]
    save_watchlist(updated_list)
    return jsonify({'message': 'Anime removed from watchlist!'})

# Serve static files (e.g., HTML, CSS, JavaScript)
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
