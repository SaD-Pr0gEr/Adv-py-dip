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

from django.urls import path, include

from shop.views import return_main_page, return_product, return_page_register, return_page_login

urlpatterns = [
    path("api/v1/", include("shop.api_v1_urls")),
    path("auth/", include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("main/", return_main_page, name="main_page"),
    path("product/<int:pk>/", return_product, name="product_page"),
    path("signup/", return_page_register, name="redirect_signup"),
    path("login/", return_page_login, name="redirect_login")
]
