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

# Import routes
from routes import user_routes, admin_routes

app.register_blueprint(user_routes.bp)
app.register_blueprint(admin_routes.bp)

if __name__ == '__main__':
    app.run(debug=True)
