from flask import Blueprint, jsonify, request
import requests
import os
from flasgger import Swagger, swag_from
import pymongo

# Define the Blueprint
anime_bp = Blueprint('anime_routes', __name__)

# API configuration
CLIENT_ID = 'dfe48b7bb1e8af63efd5cd846dee89db'
MYANIMELIST_API_URL = 'https://api.myanimelist.net/v2/anime'


# Database configuration
MONGO_URI = os.getenv("MONGO_URL_ONLINE_ANIMESAVER")
client = pymongo.MongoClient(MONGO_URI)
db = client['Flask-API']
users_collection = db['users']

# Helper function to make a request to the MyAnimeList API
def make_mal_request(endpoint, params=None):
    headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}, 500


@anime_bp.route('/anime/search', methods=['GET'])
@swag_from({
    'tags': ['Anime Search'],
    'summary': 'Search for anime by query string',
    'description': 'Search for anime using a query string. Supports pagination and field selection.',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Query string to search for anime'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Number of results to return'
        },
        {
            'name': 'offset',
            'in': 'query',
            'type': 'integer',
            'default': 0,
            'description': 'Offset for pagination'
        },
        {
            'name': 'fields',
            'in': 'query',
            'type': 'string',
            'default': 'id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status',
            'description': 'Comma-separated list of fields to include in the response'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of anime that match the query',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object'
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        '500': {
            'description': 'Server error',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    }
})
def search_anime():
    print(users_collection)

    query = request.args.get('q')
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    fields = request.args.get('fields', 'id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status')

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    params = {
        'q': query,
        'limit': limit,
        'offset': offset,
        'fields': fields
    }
    endpoint = f'{MYANIMELIST_API_URL}'
    result = make_mal_request(endpoint, params)
    return jsonify(result)


@anime_bp.route('/anime/<anime_id>', methods=['GET'])
@swag_from({
    'tags': ['Anime Search'],
    'summary': 'Get anime details by ID',
    'description': 'Retrieve detailed information about a specific anime using its ID.',
    'parameters': [
        {
            'name': 'anime_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the anime'
        },
        {
            'name': 'fields',
            'in': 'query',
            'type': 'string',
            'default': 'title,mean,num_episodes,genres,synopsis,start_date,end_date,status',
            'description': 'Comma-separated list of fields to include in the response'
        }
    ],
    'responses': {
        '200': {
            'description': 'Details of the anime',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'mean': {'type': 'number'},
                    'num_episodes': {'type': 'integer'},
                    'genres': {'type': 'array', 'items': {'type': 'string'}},
                    'synopsis': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'end_date': {'type': 'string', 'format': 'date'},
                    'status': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Invalid ID supplied',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        '404': {
            'description': 'Anime not found',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        '500': {
            'description': 'Server error',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    }
})
def get_anime_by_id(anime_id):
    fields = request.args.get('fields', 'title,mean,num_episodes,genres,synopsis,start_date,end_date,status')
    endpoint = f'{MYANIMELIST_API_URL}/{anime_id}'
    params = {
        'fields': fields
    }
    result = make_mal_request(endpoint, params)
    return jsonify(result)


@anime_bp.route('/anime/ranking', methods=['GET'])
@swag_from({
    'tags': ['Anime Search'],
    'summary': 'Get anime ranking',
    'description': 'Retrieve a list of top-ranked anime based on the selected ranking type.',
    'parameters': [
        {
            'name': 'ranking_type',
            'in': 'query',
            'type': 'string',
            'default': 'all',
            'description': 'Type of ranking (e.g., all, airing, upcoming, tv, movie, bypopularity, favorite)'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Number of results to return'
        },
        {
            'name': 'offset',
            'in': 'query',
            'type': 'integer',
            'default': 0,
            'description': 'Offset for pagination'
        },
        {
            'name': 'fields',
            'in': 'query',
            'type': 'string',
            'default': 'id,title,mean,num_episodes,genres,status,rank',
            'description': 'Comma-separated list of fields to include in the response'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of top-ranked anime',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object'
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Server error',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    }
})
def get_anime_ranking():
    ranking_type = request.args.get('ranking_type', 'all')
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    fields = request.args.get('fields', 'id,title,mean,num_episodes,genres,status,rank')

    params = {
        'ranking_type': ranking_type,
        'limit': limit,
        'offset': offset,
        'fields': fields
    }
    endpoint = f'{MYANIMELIST_API_URL}/ranking'
    result = make_mal_request(endpoint, params)
    return jsonify(result)

@anime_bp.route('/anime/season/<int:year>/<season>', methods=['GET'])
@swag_from({
    'tags': ['Anime Search'],
    'summary': 'Get seasonal anime',
    'description': 'Retrieve a list of anime released in a specific season and year.',
    'parameters': [
        {
            'name': 'year',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The year of the season'
        },
        {
            'name': 'season',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The season name (e.g., winter, spring, summer, fall)'
        },
        {
            'name': 'sort',
            'in': 'query',
            'type': 'string',
            'default': 'anime_score',
            'description': 'Sort by (anime_score, anime_num_list_users)'
        },
        {
            'name': 'sort_order',
            'in': 'query',
            'type': 'string',
            'default': 'desc',
            'description': 'Sort order (asc or desc)'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Number of results to return'
        },
        {
            'name': 'offset',
            'in': 'query',
            'type': 'integer',
            'default': 0,
            'description': 'Offset for pagination'
        },
        {
            'name': 'fields',
            'in': 'query',
            'type': 'string',
            'default': 'id,title,mean,num_episodes,genres,status,start_date',
            'description': 'Comma-separated list of fields to include in the response'
        },
        {
            'name': 'min_rating',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'description': 'Minimum rating to filter results'
        },
        {
            'name': 'max_rating',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'description': 'Maximum rating to filter results'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of seasonal anime',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object'
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Server error',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    }
})
def get_seasonal_anime(year, season):
    sort = request.args.get('sort', 'anime_score')
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    fields = request.args.get('fields', 'id,title,mean,num_episodes,genres,status,start_date')
    min_rating = request.args.get('min_rating', type=float)
    max_rating = request.args.get('max_rating', type=float)
    sort_order = request.args.get('sort_order', 'desc')

    params = {
        'sort': sort,
        'limit': limit,
        'offset': offset,
        'fields': fields
    }
    
    endpoint = f'{MYANIMELIST_API_URL}/season/{year}/{season}'
    result = make_mal_request(endpoint, params)

    # Filter results based on min_rating and max_rating if provided
    if min_rating is not None or max_rating is not None:
        filtered_data = []
        for item in result.get('data', []):
            rating = item.get('node', {}).get('mean', 0)
            if (min_rating is None or rating >= min_rating) and (max_rating is None or rating <= max_rating):
                filtered_data.append(item)
        result['data'] = filtered_data

    # Sort results based on sort_order if applicable
    if sort == 'mean':
        result['data'].sort(key=lambda x: x['node'].get('mean', 0), reverse=(sort_order == 'desc'))

    return jsonify(result)

# @anime_bp.route('/anime/suggestions', methods=['GET'])
# @swag_from({
#     'tags': ['Anime Search'],
#     'summary': 'Get suggested anime',
#     'description': 'Retrieve a list of anime suggested for the authenticated user.',
#     'parameters': [
#         {
#             'name': 'limit',
#             'in': 'query',
#             'type': 'integer',
#             'default': 10,
#             'description': 'Number of results to return'
#         },
#         {
#             'name': 'offset',
#             'in': 'query',
#             'type': 'integer',
#             'default': 0,
#             'description': 'Offset for pagination'
#         },
#         {
#             'name': 'fields',
#             'in': 'query',
#             'type': 'string',
#             'default': 'id,title,mean,num_episodes,genres,status,start_date',
#             'description': 'Comma-separated list of fields to include in the response'
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'A list of suggested anime',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'data': {
#                         'type': 'array',
#                         'items': {
#                             'type': 'object'
#                         }
#                     }
#                 }
#             }
#         },
#         '500': {
#             'description': 'Server error',
#             'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
#         }
#     }
# })
# def get_suggested_anime():
#     limit = request.args.get('limit', 10)
#     offset = request.args.get('offset', 0)
#     fields = request.args.get('fields', 'id,title,mean,num_episodes,genres,status,start_date')

#     params = {
#         'limit': limit,
#         'offset': offset,
#         'fields': fields
#     }
#     endpoint = f'{MYANIMELIST_API_URL}/suggestions'
#     headers = {
#         'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your actual token
#     }
#     response = requests.get(endpoint, headers=headers, params=params)

#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return jsonify({'error': response.json().get('error', 'An error occurred')}), response.status_code
