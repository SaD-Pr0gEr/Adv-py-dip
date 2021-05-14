from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest

from shop.models import Orders, OrderPositions, Collections, Product, ProductComment, User


@pytest.mark.django_db
def test_request_list_products(client, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    quantity = 2
    product = product_fabric(_quantity=quantity)
    url = reverse("products-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert len(response.json()) == quantity


@pytest.mark.django_db
def test_request_retrieve_product(client, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product = product_fabric()
    url = reverse("products-detail", args=(product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.json()["id"] == product.id


@pytest.mark.django_db
def test_request_post_product(client, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
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
    assert resposne.status_code == 201


@pytest.mark.django_db
def test_request_patch_product(client, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
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
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_delete_product(client, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
    token = Token.objects.create(user=user)
    create_product = product_fabric()
    url = reverse("products-detail", args=(create_product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_request_list_product_comments(client, product_comment_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    quantity = 20
    product = product_comment_fabric(_quantity=quantity)
    url = reverse("product_reviews-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert len(response.json()) == quantity


@pytest.mark.django_db
def test_request_retrieve_product_comment(client, product_comment_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric()
    url = reverse("product_reviews-detail", args=(product_comment.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.json()["id"] == product_comment.id


@pytest.mark.django_db
def test_request_post_product_comment(client, product_comment_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
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
    assert resposne.status_code == 201


@pytest.mark.django_db
def test_request_patch_product_comment(client, product_comment_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
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
    assert resposne.status_code == 200


@pytest.mark.django_db
def test_request_delete_product_comment(client, product_comment_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product_comment = product_comment_fabric(user=user)
    url = reverse("product_reviews-detail", args=(product_comment.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    resposne = client.delete(url)

    # assert
    assert resposne.status_code == 204


@pytest.mark.django_db
def test_request_list_orders(client, orders_fabric, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product = orders_fabric(
        user=user,
    )
    url = reverse("orders-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_retrieve_orders(client, orders_fabric, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product = orders_fabric(
        user=user,
    )
    url = reverse("orders-detail", args=(product.id,))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_post_orders(client, orders_fabric, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product1 = product_fabric()
    product2 = product_fabric()
    data = {
        "positions": [
            {
                "product": product1.id,
                "quantity": 10
            },
            {
                "product": product2.id,
                "quantity": 5
            }
        ]
    }
    url = reverse("orders-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.post(url, data)
    # assert
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_patch_orders(client, orders_fabric, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    product1 = product_fabric()
    product2 = product_fabric()
    order1 = orders_fabric(user=user)
    data = {
        "positions": [
            {
                "product": product1.id,
                "quantity": 10
            },
            {
                "product": product2.id,
                "quantity": 5
            }
        ]
    }
    url = reverse("orders-detail", args=(order1.id, ))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.patch(url, data)
    # assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_delete_orders(client, orders_fabric, product_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone")
    token = Token.objects.create(user=user)
    order1 = orders_fabric(user=user)
    url = reverse("orders-detail", args=(order1.id, ))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.delete(url)

    # assert
    assert response.status_code == 204


@pytest.mark.django_db
def test_request_list_collections(client, collections_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
    token = Token.objects.create(user=user)
    quantity = 10
    collections_fabric(_quantity=quantity)
    url = reverse("product_collections-list")

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_retrieve_collections(client, collections_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
    token = Token.objects.create(user=user)
    collection = collections_fabric()
    url = reverse("product_collections-detail", args=(collection.id, ))

    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    # assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_post_collections(client, product_fabric, collections_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
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
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_patch_collections(client, product_fabric, collections_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
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
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_delete_collections(client, product_fabric, collections_fabric):
    # arrange
    user = User.objects.create(username="user", first_name="ozod", last_name="alone", is_staff=True)
    token = Token.objects.create(user=user)
    collection1 = collections_fabric()
    url = reverse("product_collections-detail", args=(collection1.id, ))
    # act
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.delete(url)

    # assert
    assert response.status_code == 204
