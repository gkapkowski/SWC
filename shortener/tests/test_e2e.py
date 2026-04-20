import pytest
from urllib.parse import urlsplit
from rest_framework.test import APIClient


@pytest.fixture
def long_url() -> str:
    return "https://somewhat.long.url/for-shortening?param1=abc&param2=bcd"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def test_create_short_url(api_client: APIClient, long_url: str):
    # TODO: make sure the DB will generate ID of known value
    response = api_client.post("/shorten/", {"url": long_url})
    assert response.status_code == 201, f"Invalid response: {response.status_code} {response.content}"
    data = response.json()
    assert "short_url" in data
    assert "url" in data
    assert data["short_url"].startswith("http://")
    assert data["url"] == long_url


@pytest.mark.django_db
def test_create_short_url_with_invalid_input(api_client: APIClient):
    # TODO: make sure the DB will generate ID of known value
    response = api_client.post("/shorten/", {"url": "I'm not an url"})
    assert response.status_code == 400
    data = response.json()
    assert data["url"] == ["Enter a valid URL."]


@pytest.mark.django_db
def test_redirect_to_original_url(api_client: APIClient, long_url: str):
    response = api_client.post(
        "/shorten/",
        {"url": long_url},
    )
    assert response.status_code == 201, "Failed to create short URL"
    url = response.json()["short_url"]
    path = urlsplit(url).path
    response = api_client.get(path)
    assert response.status_code == 302
    assert response["location"] == long_url


@pytest.mark.django_db
def test_invalid_url(api_client: APIClient, long_url: str):
    response = api_client.get("/i-do-not-exist")
    assert response.status_code == 404
