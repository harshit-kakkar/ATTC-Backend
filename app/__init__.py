from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config.from_object(app_config['config'])

app.config.from_object(app_config['config'])

app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
