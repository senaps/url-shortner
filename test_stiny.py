import pytest

from stiny import create_app, make_shorten, shorten_url


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    yield app.test_client()


def test_ping(client):
    assert client.get("/ping/").status == "200 OK"


def test_make_shorten():
    assert len(make_shorten()) == 8


# def test_create_tiny(client):
#     url = "https://www.google.com/"
#     assert client.post("/", data={"url": url}).status == "201 CREATED"
#
    
