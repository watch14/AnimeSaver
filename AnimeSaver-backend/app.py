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

CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (adjust as needed)

def create_app():
    # Import blueprints inside the function to avoid circular imports
    from routes.user_routes import bp as user_bp
    from routes.admin_routes import bp as admin_bp
    from routes.anime_routes import anime_bp  
    from routes.share_routes import share_bp  

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(anime_bp, url_prefix='/api')
    app.register_blueprint(share_bp, url_prefix='/api')
    return app



@app.route('/')
def hello():
    return "swagger : https://animesaver-backend.onrender.com/apidocs/"
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
