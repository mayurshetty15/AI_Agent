import pytest
from panel.app import app
import panel.database as db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b'alice@company.com' in response.data

def test_create_user_valid(client):
    response = client.post('/users/create', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'Developer',
        'status': 'Active',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'User created successfully' in response.data

def test_create_user_invalid_email(client):
    response = client.post('/users/create', data={
        'name': 'Test User',
        'email': 'invalidemail',
        'role': 'Developer',
        'status': 'Active',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Email must contain @ and .' in response.data

def test_reset_password_valid(client):
    response = client.post('/reset-password', data={
        'email': 'bob@company.com',
        'new_password': 'newpass123'
    })
    assert response.status_code == 200
    assert b'Password reset for bob@company.com' in response.data

def test_reset_password_invalid(client):
    response = client.post('/reset-password', data={
        'email': 'nonexistent@example.com',
        'new_password': 'newpass123'
    })
    assert response.status_code == 200
    assert b'User not found.' in response.data

def test_licenses(client):
    response = client.get('/licenses')
    assert response.status_code == 200

def test_assign_license(client):
    # Get a user id, assuming alice is id 1
    response = client.post('/licenses/assign', data={
        'user_id': 1,
        'license': 'GitHub'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'License assigned successfully' in response.data