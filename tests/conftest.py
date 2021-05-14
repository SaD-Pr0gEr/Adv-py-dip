import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    client = APIClient()
    return client


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

