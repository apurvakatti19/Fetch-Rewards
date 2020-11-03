import numpy as np
import json
import pytest
np.set_printoptions(suppress=True)

from server import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_points(client):
    response = client.post('http://127.0.0.1:5000/add_points',
    json = {"payerName":"DANNON","points":300,"transactionDate":"10/31 10AM"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_points',
    json = {"payerName":"UNILEVER","points":200,"transactionDate":"10/31 11AM"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_points',
    json = {"payerName":"DANNON","points":-200,"transactionDate":"10/31 3PM"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_points',
    json = {"payerName":"MILLER COORS","points":10000,"transactionDate":"11/1 2PM"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_points',
    json = {"payerName":"DANNON","points":1000,"transactionDate":"11/2 2PM"})
    assert response.status_code == 200

def test_delete_points(client):
    response = client.delete('http://127.0.0.1:5000/delete_points',json={"points_to_deduct":5000})
    print(response.data)
    assert response.status_code == 200

def test_balance(client):
    response = client.get('http://127.0.0.1:5000/balance')
    print(response.data)

    assert response.status_code == 200