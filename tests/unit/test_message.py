from app import create_app, db
from app.models import User, Game, Message
from config import TestConfig
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import unittest
import pytest

class TestMessageModel(unittest.TestCase):
    """
    Unit test case for the Message class. 
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
        self.game = Game(user_id=self.user.id, role='Questioner', winner=False)
        db.session.add(self.game)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_repr(self):
        """
        GIVEN a message object
        WHEN you call repr method
        THEN it should produce the expected string
        """
        message = Message(timestamp=datetime.utcnow(), game_id=self.game.id, role='user', content='hello there')
        result = message.__repr__()
        expected = '<Role: user, Content: hello there>'
        self.assertEqual(result, expected)

    def test_timestamp_not_nullable(self):
        """
        GIVEN a message with no timestamp
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        message = Message(game_id=self.game.id, role='assistant', content='how may I assist you?')
        db.session.add(message)
        with pytest.raises(IntegrityError):
            db.session.commit()
    
    def test_gameid_not_nullable(self):
        """
        GIVEN a message with no game_id
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        message = Message(timestamp=datetime.utcnow(), role='user', content='hello there')
        db.session.add(message)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_role_not_nullable(self):
        """
        GIVEN a message with no role
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        message = Message(timestamp=datetime.utcnow(), game_id=self.game.id, content='hello there')
        db.session.add(message)
        with pytest.raises(IntegrityError):
            db.session.commit()
    
    def test_content_not_nullable(self):
        """
        GIVEN a message with no content
        WHEN it is committed to the database
        THEN it should cause an integrity error
        """
        message = Message(timestamp=datetime.utcnow(), game_id=self.game.id, role='user')
        db.session.add(message)
        with pytest.raises(IntegrityError):
            db.session.commit()

if __name__ == '__main__':
    unittest.main()