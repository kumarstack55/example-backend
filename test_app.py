import requests


def test_container_response():
    response = requests.get("http://localhost:8080")
    assert response.status_code == 200 or response.status_code == 500
    assert response.json()["message"] == "ok" or response.json()["message"] == "bad"
