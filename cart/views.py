from decimal import Decimal

from django.shortcuts import redirect, render

from orders.models import Product


def cart_detail(request):
    cart = request.session.get('cart', {})

    products = Product.objects.filter(
        id__in=cart.keys(),
        is_available=True,
    )

    cart_items = []
    total = Decimal('0.00')

    for product in products:
        quantity = int(cart.get(str(product.id), 0))

        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(
        request,
        'cart/cart_detail.html',
        {
            'cart_items': cart_items,
            'total': total,
        },
    )


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        cart.pop(str(product_id), None)

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:detail')


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        try:
            quantity = int(
                request.POST.get('quantity', 1)
            )
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            cart.pop(str(product_id), None)
        else:
            cart[str(product_id)] = min(
                quantity,
                99,
            )

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:detail')