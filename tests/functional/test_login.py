from tests.conftest import client

def test_get_status(client):
    """
    GIVEN an app instance and a client
    WHEN the client GET requests the login page
    THEN it should receive a 200 OK response
    """
    response = client.get('/login', content_type='html/text')
    assert response.status_code == 200

def test_valid_login(client):
    """
    GIVEN an app instance and a client
    WHEN the client tries to log in with valid credentials
    THEN it should receive a 200 OK, and be redirected to user home page
    """
    form_data = {"username": 'Bob', "password": "123"}
    response = client.post('/login', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Bob' in response.data

def test_invalid_login(client):
    """
    GIVEN an app instance and a client
    WHEN the client tries to log in with invalid credentials
    THEN it should receive a 200 OK but be redirected back to login page
    """
    login_data = {"username": "Bill", "password": "12345"}
    response = client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data

def test_no_username(client):
    """
    GIVEN a client trying to log in
    WHEN they omit a username
    THEN they should get a 200 OK, but be redirected back to login
    """
    login_data = {"password": "123"}
    response = client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data
    assert b'This field is required.' in response.data

def test_no_password(client):
    """
    GIVEN a client trying to log in
    WHEN they omit a password
    THEN they should get a 200 OK, but be redirected back to login
    """
    login_data = {"username": "Bob"}
    response = client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data
    assert b'This field is required.' in response.data

if __name__ == '__main__':
    test_get_status(client)
    test_valid_login(client)
    test_invalid_login(client)
    test_no_username(client)
    test_no_password(client)