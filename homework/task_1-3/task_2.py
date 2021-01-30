"""API-Tests for https://api.openbrewerydb.org/breweries"""
import requests
import pytest


@pytest.mark.parametrize("param, value", [('city', 'miami'),
                                          ('state', 'new york'),
                                          ('name', 'mood')])
def test_get_breweries_by_param(base_url, param, value):
    response = requests.get(url = base_url,
                            params={'by_' + param: value})

    assert response.status_code == 200

    print(response.json())
    breweries = response.json()
    for i in range(len(breweries)):
        assert value in breweries[i][param].lower()


@pytest.mark.parametrize("postal_code", ["33139", "2441", "33139-2441", "33139%2D2441", "33139_2441", "33139%5F2441"])
def test_get_breweries_by_postal(base_url, postal_code):
    response = requests.get(base_url + "?by_postal=" + postal_code)
    assert response.status_code == 200

    breweries = response.json()
    for i in range(len(breweries)):
        assert "33139" in breweries[i]['postal_code'].lower()


@pytest.mark.parametrize("brewery_id", [2462, 1232, 1, 232, 45, 8033])
def test_get_brewery_by_id(base_url, brewery_id):
    response = requests.get(base_url + str(brewery_id))

    assert response.status_code == 200
    assert response.json().get("id") == brewery_id


def test_search_brewery(base_url):
    test_word = 92530
    search_word = str(test_word)

    response = requests.get(url=base_url + "search",
                            params={"query=": search_word})

    assert response.status_code == 200
    assert search_word in response.json()[0].get("postal_code")


@pytest.mark.parametrize("name", ["california", "empty", "sunny", "1213"])
def test_use_autocomplete(base_url, name):
    response = requests.get(url=base_url + "autocomplete",
                            params={"query": name})

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.parametrize("method, status", [('post', 404), ('get', 200), ('put', 404), ('delete', 404)])
def test_methods_for_brewery_api(base_url, method, status):
    request = getattr(requests, method)
    response = request(url=base_url)

    assert response.status_code == status
