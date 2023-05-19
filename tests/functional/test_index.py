from tests.conftest import client

def test_status(client):
    """
    GIVEN a an app instance and a client
    WHEN the client GET requests the index page
    THEN it should receive a 200 OK response
    """
    response = client.get('/', content_type='html/text')
    assert response.status_code == 200

if __name__ == '__main__':
    test_status(client)