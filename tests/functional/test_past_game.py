from tests.conftest import client
from app.models import User, Game
from app import db

# TODO
# other test methods involving logged in user

def test_status_not_logged_in(client):
    """
    GIVEN a client that is not logged in
    WHEN they request the past game page
    THEN they should receive a 302 response
    """
    user = User(username='Bob', email='bob@email.com')
    user.set_password('123')
    db.session.add(user)
    db.session.commit()
    game = Game(user_id=user.id, role='Answerer', winner=True, finished=True)
    db.session.add(game)
    db.session.commit()
    path = '/past_game/' + str(game.id)
    response = client.get(path, content_type='html/text')
    assert response.status_code == 302

def test_redirect_not_logged_in(client):
    """
    GIVEN a client who is not logged in
    WHEN they request the new game page
    THEN they should be redirected to the login page
    """
    user = User(username='Bob', email='bob@email.com')
    user.set_password('123')
    db.session.add(user)
    db.session.commit()
    game = Game(user_id=user.id, role='Answerer', winner=True, finished=True)
    db.session.add(game)
    db.session.commit()
    path = '/past_game/' + str(game.id)
    response = client.get(path, content_type='html/text', follow_redirects=True)   
    assert b'Sign In' in response.data
    assert b'Please log in to access this page.' in response.data

if __name__ == '__main__':
    test_status_not_logged_in(client)
    test_redirect_not_logged_in(client)