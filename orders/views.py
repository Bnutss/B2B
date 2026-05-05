from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product


def cart(request):
    cart_items = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, qty in cart_items.items():
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
            subtotal = (product.price or 0) * qty
            total += subtotal
            products.append({'product': product, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    return render(request, 'orders/cart.html', {'items': products, 'total': total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = request.session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', '/catalog/'))


def cart_remove(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('orders:cart')


def checkout(request):
    return render(request, 'orders/checkout.html')
