from django.shortcuts import render

from shop.models import Product


def return_main_page(request):
    html = "shop/index.html"
    content = (i for i in Product.objects.all())
    user = request.user
    context = {
        "content": content,
        "user": user
    }
    return render(
        request=request,
        template_name=html,
        context=context
    )


def return_product(request, pk):
    html = "shop/products.html"
    content = Product.objects.get(pk=pk)
    user = request.user
    context = {
        "content": content,
        "user": user
    }
    return render(
        request=request,
        template_name=html,
        context=context
    )


def return_page_register(request):
    html = "shop/register.html"
    return render(request, html)


def return_page_login(request):
    html = "shop/login.html"
    return render(request, html)
