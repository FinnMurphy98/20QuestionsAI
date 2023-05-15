from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    """
    User database model. 
    Username and email must be unique.
    games field is a list of all games played by the user.  
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    games = db.relationship('Game', backref='player', lazy='dynamic')
    __tablename__ = 'User'

    def __repr__(self):
        return '<User: {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def stats(self):
        """
        Calculate and return the users game statistics 
        """
        total_games = self.games.count()
        answer_games = 0
        answer_wins = 0
        question_games = 0
        question_wins = 0
        for game in self.games:
            if game.role == 'Answerer':
                answer_games += 1
                if game.winner:
                    answer_wins += 1
            else:
                question_games += 1
                if game.winner:
                    question_wins += 1
        total_wins = answer_wins + question_wins
        win_rate = 0
        if total_games > 0:
            win_rate = round(total_wins / total_games, 2)
        answer_win_rate = 0
        if answer_games > 0:
            answer_win_rate = round(answer_wins / answer_games, 2)
        question_win_rate = 0
        if question_games > 0:
            question_win_rate = round(question_wins / question_games, 2)
        stats = {
            "total_games": total_games, "total_wins": total_wins, "win_rate": win_rate, 
            "answer_games": answer_games, "answer_wins": answer_wins, "answer_win_rate": answer_win_rate,
            "question_games": question_games, "question_wins": question_wins, "question_win_rate": question_win_rate
        }
        return stats

class Game(db.Model):
    """
    Game database model. 
    timestamp is created when committed to database. 
    role is either 'Questioner' or 'Answerer'. 
    winner is True or False.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    role = db.Column(db.String(64), nullable=False)
    winner = db.Column(db.Boolean, nullable=False)
    messages = db.relationship('Message', backref='game', lazy='dynamic')
    __tablename__ = 'Game'

    def __repr__(self):
        return '<Role: {}, Winner: {}>'.format(self.role, self.winner)

class Message(db.Model):
    """
    Message database model. 
    Every message belongs to a game (game_id).
    role is either 'user' (was sent by a user) or 'assistant' (was sent by ChatGPT).
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String())
    __tablename__ = 'Message'

    def __repr__(self):
        return '<Role: {}, Content: {}'.format(self.role, self.content)