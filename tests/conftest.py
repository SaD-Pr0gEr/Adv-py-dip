import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def authorize():
    def return_client(token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        return client
    return return_client


@pytest.fixture
def product_fabric():
    def create(**kwargs):
        return baker.make("shop.product", **kwargs)
    return create


@pytest.fixture
def product_comment_fabric():
    def create(**kwargs):
        return baker.make("shop.productcomment", **kwargs)
    return create


@pytest.fixture
def orders_fabric():
    def create(**kwargs):
        return baker.make("shop.orders", **kwargs)
    return create


@pytest.fixture
def collections_fabric():
    def create(**kwargs):
        return baker.make("shop.collections", **kwargs)
    return create


@pytest.fixture
def user_fabric():
    def create(**kwargs):
        return baker.make("shop.User", **kwargs)
    return create


@pytest.fixture
def token_fabric():
    def create(**kwargs):
        return Token.objects.create(**kwargs)
    return create
