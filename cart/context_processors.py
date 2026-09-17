def cart_context(request):

    cart = request.session.get('cart', {})

    total_quantity = 0

    if isinstance(cart, dict):

        for quantity in cart.values():

            try:
                total_quantity += int(quantity)
            except (TypeError, ValueError):
                pass

    return {
        'cart_count': total_quantity
    }