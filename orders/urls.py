from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path(
        'product/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
    path(
        'add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart',
    ),
    path(
        'checkout/',
        views.checkout,
        name='checkout',
    ),
    path(
        'success/<int:order_id>/',
        views.order_success,
        name='order_success',
    ),
]