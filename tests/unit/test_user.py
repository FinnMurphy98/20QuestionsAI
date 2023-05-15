from app import create_app, db
from app.models import User, Game
from config import TestConfig
from werkzeug.security import generate_password_hash, check_password_hash
import unittest

class TestUserModel(unittest.TestCase):
    """
    Unit test case for the User class. 
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
        GIVEN a user object
        WHEN you get its fields
        THEN those fields should match the arguments passed
        """
        username = 'Bob'
        email = 'bob@email.com'
        user = User(username=username, email=email)
        self.assertEqual(username, user.username)
        self.assertEqual(email, user.email)

    def test_set_password(self):
        """
        GIVEN a user object who's password I just set
        WHEN I set get its password hash
        THEN it should not be Null
        """
        user = User(username='Bob', email='bob@email.com')
        user.set_password('123')
        password_hash = user.password_hash
        self.assertTrue(password_hash != None)

    def test_check_password(self):
        """
        GIVEN a user object whos password_hash has been set
        WHEN I call the check_password with a correct and incorrect password
        THEN check_password() should return True and False respectively
        """
        user = User(username='Bob', email='bob@email.com')
        user.set_password('123')
        self.assertTrue(user.check_password('123'))
        self.assertFalse(user.check_password('456'))
    
    def test_stats(self):
        """
        GIVEN a user, and a bunch of games played by the user
        WHEN I call the user.stats() method
        THEN I should get the correct stats for that user
        """
        user = User(username='Bob', email='bob@email.com')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()
        for i in range(5):
            game = Game(user_id=user.id, role='Answerer', winner=True)
            db.session.add(game)
        for i in range(5):
            game = Game(user_id=user.id, role='Answerer', winner=False)
            db.session.add(game)
        for i in range(5):
            game = Game(user_id=user.id, role='Questioner', winner=True)
            db.session.add(game)
        for i in range(5):
            game = Game(user_id=user.id, role='Questioner', winner=False)
            db.session.add(game)
        db.session.commit()
        stats = user.stats()
        self.assertEqual(stats['total_games'], 20)
        self.assertEqual(stats['total_wins'], 10)
        self.assertEqual(stats['win_rate'], 0.5)
        self.assertEqual(stats['answer_games'], 10)
        self.assertEqual(stats['answer_wins'], 5)
        self.assertEqual(stats['answer_win_rate'], 0.5)
        self.assertEqual(stats['question_games'], 10)
        self.assertEqual(stats['question_wins'], 5)
        self.assertEqual(stats['question_win_rate'], 0.5)