import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test the GET request to '/' route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PathPilot' in response.data

def test_index_post_valid_input(client):
    """Test POST request with valid interests and skills"""
    response = client.post('/', data={
        'interests': 'technology, creativity',
        'skills': 'python, html, css'
    })
    assert response.status_code == 200
    assert b'Career Suggestions' in response.data or b'Sorry' in response.data

def test_index_post_empty_input(client):
    """Test POST request with empty inputs"""
    response = client.post('/', data={
        'interests': '',
        'skills': ''
    })
    assert response.status_code == 200
    assert b'Career Suggestions' not in response.data
