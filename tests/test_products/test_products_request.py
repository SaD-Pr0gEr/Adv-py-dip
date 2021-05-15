from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest

from shop.models import Orders, OrderPositions, Collections, Product, ProductComment, User


@pytest.mark.django_db
def test_request_list_products(client, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    quantity = 2
    product = product_fabric(_quantity=quantity)
    url = reverse("products-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert len(response.json()) == quantity and response.status_code == 200


@pytest.mark.django_db
def test_request_retrieve_product(client, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    product = product_fabric()
    url = reverse("products-detail", args=(product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.json()["id"] == product.id and response.status_code == 200


@pytest.mark.django_db
def test_request_post_product(client, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    url = reverse("products-list")
    json = {
        "name": "something",
        "description": "some test",
        "price": 1000,
    }

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    resposne = client.post(url, data=json)

    # assert
    assert resposne.status_code == 201 and resposne.data["name"] == json["name"]


@pytest.mark.django_db
def test_request_patch_product(client, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    create_product = product_fabric()
    url = reverse("products-detail", args=(create_product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    patch = {
        "name": "something",
        "description": "something_else"
    }
    response = client.patch(url, data=patch)
    assert response.status_code == 200 and response.data["id"] == create_product.id


@pytest.mark.django_db
def test_request_delete_product(client, product_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    create_product = product_fabric()
    url = reverse("products-detail", args=(create_product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.delete(url)
    assert response.status_code == 204
