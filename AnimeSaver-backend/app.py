from flask import Flask
from flask_pymongo import PyMongo
from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = os.getenv("MONGO_URL_ONLINE_ANIMESAVER")
mongo = PyMongo(app)

# Initialize Swagger
swagger = Swagger(app)

def create_app():
    # Import blueprints inside the function to avoid circular imports
    from routes.user_routes import bp as user_bp
    from routes.admin_routes import bp as admin_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
