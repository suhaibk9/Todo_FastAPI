from fastapi.testclient import TestClient 
from fastapi import status

try:
    from ..main import app
except ImportError:
    from main import app

client = TestClient(app)


def test_ping_check():
    response = client.get('/ping')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'pint': 'pong'}
    

