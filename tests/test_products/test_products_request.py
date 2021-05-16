from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest


@pytest.mark.django_db
def test_request_list_products(authorize, token_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
    quantity = 2
    product_fabric(_quantity=quantity)
    url = reverse("products-list")
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert len(response.json()) == quantity and response.status_code == 200


@pytest.mark.django_db
def test_request_retrieve_product(authorize, token_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
    product = product_fabric()
    url = reverse("products-detail", args=(product.id,))
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert response.json()["id"] == product.id and response.status_code == 200


@pytest.mark.django_db
def test_request_post_product(authorize, token_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    url = reverse("products-list")
    json = {
        "name": "something",
        "description": "some test",
        "price": 1000,
    }
    client = authorize(token)

    # act
    resposne = client.post(url, data=json)

    # assert
    assert resposne.status_code == 201 and resposne.data["name"] == json["name"]


@pytest.mark.django_db
def test_request_patch_product(authorize, token_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    create_product = product_fabric()
    url = reverse("products-detail", args=(create_product.id,))
    client = authorize(token)
    patch = {
        "name": "something",
        "description": "something_else"
    }

    # act
    response = client.patch(url, data=patch)
    assert response.status_code == 200 and response.data["id"] == create_product.id


@pytest.mark.django_db
def test_request_delete_product(authorize, token_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    create_product = product_fabric()
    url = reverse("products-detail", args=(create_product.id,))
    client = authorize(token)

    # act
    response = client.delete(url)
    assert response.status_code == 204
