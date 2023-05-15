from app import create_app, db
from config import DevConfig
from app.models import User, Game, Message
import openai

app = create_app(config_class=DevConfig)
openai.api_key = app.config.get('OPENAI_KEY')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game, 'Message': Message}