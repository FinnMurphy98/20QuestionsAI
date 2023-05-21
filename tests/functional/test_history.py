from tests.conftest import client

def test_status_not_logged_in(client):
    """
    GIVEN a client who is not logged in
    WHEN they request the history page
    THEN they should receive a 302 response
    """
    response = client.get('/history', content_type='html/text')
    assert response.status_code == 302

def test_redirect_not_logged_in(client):
    """
    GIVEN a client who is not logged in
    WHEN they request the history page
    THEN they should be be temporarily redirected to the login page
    """
    response = client.get('/history', content_type='html/text', follow_redirects=True)
    assert b'Sign In' in response.data
    assert b'Please log in to access this page.' in response.data

if __name__ == '__main__':
    test_status_not_logged_in(client)
    test_redirect_not_logged_in(client)