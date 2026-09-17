from django.shortcuts import render

from orders.models import Category, Product


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True,
    ).select_related("category")[:6]

    context = {
        "categories": categories,
        "featured_products": featured_products,
    }

    return render(request, "home/home.html", context)