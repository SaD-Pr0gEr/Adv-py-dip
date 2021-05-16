from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_request_list_orders(authorize, token_fabric, orders_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
    product = orders_fabric(
        user=user,
    )
    url = reverse("orders-list")
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200 and response.data[0]["id"] == product.id


@pytest.mark.django_db
def test_request_retrieve_orders(authorize, token_fabric, orders_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
    product = orders_fabric(
        user=user,
    )
    url = reverse("orders-detail", args=(product.id,))
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200 and response.data["id"] == product.id


@pytest.mark.django_db
def test_request_post_orders(authorize, token_fabric, orders_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
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
    client = authorize(token)

    # act
    response = client.post(url, data)
    # assert
    assert response.status_code == 201 and response.data["positions"][0]["product"] == data["positions"][0]["product"]


@pytest.mark.django_db
def test_request_patch_orders(authorize, token_fabric, orders_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
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
    client = authorize(token)

    # act
    response = client.patch(url, data)
    # assert
    assert response.status_code == 200 and response.data['positions'][0]["quantity"] == data["positions"][0]["quantity"]


@pytest.mark.django_db
def test_request_delete_orders(authorize, token_fabric, orders_fabric, product_fabric, user_fabric):
    # arrange
    user = user_fabric()
    token = token_fabric(user=user)
    order1 = orders_fabric(user=user)
    url = reverse("orders-detail", args=(order1.id, ))
    client = authorize(token)

    # act
    response = client.delete(url)

    # assert
    assert response.status_code == 204
