from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    games = db.relationship('Game', backref='player', lazy='dynamic')
    __tablename__ = 'User'

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    questioner = db.Column(db.Boolean)
    winner = db.Column(db.Boolean)
    __tablename__ = 'Game'

    def __repr__(self):
        return '<Questioner {}, Winner {}>'.format(self.questioner, self.winner)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))