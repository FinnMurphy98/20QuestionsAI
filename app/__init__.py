from flask import Flask
from config import Config, DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
import openai

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
socketio = SocketIO(app)
openai.api_key = app.config.get('OPENAI_KEY')

def create_app(config_class=Config):
    """
    Creates an instance of the flask application with a specified Config class. 
    Initializes extensions.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app, db)
    migrate.init_app(app)
    login.init_app(app)
    socketio.init_app(app)
    openai.api_key = app.config.get('OPENAI_KEY')
    return app

from app import routes, models