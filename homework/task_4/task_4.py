import requests


def test(base_url,status_code):
    response = requests.get(base_url)

    assert response.status_code == status_code
