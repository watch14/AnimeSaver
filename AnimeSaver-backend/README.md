# AnimeSaver API

AnimeSaver is a Flask-based web application that allows users to manage and track their anime watchlists. The application uses MongoDB for data storage and includes features for user management and anime tracking. It also integrates with the MyAnimeList API to provide detailed anime information and rankings.

## Features

- User registration and login
- View, update, and delete user profiles
- Add and remove anime from user watchlists
- Search for anime and fetch detailed information from MyAnimeList
- Retrieve anime rankings, seasonal anime, and suggestions

## Getting Started

### Prerequisites

- Python 3.7 or later
- MongoDB
- Flask
- Flask-PyMongo
- Flasgger (for Swagger documentation)
- `python-dotenv` (for environment variable management)
- `requests` (for making HTTP requests to the MyAnimeList API)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/anime-saver.git
   cd anime-saver
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory with the following content:

   ```env
   MONGO_URL_ONLINE_ANIMESAVER=your_mongodb_connection_string
   ```

5. **Run the application:**

   ```bash
   python app.py
   ```

   or

   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 myapp:app
   ```

   By default, the application will run on `http://127.0.0.1:5000`. You can change the port in the `app.py` file if needed.

## API Endpoints

### User Management

- **Register User**

  - `POST /register`
  - Request body: `{ "userName": "string", "userEmail": "string", "userPassword": "string", "isAdmin": "boolean" }`
  - Response: `{ "message": "User registered successfully!" }`

- **Login User**

  - `POST /login`
  - Request body: `{ "userEmail": "string", "userPassword": "string" }`
  - Response: `{ "message": "Login successful!", "isAdmin": "boolean" }`

- **Get User by ID**

  - `GET /user/<user_id>`
  - Response: `{ "userName": "string", "userEmail": "string", "savedList": [ "anime_id" ], "_id": "string" }`

- **Update User**

  - `PUT /user/<user_id>`
  - Request body: `{ "userName": "string", "userEmail": "string", "userPassword": "string", "isAdmin": "boolean" }`
  - Response: `{ "message": "User updated successfully!" }`

- **Delete User**
  - `DELETE /user/<user_id>`
  - Response: `{ "message": "User deleted successfully!" }`

### Anime Management

- **Search Anime**

  - `GET /anime/search`
  - Parameters:
    - `q` (string, required): Query string to search for anime
    - `limit` (integer, default 10): Number of results to return
    - `offset` (integer, default 0): Offset for pagination
    - `fields` (string, default 'id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status'): Comma-separated list of fields to include in the response

- **Get Anime by ID**

  - `GET /anime/<anime_id>`
  - Parameters:
    - `anime_id` (integer, required): The ID of the anime
    - `fields` (string, default 'title,mean,num_episodes,genres,synopsis,start_date,end_date,status'): Comma-separated list of fields to include in the response

- **Get Anime Ranking**

  - `GET /anime/ranking`
  - Parameters:
    - `ranking_type` (string, default 'all'): Type of ranking (e.g., all, airing, upcoming, tv, movie, bypopularity, favorite)
    - `limit` (integer, default 10): Number of results to return
    - `offset` (integer, default 0): Offset for pagination
    - `fields` (string, default 'id,title,mean,num_episodes,genres,status,rank'): Comma-separated list of fields to include in the response

- **Get Seasonal Anime**

  - `GET /anime/season/<year>/<season>`
  - Parameters:
    - `year` (integer, required): The year of the season
    - `season` (string, required): The season name (e.g., winter, spring, summer, fall)
    - `sort` (string, default 'anime_score'): Sort by (anime_score, anime_num_list_users)
    - `limit` (integer, default 10): Number of results to return
    - `offset` (integer, default 0): Offset for pagination
    - `fields` (string, default 'id,title,mean,num_episodes,genres,status,start_date'): Comma-separated list of fields to include in the response

- **Get Suggested Anime**
  - `GET /anime/suggestions`
  - Parameters:
    - `limit` (integer, default 10): Number of results to return
    - `offset` (integer, default 0): Offset for pagination
    - `fields` (string, default 'id,title,mean,num_episodes,genres,status,start_date'): Comma-separated list of fields to include in the response

### Documentation

Swagger documentation for the API can be accessed at `http://127.0.0.1:5000/apidocs`.

## Contributing

Feel free to open issues or submit pull requests for any bugs or enhancements.
