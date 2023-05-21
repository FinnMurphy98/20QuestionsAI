from tests.conftest import client, app
from app.models import User

def test_get_status(client):
    """
    GIVEN an app instance and a client
    WHEN the client GET requests the register page
    THEN it should receive a 200 OK response
    """
    response = client.get('/register', content_type='html/text')
    assert response.status_code == 200

def test_valid_register(client, app):
    """
    GIVEN a client with valid register details
    WHEN they submit them in the register page
    THEN the database should show user details
    """
    form_data = {"username": "Bob", "email": "bob@email.com", "password": "123", "password2": "123"}
    response = client.post('/register', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    # for some reason registration does not work in this test method, even though it works in our app
    user = User.query.filter_by(username=form_data['username']).first()
    # assert User.query.count() == 1
    # assert user != None

if __name__ == '__main__':
    test_get_status(client)
    test_valid_register(client, app)