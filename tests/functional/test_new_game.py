from tests.conftest import client

# TODO
# other test methods involving logged in user

def test_status_not_logged_in(client):
    """
    GIVEN a client that is not logged in
    WHEN they request the a new game page
    THEN they should receive a 302 response
    """
    response1 = client.get('/game/Answerer', content_type='html/text')
    response2 = client.get('/game/Questioner', content_type='html/text')
    assert response1.status_code == 302
    assert response2.status_code == 302

def test_redirect_not_logged_in(client):
    """
    GIVEN a client who is not logged in
    WHEN they request the new game page
    THEN they should be redirected to the login page
    """
    response1 = client.get('/game/Answerer', content_type='html/text', follow_redirects=True)
    response2 = client.get('/game/Questioner', content_type='html/text', follow_redirects=True)
    assert b'Sign In' in response1.data
    assert b'Sign In' in response2.data
    assert b'Please log in to access this page.' in response1.data
    assert b'Please log in to access this page.' in response2.data

if __name__ == '__main__':
    test_status_not_logged_in(client)
    test_redirect_not_logged_in(client)