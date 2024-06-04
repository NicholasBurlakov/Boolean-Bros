def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Check if the response is a valid HTML document
    assert b"ParkSmart" in response.data  # Check for specific text in the HTML content


def test_login_page(client):
    response = client.get('/login.html')
    assert response.status_code == 200
    assert b"Login" in response.data

# Add more tests as needed
