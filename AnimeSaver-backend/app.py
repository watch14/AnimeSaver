from flask import Flask
from flask_pymongo import PyMongo
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

load_dotenv()

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = os.getenv("MONGO_URL_ONLINE_ANIMESAVER")
mongo = PyMongo(app)

# Initialize Swagger
swagger = Swagger(app)

CORS(app)

def create_app():
    # Import blueprints inside the function to avoid circular imports
    from routes.user_routes import bp as user_bp
    from routes.admin_routes import bp as admin_bp
    from routes.anime_routes import anime_bp  # Import the new anime blueprint

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(anime_bp, url_prefix='/api')  # Register with a URL prefix

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
