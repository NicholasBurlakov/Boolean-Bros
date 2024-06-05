"""
PyTests for ParkSmart Functionality
"""

"""
Tests For Home Page
"""


def test_index_page_load(client):
    """Test that the index page loads correctly."""
    response = client.get('/index.html')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data


def test_index_navigation_links(client):
    """Test the presence of navigation links on the index page."""
    response = client.get('/index.html')
    assert b"Team" in response.data
    assert b"Services" in response.data
    assert b"Contact" in response.data
    assert b"Parking Availability" in response.data
    assert b"Login" in response.data


def test_index_main_sections(client):
    """Test that main content sections are present."""
    response = client.get('/index.html')
    assert b"OUR TEAM" in response.data
    assert b"How to park guide" in response.data
    assert b"Contact Us" in response.data


def test_index_dynamic_content(client):
    """Test dynamic content like images and user-specific elements."""
    response = client.get('/index.html')
    # Assuming there's a check for a logged-in user or other dynamic conditions:
    # Adjust the path or session condition as per your app logic
    assert b"empty_parking" in response.data  # Check if the image loads correctly


def test_index_javascript_presence(client):
    """Test the presence of JavaScript for functionality."""
    response = client.get('/index.html')
    assert b"w3_open()" in response.data
    assert b"w3_close()" in response.data
    assert b"openNav()" in response.data


"""
Tests For Availability
"""


def test_parking_availability_page_load(client):
    """Test that the parking availability page loads correctly."""
    response = client.get('/availability.html')
    assert response.status_code == 200
    assert b"Parking Availability" in response.data
    assert b"<title>Parking Availability</title>" in response.data


def test_parking_availability_navigation_links(client):
    """Test the navigation links on the parking availability page."""
    response = client.get('/availability.html')
    assert b"Team" in response.data
    assert b"Services" in response.data
    assert b"Contact" in response.data
    assert b"Login" in response.data


def test_parking_availability_search_input(client):
    """Test for presence of the search input on the parking availability page."""
    response = client.get('/availability.html')
    assert b'<input class="search-input"' in response.data


def test_parking_availability_grid_container(client):
    """Test that the parking grid container is present."""
    response = client.get('/availability.html')
    assert b'id="parking-grid"' in response.data


def test_parking_availability_reservation_section(client):
    """Test the reservation section and button."""
    response = client.get('/availability.html')
    assert b'id="reservation-section"' in response.data
    assert b'<button id="reserve-button"' in response.data


"""
Tests For Checkout
"""


def test_checkout_page_load(client):
    """Test that the checkout page loads correctly."""
    response = client.get('/checkout')
    assert response.status_code == 200
    assert b"Responsive Checkout Form" in response.data


def test_checkout_form_elements(client):
    """Test the presence of essential form elements on the checkout page."""
    response = client.get('/checkout')
    # Personal Information
    assert b'<input type="text" id="fname"' in response.data
    assert b'<input type="text" id="email"' in response.data
    assert b'<input type="text" id="adr"' in response.data
    # Payment Information
    assert b'<input type="text" id="cname"' in response.data
    assert b'<input type="text" id="ccnum"' in response.data
    assert b'<input type="text" id="expmonth"' in response.data
    # CVV and other credit card details
    assert b'<input type="text" id="cvv"' in response.data
    assert b'<input type="submit"' in response.data  # Check for submit button


"""
Tests For Register
"""


def test_register_page_load(client):
    """Test that the register page loads correctly."""
    response = client.get('/register.html')
    assert response.status_code == 200
    assert b"Register - ParkSmart" in response.data
    assert b"<title>Register - ParkSmart</title>" in response.data


def test_register_form_elements(client):
    """Test the presence of essential form elements on the register page."""
    response = client.get('/register.html')
    assert b'<input type="email"' in response.data
    assert b'<input type="text" id="username"' in response.data
    assert b'<input type="password"' in response.data
    assert b'<select id="vehicle-type"' in response.data
    assert b'<select id="color"' in response.data
    assert b'<button type="submit"' in response.data  # Adjusted to check for button tag


def test_register_form_submission_setup(client):
    """Test the form setup for submission."""
    response = client.get('/register.html')
    form_action = response.data.decode().find('<form method="POST">')
    assert form_action != -1  # Confirm form is set to post, indicating correct setup for submission


def test_navigation_and_login_link(client):
    """Test navigation and transition links on the registration page."""
    response = client.get('/register.html')
    assert b"Team" in response.data
    assert b"Services" in response.data
    assert b"Contact" in response.data
    assert b"Parking Availability" in response.data
    assert b"Already have an account? Login" in response.data
