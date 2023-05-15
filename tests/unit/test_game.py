from app import create_app, db
from app.models import User, Game
from config import TestConfig
import unittest

class TestGameModel(unittest.TestCase):
    """
    Unit test case for the Game class. 
    """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
        """
        GIVEN a newly created Game object
        WHEN I get its fields
        THEN those fields should be equal to the ones passed in the constructor
        """
        user = User(username='Bob', email='bob@email.com')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()
        role = 'Answerer'
        winner = True
        game = Game(user_id=user.id, role=role, winner=winner)
        self.assertEqual(game.user_id, user.id)
        self.assertEqual(game.role, role)
        self.assertEqual(game.winner, winner)
