from app import create_app, db
from app.models import User, Game
from config import TestConfig
from sqlalchemy.exc import IntegrityError
import unittest
import pytest

class TestGameModel(unittest.TestCase):
    """
    Unit test case for the Game class. 
    """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(username='Bob', email='bob@email.com')
        self.user.set_password('123')
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_repr(self):
        """
        GIVEN a game object
        WHEN you call repr method
        THEN it should produce the expected string
        """
        game = Game(user_id=self.user.id, role='Questioner', winner=True)
        result = game.__repr__()
        expected = "<Role: Questioner, Winner: True>"
        self.assertEqual(result, expected)
    
    def test_userid_not_nullable(self):
        """
        GIVEN a game with no user_id
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        game = Game(role='Answerer', winner=True)
        db.session.add(game)
        with pytest.raises(IntegrityError):
            db.session.commit()
    
    def test_role_not_nullable(self):
        """
        GIVEN a game with no role
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        game = Game(user_id=self.user.id, winner=True)
        db.session.add(game)
        with pytest.raises(IntegrityError):
            db.session.commit()
    
    def test_winner_not_nullable(self):
        """
        GIVEN a game with no winner
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        game = Game(user_id=self.user.id, role='Questioner')
        db.session.add(game)
        with pytest.raises(IntegrityError):
            db.session.commit()

if __name__ == '__main__':
    unittest.main()