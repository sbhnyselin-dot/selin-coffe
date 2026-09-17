from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm
from .models import Category, Order, OrderItem, Product


def menu(request):
    categories = Category.objects.filter(
        is_active=True
    )

    products = Product.objects.filter(
        is_available=True
    ).select_related('category')

    category_slug = request.GET.get('category')

    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    context = {
        'categories': categories,
        'products': products,
        'active_category': category_slug,
    }

    return render(request, 'orders/menu.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_available=True,
    )

    reviews = product.reviews.all()

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(
        request,
        'orders/product_detail.html',
        context,
    )


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('orders:menu')

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(
        request,
        f'{product.name} added to your cart.'
    )

    return redirect(
        request.POST.get('next')
        or 'orders:menu'
    )


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.info(
            request,
            'Your cart is empty.'
        )
        return redirect('orders:menu')

    product_ids = cart.keys()

    products = Product.objects.filter(
        id__in=product_ids,
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

    if not cart_items:
        request.session['cart'] = {}
        return redirect('orders:menu')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                )

            request.session['cart'] = {}
            request.session.modified = True

            return redirect(
                'orders:order_success',
                order_id=order.id,
            )

    else:
        form = CheckoutForm()

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'total': total,
        },
    )


def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
    )

    return render(
        request,
        'orders/order_success.html',
        {'order': order},
    )