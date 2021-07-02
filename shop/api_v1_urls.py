"""dj_diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from shop.api_v1_views import ProductsViewSet, ProductCommentsViewSet, OrdersViewSet, CollectionsViewSet

router = DefaultRouter()
router.register("products", ProductsViewSet, basename="products")
router.register("product-reviews", ProductCommentsViewSet, basename="product_reviews")
router.register("orders", OrdersViewSet, basename="orders")
router.register("product-collections", CollectionsViewSet, basename="product_collections")

urlpatterns = [] + router.urls
