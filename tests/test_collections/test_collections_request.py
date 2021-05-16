from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_request_list_collections(authorize, collections_fabric, user_fabric, token_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    quantity = 10
    collections_fabric(_quantity=quantity)
    url = reverse("product_collections-list")
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200 and len(response.data) == quantity


@pytest.mark.django_db
def test_request_retrieve_collections(authorize, collections_fabric, user_fabric, token_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    collection = collections_fabric()
    url = reverse("product_collections-detail", args=(collection.id, ))
    client = authorize(token)

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200 and response.data["id"] == collection.id


@pytest.mark.django_db
def test_request_post_collections(authorize, product_fabric, collections_fabric, user_fabric, token_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    url = reverse("product_collections-list")
    product1 = product_fabric()
    product2 = product_fabric()
    data = {
        "header": "test",
        "text": "test",
        "product": [product1.id, product2.id]
    }
    client = authorize(token)

    # act
    response = client.post(url, data)

    # assert
    assert response.status_code == 201 and response.data["header"] == data["header"]


@pytest.mark.django_db
def test_request_patch_collections(authorize, product_fabric, collections_fabric, user_fabric, token_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    collection1 = collections_fabric()
    url = reverse("product_collections-detail", args=(collection1.id, ))
    product1 = product_fabric()
    product2 = product_fabric()
    data = {
        "header": "test",
        "text": "test",
        "product": [product1.id, product2.id]
    }
    client = authorize(token)

    # act
    response = client.patch(url, data)

    # assert
    assert response.status_code == 200 and response.data["product"][0] == product1.id


@pytest.mark.django_db
def test_request_delete_collections(authorize, product_fabric, collections_fabric, user_fabric, token_fabric):
    # arrange
    user = user_fabric(is_staff=True)
    token = token_fabric(user=user)
    collection1 = collections_fabric()
    url = reverse("product_collections-detail", args=(collection1.id, ))
    # act
    client = authorize(token)
    response = client.delete(url)

    # assert
    assert response.status_code == 204
