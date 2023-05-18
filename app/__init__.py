from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

bp = Blueprint('app', __name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
socketio = SocketIO()

def create_app(config_class=Config):
    """
    Creates an instance of the flask application with a specified Config class. 
    Initializes extensions.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    socketio.init_app(app, namespaces=['/game/Answerer', '/game/Questioner'])
    app.register_blueprint(bp)
    return app

ANSWERER_PROMPT = "Let's play a game of 20 questions. I'll be the answerer, which means I have to think of \
    a person, place or thing. You be the questioner. Remember, your only allowed to ask questions that have \
    yes or no answers, and you have a maximum of 20 questions. Ok, I've thought of something. Now, ask your \
    first question."

QUESTIONER_PROMPT = "Let's play a game of 20 questions. You can be the answerer, which means you have to \
    think of a person, place or thing. I'll be the questioner, which means I have to ask you questions to \
    which you can only respond yes or no. I have to guess correctly in 20 questions or less. Are you ready?"

from app import routes, models