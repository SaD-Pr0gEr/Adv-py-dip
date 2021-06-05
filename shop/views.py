from django.shortcuts import render

from shop.models import Product


def return_main_page(request):
    html = "shop/index.html"
    content = (i for i in Product.objects.all())
    context = {
        "content": content
    }
    return render(
        request=request,
        template_name=html,
        context=context
    )


def return_product(request):
    html = "shop/products.html"
    product_id = request.GET.get("id")
    content = Product.objects.get(pk=product_id)
    context = {
        "content": content
    }
    return render(
        request=request,
        template_name=html,
        context=context
    )
