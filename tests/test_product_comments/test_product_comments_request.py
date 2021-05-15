from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest

from shop.models import Orders, OrderPositions, Collections, Product, ProductComment, User


@pytest.mark.django_db
def test_request_list_product_comments(client, product_comment_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    quantity = 20
    product = product_comment_fabric(_quantity=quantity)
    url = reverse("product_reviews-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert len(response.json()) == quantity and response.status_code == 200


@pytest.mark.django_db
def test_request_retrieve_product_comment(client, product_comment_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric()
    url = reverse("product_reviews-detail", args=(product_comment.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.json()["id"] == product_comment.id and response.status_code == 200


@pytest.mark.django_db
def test_request_post_product_comment(client, product_comment_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric()
    url = reverse("product_reviews-list")
    json = {
        "product": product_comment.id,
        "comment": "good",
        "rating": 5
    }

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    resposne = client.post(url, data=json)

    # assert
    assert resposne.status_code == 201 and resposne.data['product'] == json["product"]


@pytest.mark.django_db
def test_request_patch_product_comment(client, product_comment_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric(user=user)
    url = reverse("product_reviews-detail", args=(product_comment.id,))
    json = {
        "product": product_comment.id,
        "comment": "good",
        "rating": 5
    }

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    resposne = client.patch(url, data=json)

    # assert
    assert resposne.status_code == 200 and resposne.data["rating"] == json["rating"]


@pytest.mark.django_db
def test_request_delete_product_comment(client, product_comment_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric(user=user)
    url = reverse("product_reviews-detail", args=(product_comment.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    resposne = client.delete(url)

    # assert
    assert resposne.status_code == 204
