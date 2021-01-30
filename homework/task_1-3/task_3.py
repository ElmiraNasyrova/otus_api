# API-Tests for https://jsonplaceholder.typicode.com/.

import requests
import pytest


# тестовые данные
data = {
    "title": "test test",
    "body": "test testtest testtest testtest testtest testtest testtest test",
    "userId":3
}


def test_add_new_post(base_url):
    response = requests.get(url=base_url + '/posts')
    last_post_id = len(response.json())

    r = requests.post(url=base_url + '/posts',
                      json=data)

    assert r.status_code == 201

    assert r.json().get("id") == last_post_id + 1
    assert r.json().get("title") == data["title"]
    assert r.json().get("body") == data["body"]
    assert r.json().get("userId") == data["userId"]


@pytest.mark.parametrize("post_id", [1, 23, 99, 100])
def test_update_post(base_url, post_id):
    id = str(post_id)

    response = requests.get(url=base_url + '/posts/' + id)
    edit_data = response.json()
    edit_data.update(title=data["title"], body=data["body"])

    r = requests.put(url=base_url + '/posts/' + id,
                     json=edit_data)

    assert r.status_code==200

    assert r.json().get("id") == post_id
    assert r.json().get("userId") == edit_data["userId"]
    assert r.json().get("title") == edit_data["title"]
    assert r.json().get("body") == edit_data["body"]


def test_patch_post(base_url):
    old_response = requests.get(url=base_url + '/posts/23')

    r = requests.patch(url=base_url + '/posts/23',
                       json=data)

    assert r.status_code==200

    assert r.json().get("id") == old_response.json().get("id")
    assert r.json().get("userId") == old_response.json().get("userId")
    assert r.json().get("title") == data["title"]
    assert r.json().get("body") == data["body"]


@pytest.mark.parametrize("endpoint, status_code",
                         [("/posts/1/comments", 200),
                          ("/posts/1/comment", 404),
                          ("/comments?postId=1", 200),
                          ("/comment?postId=1", 404)])
def test_get_post_comments(base_url, endpoint, status_code):
    r = requests.get(url=base_url + endpoint)

    assert r.status_code==status_code

    for comment in r.json():
        assert comment.get("postId") == 1
        assert comment.get("email") != []
        assert comment.get("name") != []

@pytest.mark.parametrize("post_id, status_code",
                         [("1", 200),
                          ("32" , 200),
                          ("100", 200),
                          ("0", 200),
                          ("101", 200),
                          ("+12323d", 200)])
def test_delete_post(base_url, post_id, status_code):
    r = requests.delete(url=base_url + '/posts/' + post_id)

    assert r.status_code == status_code
