from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest

from shop.models import Orders, OrderPositions, Collections, Product, ProductComment, User


@pytest.mark.django_db
def test_request_list_collections(client, collections_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    quantity = 10
    collections_fabric(_quantity=quantity)
    url = reverse("product_collections-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200 and len(response.data) == quantity


@pytest.mark.django_db
def test_request_retrieve_collections(client, collections_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    collection = collections_fabric()
    url = reverse("product_collections-detail", args=(collection.id, ))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200 and response.data["id"] == collection.id


@pytest.mark.django_db
def test_request_post_collections(client, product_fabric, collections_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    url = reverse("product_collections-list")
    product1 = product_fabric()
    product2 = product_fabric()
    data = {
        "header": "test",
        "text": "test",
        "product": [product1.id, product2.id]
    }

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.post(url, data)

    # assert
    assert response.status_code == 201 and response.data["header"] == data["header"]


@pytest.mark.django_db
def test_request_patch_collections(client, product_fabric, collections_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    collection1 = collections_fabric()
    url = reverse("product_collections-detail", args=(collection1.id, ))
    product1 = product_fabric()
    product2 = product_fabric()
    data = {
        "header": "test",
        "text": "test",
        "product": [product1.id, product2.id]
    }

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.patch(url, data)

    # assert
    assert response.status_code == 200 and response.data["product"][0] == product1.id


@pytest.mark.django_db
def test_request_delete_collections(client, product_fabric, collections_fabric, user_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = Token.objects.create(user=user)
    collection1 = collections_fabric()
    url = reverse("product_collections-detail", args=(collection1.id, ))
    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.delete(url)

    # assert
    assert response.status_code == 204
